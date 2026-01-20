"""File change detection for tracking task progress."""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


class FileChangeDetector:
    """Detects file changes for tracking task progress."""

    def __init__(self, project_path: str):
        """
        Initialize file change detector.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.initial_states: Dict[str, Dict[str, any]] = {}

    def track_initial_state(self, task_id: str) -> None:
        """
        Track initial state of filesystem for a task.

        Args:
            task_id: Task ID
        """
        if task_id in self.initial_states:
            return  # Already tracked

        initial_state = {
            "tracked_at": datetime.now().isoformat(),
            "git_commits": self._get_git_commits(),
            "files": self._get_all_files(),
        }

        self.initial_states[task_id] = initial_state

    def detect_changes(
        self, task_id: str, since_iteration: int = 0
    ) -> List[str]:
        """
        Detect files that have changed since task started or since iteration.

        Args:
            task_id: Task ID
            since_iteration: Iteration number to compare from (0 = from start)

        Returns:
            List of changed file paths (relative to project root)
        """
        # Try git first (most accurate)
        git_changes = self.get_git_changes(str(self.project_path))
        if git_changes:
            return git_changes

        # Fallback to filesystem comparison
        if task_id in self.initial_states:
            initial_state = self.initial_states[task_id]
            current_files = self._get_all_files()
            initial_files = set(initial_state.get("files", []))

            # Find files that exist now but didn't exist initially
            changed = []
            for file_path in current_files:
                if file_path not in initial_files:
                    changed.append(file_path)

            return changed

        # If no initial state tracked, return empty
        return []

    def get_git_changes(self, project_path: Optional[str] = None) -> List[str]:
        """
        Get changed files using git diff.

        Args:
            project_path: Optional project path (uses instance path if None)

        Returns:
            List of changed file paths
        """
        path = Path(project_path) if project_path else self.project_path

        # Check if git repo
        git_dir = path / ".git"
        if not git_dir.exists():
            return []

        try:
            # Get uncommitted changes
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and result.stdout.strip():
                files = [
                    f.strip()
                    for f in result.stdout.strip().split("\n")
                    if f.strip()
                ]
                return files

            # Also check untracked files
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and result.stdout.strip():
                untracked = [
                    f.strip()
                    for f in result.stdout.strip().split("\n")
                    if f.strip()
                ]
                return untracked

            return []

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return []

    def get_filesystem_changes(
        self, project_path: Optional[str] = None, since: Optional[datetime] = None
    ) -> List[str]:
        """
        Get filesystem changes since a timestamp (fallback method).

        Args:
            project_path: Optional project path
            since: Timestamp to compare from

        Returns:
            List of changed file paths
        """
        path = Path(project_path) if project_path else self.project_path

        if not since:
            # If no timestamp, can't determine changes
            return []

        changed_files = []
        try:
            # Walk through project directory
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    # Check modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > since:
                        # Get relative path
                        rel_path = file_path.relative_to(path)
                        changed_files.append(str(rel_path))
        except Exception:
            pass

        return changed_files

    def _get_git_commits(self) -> List[str]:
        """
        Get list of git commit SHAs.

        Returns:
            List of commit SHAs
        """
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                commits = [
                    line.split()[0]
                    for line in result.stdout.strip().split("\n")
                    if line.strip()
                ]
                return commits
        except Exception:
            pass

        return []

    def _get_all_files(self) -> List[str]:
        """
        Get list of all files in project (relative paths).

        Returns:
            List of file paths
        """
        files = []
        try:
            # Common directories to ignore
            ignore_dirs = {
                ".git",
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
                "node_modules",
                ".venv",
                "venv",
                "env",
                ".dt",
                "dist",
                "build",
            }

            for file_path in self.project_path.rglob("*"):
                if file_path.is_file():
                    # Skip ignored directories
                    parts = file_path.parts
                    if any(ignore_dir in parts for ignore_dir in ignore_dirs):
                        continue

                    # Get relative path
                    rel_path = file_path.relative_to(self.project_path)
                    files.append(str(rel_path))
        except Exception:
            pass

        return files

    def clear_initial_state(self, task_id: str) -> None:
        """
        Clear initial state tracking for a task.

        Args:
            task_id: Task ID
        """
        if task_id in self.initial_states:
            del self.initial_states[task_id]
