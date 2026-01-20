"""Tests for TaskProgressTracker."""

import tempfile
from pathlib import Path

import pytest

from agents_army.core.progress_tracker import TaskProgressTracker
from agents_army.core.task_storage import TaskStorage


class TestTaskProgressTracker:
    """Tests for TaskProgressTracker class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def tracker(self, temp_dir):
        """Create TaskProgressTracker instance."""
        storage = TaskStorage(temp_dir)
        return TaskProgressTracker(storage)

    def test_record_iteration(self, tracker):
        """Test recording an iteration."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=["file1.py"],
            test_results={"passed": True},
            agent_output="Task completed",
            errors=[],
        )
        
        assert tracker.get_iteration_count("test_task") == 1

    def test_has_progress_with_changes(self, tracker):
        """Test has_progress when files changed."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=["file1.py"],
            test_results={"passed": False},
            agent_output="Working on it",
            errors=[],
        )
        
        assert tracker.has_progress("test_task", last_n=1) is True

    def test_has_progress_without_changes(self, tracker):
        """Test has_progress when no changes."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=[],
            test_results={"passed": False},
            agent_output="No changes",
            errors=["Error"],
        )
        
        tracker.record_iteration(
            task_id="test_task",
            iteration=2,
            file_changes=[],
            test_results={"passed": False},
            agent_output="Still no changes",
            errors=["Error"],
        )
        
        tracker.record_iteration(
            task_id="test_task",
            iteration=3,
            file_changes=[],
            test_results={"passed": False},
            agent_output="Still no changes",
            errors=["Error"],
        )
        
        # Should have no progress in last 3 iterations
        assert tracker.has_progress("test_task", last_n=3) is False

    def test_is_stuck_no_progress_and_errors(self, tracker):
        """Test is_stuck detection."""
        # Record iterations with no progress and same errors
        for i in range(1, 4):
            tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],
                test_results={"passed": False},
                agent_output="Error occurred",
                errors=["Same error"],
            )
        
        assert tracker.is_stuck("test_task") is True

    def test_is_stuck_with_progress(self, tracker):
        """Test is_stuck when there's progress."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=["file1.py"],  # Has progress
            test_results={"passed": False},
            agent_output="Working",
            errors=[],
        )
        
        assert tracker.is_stuck("test_task") is False

    def test_get_file_changes(self, tracker):
        """Test getting file changes for iteration."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=["file1.py", "file2.py"],
            test_results={},
            agent_output="",
            errors=[],
        )
        
        changes = tracker.get_file_changes("test_task", iteration=1)
        assert changes == ["file1.py", "file2.py"]

    def test_get_error_patterns(self, tracker):
        """Test getting error patterns."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=[],
            test_results={},
            agent_output="",
            errors=["Error 1", "Error 2"],
        )
        
        tracker.record_iteration(
            task_id="test_task",
            iteration=2,
            file_changes=[],
            test_results={},
            agent_output="",
            errors=["Error 1", "Error 3"],
        )
        
        patterns = tracker.get_error_patterns("test_task", last_n=2)
        assert "Error 1" in patterns
        assert "Error 2" in patterns
        assert "Error 3" in patterns

    def test_get_iteration_count(self, tracker):
        """Test getting iteration count."""
        assert tracker.get_iteration_count("test_task") == 0
        
        for i in range(1, 6):
            tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],
                test_results={},
                agent_output="",
                errors=[],
            )
        
        assert tracker.get_iteration_count("test_task") == 5

    def test_clear_progress(self, tracker):
        """Test clearing progress."""
        tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=[],
            test_results={},
            agent_output="",
            errors=[],
        )
        
        assert tracker.get_iteration_count("test_task") == 1
        
        tracker.clear_progress("test_task")
        
        assert tracker.get_iteration_count("test_task") == 0
