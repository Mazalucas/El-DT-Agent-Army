"""Task progress tracking for autonomous loops."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents_army.core.task_storage import TaskStorage


@dataclass
class IterationRecord:
    """Record of a single iteration."""

    iteration: int
    timestamp: datetime
    file_changes: List[str] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    agent_output: str = ""
    errors: List[str] = field(default_factory=list)
    has_progress: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "iteration": self.iteration,
            "timestamp": self.timestamp.isoformat(),
            "file_changes": self.file_changes,
            "test_results": self.test_results,
            "agent_output": self.agent_output,
            "errors": self.errors,
            "has_progress": self.has_progress,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IterationRecord":
        """Create from dictionary."""
        return cls(
            iteration=data["iteration"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            file_changes=data.get("file_changes", []),
            test_results=data.get("test_results", {}),
            agent_output=data.get("agent_output", ""),
            errors=data.get("errors", []),
            has_progress=data.get("has_progress", False),
        )


class TaskProgressTracker:
    """Tracks progress of task execution across iterations."""

    def __init__(self, task_storage: TaskStorage):
        """
        Initialize progress tracker.

        Args:
            task_storage: TaskStorage instance for persistence
        """
        self.task_storage = task_storage
        self.progress_dir = Path(task_storage.project_path) / "tasks" / "progress"
        self.progress_dir.mkdir(parents=True, exist_ok=True)

    def _get_progress_file(self, task_id: str) -> Path:
        """
        Get path to progress file for a task.

        Args:
            task_id: Task ID

        Returns:
            Path to progress file
        """
        return self.progress_dir / f"{task_id}.json"

    def record_iteration(
        self,
        task_id: str,
        iteration: int,
        file_changes: List[str],
        test_results: Dict[str, Any],
        agent_output: str,
        errors: List[str],
    ) -> None:
        """
        Record an iteration.

        Args:
            task_id: Task ID
            iteration: Iteration number
            file_changes: List of changed files
            test_results: Test results dictionary
            agent_output: Output from agent
            errors: List of errors encountered
        """
        # Load existing progress
        progress = self._load_progress(task_id)

        # Determine if there's progress
        has_progress = self._determine_progress(
            file_changes, test_results, errors, progress.get("iterations", [])
        )

        # Create iteration record
        record = IterationRecord(
            iteration=iteration,
            timestamp=datetime.now(),
            file_changes=file_changes,
            test_results=test_results,
            agent_output=agent_output,
            errors=errors,
            has_progress=has_progress,
        )

        # Add to progress
        if "iterations" not in progress:
            progress["iterations"] = []
        progress["iterations"].append(record.to_dict())

        # Keep only last 100 iterations
        if len(progress["iterations"]) > 100:
            progress["iterations"] = progress["iterations"][-100:]

        # Update metadata
        progress["last_iteration"] = iteration
        progress["last_updated"] = datetime.now().isoformat()

        # Save progress
        self._save_progress(task_id, progress)

    def _determine_progress(
        self,
        file_changes: List[str],
        test_results: Dict[str, Any],
        errors: List[str],
        previous_iterations: List[Dict[str, Any]],
    ) -> bool:
        """
        Determine if there's progress in this iteration.

        Args:
            file_changes: Current file changes
            test_results: Current test results
            errors: Current errors
            previous_iterations: Previous iteration records

        Returns:
            True if there's progress, False otherwise
        """
        # Progress if files changed
        if file_changes:
            return True

        # Progress if tests improved
        if test_results.get("passed", False):
            # Check if previous iteration had failing tests
            if previous_iterations:
                last_test = previous_iterations[-1].get("test_results", {})
                if not last_test.get("passed", False):
                    return True

        # Progress if errors decreased
        if previous_iterations:
            last_errors = previous_iterations[-1].get("errors", [])
            if len(errors) < len(last_errors):
                return True

        # No progress detected
        return False

    def has_progress(self, task_id: str, last_n: int = 3) -> bool:
        """
        Check if there's been progress in the last N iterations.

        Args:
            task_id: Task ID
            last_n: Number of recent iterations to check

        Returns:
            True if there's progress, False otherwise
        """
        progress = self._load_progress(task_id)
        iterations = progress.get("iterations", [])

        if len(iterations) < last_n:
            # Not enough iterations yet
            return True  # Assume progress if just starting

        # Check last N iterations
        recent = iterations[-last_n:]
        return any(iter_record.get("has_progress", False) for iter_record in recent)

    def is_stuck(self, task_id: str) -> bool:
        """
        Check if task is stuck (no progress and repeated errors).

        Args:
            task_id: Task ID

        Returns:
            True if stuck, False otherwise
        """
        progress = self._load_progress(task_id)
        iterations = progress.get("iterations", [])

        if len(iterations) < 3:
            return False  # Need at least 3 iterations to determine if stuck

        # Check last 3 iterations
        recent = iterations[-3:]

        # Stuck if no progress in last 3 iterations
        has_any_progress = any(iter_record.get("has_progress", False) for iter_record in recent)
        if has_any_progress:
            return False

        # Check for repeated errors
        errors_list = [iter_record.get("errors", []) for iter_record in recent]
        if not all(errors_list):
            return False  # Not all iterations have errors

        # Check if errors are similar/repeated
        if len(errors_list) >= 2:
            first_errors = set(errors_list[0])
            for error_set in errors_list[1:]:
                if not first_errors.intersection(set(error_set)):
                    return False  # Errors are different, not stuck

        # No progress and repeated errors = stuck
        return True

    def get_file_changes(self, task_id: str, iteration: int) -> List[str]:
        """
        Get file changes for a specific iteration.

        Args:
            task_id: Task ID
            iteration: Iteration number

        Returns:
            List of changed files
        """
        progress = self._load_progress(task_id)
        iterations = progress.get("iterations", [])

        for iter_record in iterations:
            if iter_record.get("iteration") == iteration:
                return iter_record.get("file_changes", [])

        return []

    def get_error_patterns(self, task_id: str, last_n: int = 5) -> List[str]:
        """
        Get error patterns from recent iterations.

        Args:
            task_id: Task ID
            last_n: Number of recent iterations to analyze

        Returns:
            List of unique error patterns
        """
        progress = self._load_progress(task_id)
        iterations = progress.get("iterations", [])

        if not iterations:
            return []

        # Get errors from last N iterations
        recent = iterations[-last_n:]
        all_errors = []
        for iter_record in recent:
            all_errors.extend(iter_record.get("errors", []))

        # Return unique errors
        return list(set(all_errors))

    def get_iteration_count(self, task_id: str) -> int:
        """
        Get total number of iterations for a task.

        Args:
            task_id: Task ID

        Returns:
            Number of iterations
        """
        progress = self._load_progress(task_id)
        return len(progress.get("iterations", []))

    def _load_progress(self, task_id: str) -> Dict[str, Any]:
        """
        Load progress data for a task.

        Args:
            task_id: Task ID

        Returns:
            Progress data dictionary
        """
        progress_file = self._get_progress_file(task_id)
        if not progress_file.exists():
            return {"iterations": []}

        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert iteration dicts back to proper format
                if "iterations" in data:
                    data["iterations"] = [
                        IterationRecord.from_dict(iter_dict).to_dict()
                        for iter_dict in data["iterations"]
                    ]
                return data
        except Exception:
            return {"iterations": []}

    def _save_progress(self, task_id: str, progress: Dict[str, Any]) -> None:
        """
        Save progress data for a task.

        Args:
            task_id: Task ID
            progress: Progress data dictionary
        """
        progress_file = self._get_progress_file(task_id)
        try:
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Fail silently if can't save

    def clear_progress(self, task_id: str) -> None:
        """
        Clear progress data for a task.

        Args:
            task_id: Task ID
        """
        progress_file = self._get_progress_file(task_id)
        if progress_file.exists():
            progress_file.unlink()
