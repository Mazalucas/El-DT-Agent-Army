"""Circuit breaker for detecting stuck loops."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agents_army.core.progress_tracker import TaskProgressTracker


class CircuitState(str, Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit open, blocking execution
    HALF_OPEN = "half_open"  # Testing if issue resolved


@dataclass
class CircuitBreakerResult:
    """Result of circuit breaker check."""

    should_continue: bool
    reason: str
    state: str
    iteration: int

    def __str__(self) -> str:
        """String representation."""
        return f"CircuitBreakerResult(state={self.state}, should_continue={self.should_continue}, reason={self.reason})"


class TaskCircuitBreaker:
    """Circuit breaker for detecting and preventing stuck loops."""

    def __init__(
        self,
        no_progress_threshold: int = 3,
        same_error_threshold: int = 5,
        output_decline_threshold: float = 0.7,
        strict_mode: bool = False,
    ):
        """
        Initialize circuit breaker.

        Args:
            no_progress_threshold: Iterations without progress to open circuit
            same_error_threshold: Repeated errors to open circuit
            output_decline_threshold: Output decline percentage to open (0.0-1.0)
            strict_mode: If True, use stricter thresholds (for level 3)
        """
        self.no_progress_threshold = no_progress_threshold
        self.same_error_threshold = same_error_threshold
        self.output_decline_threshold = output_decline_threshold
        self.strict_mode = strict_mode

        # Adjust thresholds for strict mode
        if strict_mode:
            self.no_progress_threshold = max(2, no_progress_threshold - 1)
            self.same_error_threshold = max(3, same_error_threshold - 2)

        # State storage: task_id -> state info
        self._states: Dict[str, Dict[str, Any]] = {}

    def check_should_continue(
        self,
        task_id: str,
        iteration: int,
        progress_tracker: TaskProgressTracker,
    ) -> CircuitBreakerResult:
        """
        Check if loop should continue or circuit should open.

        Args:
            task_id: Task ID
            iteration: Current iteration number
            progress_tracker: Progress tracker instance

        Returns:
            CircuitBreakerResult indicating if should continue
        """
        # Get current state
        state_info = self._get_state(task_id)
        current_state = CircuitState(state_info.get("state", CircuitState.CLOSED.value))

        # If circuit is open, check if we should try half-open
        if current_state == CircuitState.OPEN:
            # Check if enough time has passed to try half-open
            opened_at = state_info.get("opened_at")
            if opened_at:
                opened_time = datetime.fromisoformat(opened_at)
                time_since_open = (datetime.now() - opened_time).total_seconds()
                # Wait 60 seconds before trying half-open
                if time_since_open > 60:
                    self._set_state(task_id, CircuitState.HALF_OPEN)
                    return CircuitBreakerResult(
                        should_continue=True,
                        reason="Circuit entering half-open state for testing",
                        state=CircuitState.HALF_OPEN.value,
                        iteration=iteration,
                    )
            return CircuitBreakerResult(
                should_continue=False,
                reason="Circuit breaker is OPEN - loop detected as stuck",
                state=CircuitState.OPEN.value,
                iteration=iteration,
            )

        # Check conditions for opening circuit
        should_open, reason = self._should_open_circuit(
            task_id, iteration, progress_tracker, current_state
        )

        if should_open:
            self._set_state(task_id, CircuitState.OPEN)
            return CircuitBreakerResult(
                should_continue=False,
                reason=reason,
                state=CircuitState.OPEN.value,
                iteration=iteration,
            )

        # If half-open and this iteration succeeds, close circuit
        if current_state == CircuitState.HALF_OPEN:
            if progress_tracker.has_progress(task_id, last_n=1):
                self._set_state(task_id, CircuitState.CLOSED)
                return CircuitBreakerResult(
                    should_continue=True,
                    reason="Circuit closed - issue resolved",
                    state=CircuitState.CLOSED.value,
                    iteration=iteration,
                )

        # Record this iteration
        self.record_iteration(
            task_id,
            has_progress=progress_tracker.has_progress(task_id, last_n=1),
            errors=progress_tracker.get_error_patterns(task_id, last_n=1),
        )

        return CircuitBreakerResult(
            should_continue=True,
            reason="Circuit closed - normal operation",
            state=CircuitState.CLOSED.value,
            iteration=iteration,
        )

    def _should_open_circuit(
        self,
        task_id: str,
        iteration: int,
        progress_tracker: TaskProgressTracker,
        current_state: CircuitState,
    ) -> Tuple[bool, str]:
        """
        Determine if circuit should open.

        Args:
            task_id: Task ID
            iteration: Current iteration
            progress_tracker: Progress tracker
            current_state: Current circuit state

        Returns:
            Tuple of (should_open, reason)
        """
        # Check for no progress
        if not progress_tracker.has_progress(task_id, last_n=self.no_progress_threshold):
            return (
                True,
                f"No progress in last {self.no_progress_threshold} iterations",
            )

        # Check for repeated errors
        error_patterns = progress_tracker.get_error_patterns(
            task_id, last_n=self.same_error_threshold
        )
        if len(error_patterns) >= self.same_error_threshold:
            # Check if errors are the same
            recent_errors = progress_tracker.get_error_patterns(task_id, last_n=3)
            if len(recent_errors) == 1 and len(recent_errors[0]) > 0:
                return (
                    True,
                    f"Same error repeated {self.same_error_threshold} times",
                )

        # Check if task is stuck
        if progress_tracker.is_stuck(task_id):
            return (True, "Task detected as stuck (no progress + repeated errors)")

        return (False, "")

    def record_iteration(self, task_id: str, has_progress: bool, errors: List[str]) -> None:
        """
        Record an iteration for circuit breaker tracking.

        Args:
            task_id: Task ID
            has_progress: Whether iteration had progress
            errors: List of errors in iteration
        """
        state_info = self._get_state(task_id)
        if "iterations" not in state_info:
            state_info["iterations"] = []

        state_info["iterations"].append(
            {
                "has_progress": has_progress,
                "errors": errors,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Keep only last 20 iterations
        if len(state_info["iterations"]) > 20:
            state_info["iterations"] = state_info["iterations"][-20:]

        self._save_state(task_id, state_info)

    def is_open(self, task_id: str) -> bool:
        """
        Check if circuit is open for a task.

        Args:
            task_id: Task ID

        Returns:
            True if circuit is open
        """
        state_info = self._get_state(task_id)
        return state_info.get("state") == CircuitState.OPEN.value

    def reset(self, task_id: str) -> None:
        """
        Reset circuit breaker for a task.

        Args:
            task_id: Task ID
        """
        self._set_state(task_id, CircuitState.CLOSED)
        state_info = self._get_state(task_id)
        state_info["iterations"] = []
        self._save_state(task_id, state_info)

    def _get_state(self, task_id: str) -> Dict[str, any]:
        """Get state info for a task."""
        if task_id not in self._states:
            self._states[task_id] = {
                "state": CircuitState.CLOSED.value,
                "iterations": [],
            }
        return self._states[task_id]

    def _set_state(self, task_id: str, state: CircuitState) -> None:
        """Set state for a task."""
        state_info = self._get_state(task_id)
        state_info["state"] = state.value
        if state == CircuitState.OPEN:
            state_info["opened_at"] = datetime.now().isoformat()
        self._save_state(task_id, state_info)

    def _save_state(self, task_id: str, state_info: Dict[str, Any]) -> None:
        """Save state (in-memory only for now, could persist if needed)."""
        self._states[task_id] = state_info
