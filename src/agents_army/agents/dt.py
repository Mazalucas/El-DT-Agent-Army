"""El DT (Director Técnico) - Main coordinator agent."""

import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents_army.core.agent import Agent, AgentConfig, LLMProvider
from agents_army.core.models import Project, Task, TaskAssignment, TaskResult
from agents_army.protocol.message import AgentMessage
from agents_army.core.rules import RulesChecker, RulesLoader
from agents_army.core.system import AgentSystem
from agents_army.core.task_storage import TaskStorage
from agents_army.protocol.types import AgentRole, MessageType


class DT(Agent):
    """
    El DT (Director Técnico) - Main coordinator agent.

    Based on taskmaster architecture with multi-agent coordination capabilities.
    """

    def __init__(
        self,
        name: str = "El DT",
        instructions: Optional[str] = None,
        model: str = "gpt-4",
        project_path: str = ".taskmaster",
        prd_path: str = ".taskmaster/docs/prd.txt",
        llm_provider: Optional[LLMProvider] = None,
    ):
        """
        Initialize El DT.

        Args:
            name: Agent name
            instructions: Custom instructions (uses defaults if None)
            model: LLM model to use
            project_path: Path to .taskmaster directory
            prd_path: Path to PRD file
            llm_provider: Optional LLM provider
        """
        # Default instructions for El DT
        default_instructions = (
            "You are El DT (Technical Director), responsible for coordinating "
            "and managing all project tasks and agents. You parse PRDs, generate "
            "tasks, assign them to specialized agents, and ensure project completion."
        )

        config = AgentConfig(
            name=name,
            role=AgentRole.DT,
            goal="Coordinate and manage all project tasks and agents",
            backstory=(
                "You are the Technical Director, responsible for orchestrating "
                "the entire project. You have deep technical knowledge and "
                "excellent coordination skills."
            ),
            instructions=instructions or default_instructions,
            model=model,
            allow_delegation=True,
            max_iterations=5,
        )

        super().__init__(config, llm_provider)

        self.project_path = Path(project_path)
        self.prd_path = Path(prd_path)
        self.task_storage = TaskStorage(str(self.project_path))
        self.current_project: Optional[Project] = None
        self.rules_checker: Optional[RulesChecker] = None
        self.system: Optional[AgentSystem] = None

    def set_system(self, system: AgentSystem) -> None:
        """
        Set the agent system for coordination.

        Args:
            system: AgentSystem instance
        """
        self.system = system

    async def initialize_project(
        self,
        project_name: str,
        description: str,
        rules: Optional[List[str]] = None,
    ) -> Project:
        """
        Initialize a new project.

        Creates the .taskmaster directory structure.

        Args:
            project_name: Name of the project
            description: Project description
            rules: Optional list of project rules

        Returns:
            Project instance
        """
        # Create directory structure
        (self.project_path / "docs").mkdir(parents=True, exist_ok=True)
        (self.project_path / "tasks").mkdir(parents=True, exist_ok=True)
        (self.project_path / "rules").mkdir(parents=True, exist_ok=True)
        (self.project_path / "config").mkdir(parents=True, exist_ok=True)
        (self.project_path / "templates").mkdir(parents=True, exist_ok=True)

        # Create project
        project = Project(
            name=project_name,
            description=description,
            path=str(self.project_path),
            prd_path=str(self.prd_path),
            rules=rules or [],
        )

        self.current_project = project

        # Load rules
        rules_dict = RulesLoader.load_all_rules(str(self.project_path))
        self.rules_checker = RulesChecker(rules_dict)

        return project

    async def parse_prd(self, prd_path: Optional[str] = None) -> List[Task]:
        """
        Parse a PRD and generate tasks.

        Args:
            prd_path: Optional path to PRD file (uses default if None)

        Returns:
            List of generated tasks
        """
        prd_file = Path(prd_path) if prd_path else self.prd_path

        if not prd_file.exists():
            raise FileNotFoundError(f"PRD file not found: {prd_file}")

        # Read PRD
        with open(prd_file, "r", encoding="utf-8") as f:
            prd_content = f.read()

        # Generate tasks using LLM
        prompt = f"""Parse the following PRD and generate a list of tasks.

PRD:
{prd_content}

Generate tasks in JSON format:
[
  {{
    "title": "Task title",
    "description": "Task description",
    "priority": 3,
    "tags": ["tag1", "tag2"]
  }}
]

Return only valid JSON array."""

        try:
            response = await self.generate_response(prompt)
            # Parse JSON response (simplified - in production would be more robust)
            import json

            # Extract JSON from response
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            if json_start >= 0 and json_end > json_start:
                tasks_data = json.loads(response[json_start:json_end])
            else:
                # Fallback: create a single task
                tasks_data = [
                    {
                        "title": "Implement PRD requirements",
                        "description": prd_content[:200],
                        "priority": 3,
                        "tags": [],
                    }
                ]
        except Exception:
            # Fallback: create a single task
            tasks_data = [
                {
                    "title": "Implement PRD requirements",
                    "description": prd_content[:200],
                    "priority": 3,
                    "tags": [],
                }
            ]

        # Create Task objects
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                title=task_data.get("title", "Untitled Task"),
                description=task_data.get("description", ""),
                priority=task_data.get("priority", 3),
                tags=task_data.get("tags", []),
            )
            tasks.append(task)
            self.task_storage.save_task(task)

        return tasks

    async def get_tasks(
        self,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 10,
    ) -> List[Task]:
        """
        Get list of tasks.

        Args:
            status: Optional status filter
            tag: Optional tag filter
            limit: Maximum number of tasks

        Returns:
            List of tasks
        """
        tasks = self.task_storage.list_tasks(status=status, limit=limit)

        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        return tasks

    async def get_next_task(self) -> Optional[Task]:
        """
        Get the next task to work on.

        Returns:
            Next task or None if no tasks available
        """
        # Get pending tasks
        pending_tasks = await self.get_tasks(status="pending", limit=100)

        # Filter ready tasks (no dependencies)
        ready_tasks = [t for t in pending_tasks if t.is_ready()]

        if not ready_tasks:
            return None

        # Sort by priority (highest first)
        ready_tasks.sort(key=lambda t: t.priority, reverse=True)

        return ready_tasks[0]

    async def assign_task(
        self, task: Task, agent_role: AgentRole
    ) -> TaskAssignment:
        """
        Assign a task to an agent.

        Args:
            task: Task to assign
            agent_role: Role of agent to assign to

        Returns:
            TaskAssignment
        """
        old_status = task.status
        task.assigned_agent = agent_role
        task.update_status("in-progress")
        
        # Move task file first, then save
        if old_status != "in-progress":
            self.task_storage.move_task(task.id, old_status, "in-progress")
        
        self.task_storage.save_task(task)

        assignment = TaskAssignment(
            task_id=task.id,
            agent_role=agent_role,
        )

        return assignment

    async def update_task_status(
        self,
        task_id: str,
        status: str,
        agent_result: Optional[TaskResult] = None,
    ) -> Task:
        """
        Update task status.

        Args:
            task_id: Task ID
            status: New status
            agent_result: Optional result from agent

        Returns:
            Updated task
        """
        task = self.task_storage.load_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        old_status = task.status
        task.update_status(status)

        # Move task file if status changed
        if old_status != status:
            self.task_storage.move_task(task.id, old_status, status)

        self.task_storage.save_task(task)

        return task

    async def expand_task(self, task_id: str) -> Task:
        """
        Expand a task with more details.

        Args:
            task_id: Task ID

        Returns:
            Expanded task
        """
        task = self.task_storage.load_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        # Use LLM to expand task
        prompt = f"""Expand the following task with more details:

Title: {task.title}
Description: {task.description}

Provide:
1. More detailed description
2. Subtasks if applicable
3. Required resources
4. Estimated complexity

Return JSON:
{{
  "description": "expanded description",
  "subtasks": ["subtask1", "subtask2"],
  "resources": ["resource1"],
  "complexity": "low|medium|high"
}}"""

        try:
            response = await self.generate_response(prompt)
            import json

            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                expanded = json.loads(response[json_start:json_end])
                task.description = expanded.get("description", task.description)
                task.metadata.update(expanded)
        except Exception:
            pass  # Keep original task if expansion fails

        self.task_storage.save_task(task)
        return task

    async def research(
        self, query: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform research.

        Args:
            query: Research query
            context: Optional context

        Returns:
            Research results
        """
        # If Researcher agent is available, delegate
        if self.system:
            researcher = self.system.get_agent(AgentRole.RESEARCHER)
            if researcher:
                message = AgentMessage(
                    from_role=self.role,
                    to_role=AgentRole.RESEARCHER,
                    type=MessageType.TASK_REQUEST,
                    payload={"query": query, "context": context},
                )
                response = await researcher.handle_message(message)
                if response:
                    return response.payload

        # Otherwise, use LLM directly
        prompt = f"Research: {query}"
        if context:
            prompt += f"\n\nContext: {context}"

        result = await self.generate_response(prompt)

        return {
            "query": query,
            "result": result,
            "sources": [],
        }

    async def _process_message(
        self, message: AgentMessage
    ) -> Optional[AgentMessage]:
        """
        Process incoming message.

        Args:
            message: Incoming message

        Returns:
            Optional response message
        """
        # Handle different message types
        if message.type == MessageType.TASK_REQUEST:
            # Handle task request
            task_id = message.payload.get("task_id")
            if task_id:
                task = self.task_storage.load_task(task_id)
                if task:
                    # Process task assignment
                    agent_role = message.payload.get("agent_role")
                    if agent_role:
                        await self.assign_task(task, AgentRole(agent_role))

        elif message.type == MessageType.STATUS_QUERY:
            # Return status
            tasks = await self.get_tasks(limit=10)
            return AgentMessage(
                from_role=self.role,
                to_role=message.from_role,
                type=MessageType.STATUS_RESPONSE,
                payload={
                    "total_tasks": len(await self.get_tasks()),
                    "pending": len(await self.get_tasks(status="pending")),
                    "in_progress": len(await self.get_tasks(status="in-progress")),
                    "done": len(await self.get_tasks(status="done")),
                    "recent_tasks": [t.to_dict() for t in tasks[:5]],
                },
                reply_to=message.id,
            )

        return None
