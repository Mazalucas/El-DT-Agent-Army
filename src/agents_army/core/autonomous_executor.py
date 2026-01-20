"""Autonomous task executor with iterative loops."""

import asyncio
from typing import Any, Dict, List, Optional, Tuple

from agents_army.core.circuit_breaker import TaskCircuitBreaker
from agents_army.core.completion import CompletionCriteria
from agents_army.core.file_detector import FileChangeDetector
from agents_army.core.models import ActionResult, Task, TaskResult
from agents_army.core.progress_tracker import TaskProgressTracker
from agents_army.core.session_manager import TaskSession, TaskSessionManager
from agents_army.core.validation import ValidationRunner
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class AutonomousTaskExecutor:
    """Executes tasks autonomously with iterative loops until completion."""

    def __init__(
        self,
        dt: Any,  # DT instance
        max_iterations: int = 50,
        enable_circuit_breaker: bool = True,
        enable_sessions: bool = True,
        circuit_breaker_strict: bool = False,
    ):
        """
        Initialize autonomous task executor.

        Args:
            dt: DT instance (for accessing system and storage)
            max_iterations: Maximum number of iterations
            enable_circuit_breaker: Enable circuit breaker protection
            enable_sessions: Enable session management
            circuit_breaker_strict: Use strict circuit breaker mode
        """
        self.dt = dt
        self.max_iterations = max_iterations
        self.enable_circuit_breaker = enable_circuit_breaker
        self.enable_sessions = enable_sessions
        self.circuit_breaker_strict = circuit_breaker_strict

        # Initialize components
        self.progress_tracker = TaskProgressTracker(dt.task_storage)
        self.circuit_breaker = (
            TaskCircuitBreaker(strict_mode=circuit_breaker_strict)
            if enable_circuit_breaker
            else None
        )
        self.session_manager = TaskSessionManager(dt.task_storage) if enable_sessions else None
        # Determine project path for file detection and validation
        from pathlib import Path

        dt_path = Path(dt.project_path) if isinstance(dt.project_path, str) else dt.project_path

        # If .dt directory, use parent; otherwise use project path
        if dt_path.name == ".dt":
            project_root = str(dt_path.parent)
        else:
            project_root = str(dt_path)

        # Use current project path if available
        if dt.current_project and hasattr(dt.current_project, "path"):
            project_root = dt.current_project.path

        self.file_detector = FileChangeDetector(project_root)
        self.validation_runner = ValidationRunner(project_root)

    async def execute_until_complete(
        self,
        task: Task,
        agent_role: AgentRole,
        completion_criteria: CompletionCriteria,
        validate_each_iteration: bool = False,
    ) -> ActionResult:
        """
        Execute task until completion criteria are met.

        Args:
            task: Task to execute
            agent_role: Agent role to execute task
            completion_criteria: Criteria for completion
            validate_each_iteration: Validate on each iteration (for level 3)

        Returns:
            ActionResult
        """
        # Set validation runner in criteria
        completion_criteria.validation_runner = self.validation_runner

        # Track initial state for file change detection
        self.file_detector.track_initial_state(task.id)

        # Get or create session
        session = None
        if self.enable_sessions:
            session = self.session_manager.get_or_create_session(task.id, agent_role)

        # Main loop
        for iteration in range(1, self.max_iterations + 1):
            # Check circuit breaker
            if self.enable_circuit_breaker and self.circuit_breaker:
                cb_result = self.circuit_breaker.check_should_continue(
                    task.id, iteration, self.progress_tracker
                )
                if not cb_result.should_continue:
                    # Circuit breaker opened - abort
                    if self.enable_sessions and session:
                        self.session_manager.reset_session(task.id, "circuit_breaker_open")
                    return ActionResult(
                        success=False,
                        action_taken="aborted",
                        result={
                            "task_id": task.id,
                            "iteration": iteration,
                            "reason": cb_result.reason,
                        },
                        escalated=False,
                        error=f"Circuit breaker opened: {cb_result.reason}",
                    )

            # Execute iteration
            try:
                task_result, agent_output, file_changes = await self._execute_iteration(
                    task, agent_role, session, iteration
                )
            except Exception as e:
                # Error executing iteration
                errors = [str(e)]
                self.progress_tracker.record_iteration(
                    task.id,
                    iteration,
                    [],
                    {"passed": False, "error": str(e)},
                    "",
                    errors,
                )
                continue  # Try next iteration

            # Detect file changes if not provided
            if not file_changes:
                file_changes = self.file_detector.detect_changes(task.id, iteration)

            # Run validation if required
            test_results = {}
            if validate_each_iteration or completion_criteria.tests_must_pass:
                test_results_obj = self.validation_runner.run_tests()
                test_results = {
                    "passed": test_results_obj.passed,
                    "output": test_results_obj.output,
                    "coverage": test_results_obj.coverage,
                }

            # Record progress
            errors = []
            if task_result.error:
                errors.append(task_result.error)
            if not test_results.get("passed", True):
                errors.append("Tests failed")

            self.progress_tracker.record_iteration(
                task.id,
                iteration,
                file_changes,
                test_results,
                agent_output,
                errors,
            )

            # Add iteration to session
            if self.enable_sessions and session:
                self.session_manager.add_iteration(
                    task.id, iteration, agent_output, file_changes, errors
                )

            # Check completion
            is_complete = completion_criteria.is_complete(task_result, agent_output, file_changes)

            if is_complete:
                # Task complete!
                return ActionResult(
                    success=True,
                    action_taken="completed",
                    result={
                        "task_id": task.id,
                        "iteration": iteration,
                        "task_result": {
                            "task_id": task_result.task_id,
                            "status": task_result.status,
                            "result": task_result.result,
                            "error": task_result.error,
                        },
                    },
                    escalated=False,
                )

            # Not complete, continue to next iteration
            # Small delay to avoid tight loops
            await asyncio.sleep(0.1)

        # Max iterations reached
        return ActionResult(
            success=False,
            action_taken="max_iterations_reached",
            result={
                "task_id": task.id,
                "iteration": self.max_iterations,
            },
            escalated=True,
            escalation_reason=f"Reached maximum iterations ({self.max_iterations})",
        )

    async def _execute_iteration(
        self,
        task: Task,
        agent_role: AgentRole,
        session: Optional[TaskSession],
        iteration: int,
    ) -> Tuple[TaskResult, str, List[str]]:
        """
        Execute a single iteration of the task.

        Args:
            task: Task to execute
            agent_role: Agent role
            session: Optional session for context
            iteration: Iteration number

        Returns:
            Tuple of (TaskResult, agent_output, file_changes)
        """
        # Build context from session if available
        context = {}
        if session:
            context = session.context.copy()
            # Add iteration history
            context["previous_iterations"] = len(session.iterations)
            if session.iterations:
                context["last_output"] = session.iterations[-1].get("agent_output", "")

        # Create message for agent
        payload = {
            "task_id": task.id,
            "description": task.description,
            "iteration": iteration,
        }

        # Add context if available
        if context:
            payload["context"] = context

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=agent_role,
            type=MessageType.TASK_REQUEST,
            payload=payload,
        )

        # Execute agent
        agent_output = ""
        task_result = None

        if self.dt.system:
            agent = self.dt.system.get_agent(agent_role)
            if agent:
                try:
                    response = await agent.handle_message(message)
                    if response:
                        # Extract output from response
                        agent_output = self._extract_agent_output(response)

                        # Create task result
                        task_result = TaskResult(
                            task_id=task.id,
                            status=(
                                "completed"
                                if response.payload.get("status") == "completed"
                                else "partial"
                            ),
                            result=response.payload.get("result", {}),
                            error=response.payload.get("error"),
                            agent_id=agent.id,
                        )
                    else:
                        # No response from agent
                        task_result = TaskResult(
                            task_id=task.id,
                            status="failed",
                            result={},
                            error="No response from agent",
                            agent_id=None,
                        )
                except Exception as e:
                    task_result = TaskResult(
                        task_id=task.id,
                        status="failed",
                        result={},
                        error=str(e),
                        agent_id=None,
                    )
            else:
                task_result = TaskResult(
                    task_id=task.id,
                    status="failed",
                    result={},
                    error=f"Agent {agent_role.value} not found",
                    agent_id=None,
                )
        else:
            task_result = TaskResult(
                task_id=task.id,
                status="failed",
                result={},
                error="DT system not available",
                agent_id=None,
            )

        # Detect file changes
        file_changes = self.file_detector.detect_changes(task.id, iteration)

        return task_result, agent_output, file_changes

    def _extract_agent_output(self, response: AgentMessage) -> str:
        """
        Extract agent output from response message.

        Args:
            response: Response message from agent

        Returns:
            Agent output string
        """
        payload = response.payload or {}

        # Try different possible output fields
        output = payload.get("output", "")
        if not output:
            output = payload.get("result", "")
        if not output:
            output = payload.get("content", "")
        if not output:
            # Fallback to string representation of payload
            output = str(payload)

        return output

    def _check_completion(
        self,
        task_result: TaskResult,
        agent_output: str,
        completion_criteria: CompletionCriteria,
    ) -> bool:
        """
        Check if task is complete based on criteria.

        Args:
            task_result: Task execution result
            agent_output: Output from agent
            completion_criteria: Completion criteria

        Returns:
            True if complete
        """
        return completion_criteria.is_complete(task_result, agent_output)
