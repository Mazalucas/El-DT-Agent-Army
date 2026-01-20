"""Task storage and persistence."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from agents_army.core.models import Task


class TaskStorage:
    """Storage for tasks using file system."""

    def __init__(self, project_path: str):
        """
        Initialize task storage.

        Args:
            project_path: Path to .dt directory
        """
        self.project_path = Path(project_path)
        self.tasks_dir = self.project_path / "tasks"
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure task directories exist."""
        for status in ["pending", "in-progress", "done", "blocked"]:
            (self.tasks_dir / status).mkdir(parents=True, exist_ok=True)

    def _get_task_file(self, task_id: str, status: Optional[str] = None) -> Path:
        """
        Get path to task file.

        Args:
            task_id: Task ID
            status: Optional status to determine directory

        Returns:
            Path to task file
        """
        if status is None:
            # Search in all directories
            for status_dir in ["pending", "in-progress", "done", "blocked"]:
                task_file = self.tasks_dir / status_dir / f"{task_id}.json"
                if task_file.exists():
                    return task_file
            # Default to pending if not found
            return self.tasks_dir / "pending" / f"{task_id}.json"

        return self.tasks_dir / status / f"{task_id}.json"

    def save_task(self, task: Task) -> None:
        """
        Save a task to storage.

        Args:
            task: Task to save
        """
        task_file = self._get_task_file(task.id, task.status)
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task.to_dict(), f, indent=2, ensure_ascii=False)

    def load_task(self, task_id: str) -> Optional[Task]:
        """
        Load a task from storage.

        Args:
            task_id: Task ID

        Returns:
            Task or None if not found
        """
        task_file = self._get_task_file(task_id)
        if not task_file.exists():
            return None

        with open(task_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Task.from_dict(data)

    def move_task(self, task_id: str, old_status: str, new_status: str) -> None:
        """
        Move task between status directories.

        Args:
            task_id: Task ID
            old_status: Current status
            new_status: New status
        """
        old_file = self.tasks_dir / old_status / f"{task_id}.json"
        new_file = self.tasks_dir / new_status / f"{task_id}.json"

        if old_file.exists():
            # Remove new file if it exists (shouldn't happen, but just in case)
            if new_file.exists():
                new_file.unlink()
            old_file.rename(new_file)

    def list_tasks(
        self, status: Optional[str] = None, limit: int = 100
    ) -> List[Task]:
        """
        List tasks.

        Args:
            status: Optional status filter
            limit: Maximum number of tasks to return

        Returns:
            List of tasks
        """
        tasks = []

        if status:
            status_dirs = [status]
        else:
            status_dirs = ["pending", "in-progress", "done", "blocked"]

        for status_dir in status_dirs:
            status_path = self.tasks_dir / status_dir
            if not status_path.exists():
                continue

            for task_file in status_path.glob("*.json"):
                try:
                    with open(task_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        tasks.append(Task.from_dict(data))
                except Exception:
                    continue

                if len(tasks) >= limit:
                    return tasks

        return tasks

    def delete_task(self, task_id: str) -> None:
        """
        Delete a task.

        Args:
            task_id: Task ID
        """
        task_file = self._get_task_file(task_id)
        if task_file.exists():
            task_file.unlink()
