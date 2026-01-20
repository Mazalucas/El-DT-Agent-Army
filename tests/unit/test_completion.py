"""Tests for CompletionCriteria."""

import pytest

from agents_army.core.completion import CompletionCriteria, CompletionCriteriaFactory
from agents_army.core.models import Task, TaskResult


class TestCompletionCriteria:
    """Tests for CompletionCriteria class."""

    def test_is_complete_with_exit_signal(self):
        """Test completion detection with exit signal."""
        criteria = CompletionCriteria(
            agent_exit_signal=True,
            min_completion_indicators=2,
            min_file_changes=1,
        )

        result = TaskResult(
            task_id="test_task",
            status="completed",
        )

        agent_output = """
        Task completed successfully.
        EXIT_SIGNAL: true
        All work is done.
        """

        assert criteria.is_complete(result, agent_output, ["file1.py"]) is True

    def test_is_complete_without_exit_signal(self):
        """Test completion detection without exit signal when required."""
        criteria = CompletionCriteria(
            agent_exit_signal=True,
            min_completion_indicators=2,
            min_file_changes=1,
        )

        result = TaskResult(
            task_id="test_task",
            status="completed",
        )

        agent_output = "Task completed successfully."

        # Should fail because exit signal required but not present
        assert criteria.is_complete(result, agent_output, ["file1.py"]) is False

    def test_is_complete_with_insufficient_indicators(self):
        """Test completion detection with insufficient indicators."""
        criteria = CompletionCriteria(
            agent_exit_signal=False,
            min_completion_indicators=3,
            min_file_changes=1,
        )

        result = TaskResult(
            task_id="test_task",
            status="completed",
        )

        agent_output = "Done."

        # Should fail because not enough completion indicators
        assert criteria.is_complete(result, agent_output, ["file1.py"]) is False

    def test_is_complete_with_insufficient_file_changes(self):
        """Test completion detection with insufficient file changes."""
        criteria = CompletionCriteria(
            agent_exit_signal=False,
            min_completion_indicators=1,
            min_file_changes=2,
        )

        result = TaskResult(
            task_id="test_task",
            status="completed",
        )

        agent_output = "Task completed successfully."

        # Should fail because not enough file changes
        assert criteria.is_complete(result, agent_output, ["file1.py"]) is False

    def test_extract_exit_signal_explicit(self):
        """Test extracting explicit exit signal."""
        criteria = CompletionCriteria()

        output = "EXIT_SIGNAL: true"
        assert criteria.extract_exit_signal(output) is True

        output = "EXIT_SIGNAL: True"
        assert criteria.extract_exit_signal(output) is True

        output = "EXIT_SIGNAL: false"
        assert criteria.extract_exit_signal(output) is False

    def test_extract_exit_signal_ralph_status(self):
        """Test extracting exit signal from RALPH_STATUS block."""
        criteria = CompletionCriteria()

        output = """
        RALPH_STATUS: {
            EXIT_SIGNAL: true
        }
        """
        assert criteria.extract_exit_signal(output) is True

    def test_count_completion_indicators(self):
        """Test counting completion indicators."""
        criteria = CompletionCriteria()

        output = "Task completed successfully. All done."
        count = criteria.count_completion_indicators(output)
        assert count >= 2  # "completed" and "done"

        output = "All tasks complete. Project completed."
        count = criteria.count_completion_indicators(output)
        assert count >= 4  # Strong phrases count as 2 each

        output = "Nothing here"
        count = criteria.count_completion_indicators(output)
        assert count == 0

    def test_check_tests_without_runner(self):
        """Test check_tests without validation runner."""
        criteria = CompletionCriteria()
        # Should return True if no runner (assumes tests pass)
        assert criteria.check_tests() is True

    def test_check_linter_without_runner(self):
        """Test check_linter without validation runner."""
        criteria = CompletionCriteria()
        # Should return True if no runner (assumes linter passes)
        assert criteria.check_linter() is True

    def test_check_build_without_runner(self):
        """Test check_build without validation runner."""
        criteria = CompletionCriteria()
        # Should return True if no runner (assumes build succeeds)
        assert criteria.check_build() is True


class TestCompletionCriteriaFactory:
    """Tests for CompletionCriteriaFactory."""

    def test_create_for_code_implementation(self):
        """Test creating criteria for code implementation task."""
        task = Task(
            id="test_task",
            title="Implement API endpoint",
            description="Implement a new REST API endpoint for user authentication",
            tags=["code", "api"],
        )

        criteria = CompletionCriteriaFactory.create_for_task(task, autonomy_level=4)

        assert criteria.tests_must_pass is True
        assert criteria.linter_must_pass is True
        assert criteria.build_must_succeed is True
        assert criteria.agent_exit_signal is True

    def test_create_for_documentation(self):
        """Test creating criteria for documentation task."""
        task = Task(
            id="test_task",
            title="Write documentation",
            description="Write user guide documentation for the API",
            tags=["documentation"],
        )

        criteria = CompletionCriteriaFactory.create_for_task(task, autonomy_level=3)

        assert criteria.tests_must_pass is False
        assert criteria.linter_must_pass is True  # Formatting only
        assert criteria.build_must_succeed is False

    def test_create_for_research(self):
        """Test creating criteria for research task."""
        task = Task(
            id="test_task",
            title="Research topic",
            description="Research best practices for authentication",
            tags=["research"],
        )

        criteria = CompletionCriteriaFactory.create_for_task(task, autonomy_level=2)

        assert criteria.tests_must_pass is False
        assert criteria.linter_must_pass is False
        assert criteria.build_must_succeed is False

    def test_create_for_general_task(self):
        """Test creating criteria for general task."""
        task = Task(
            id="test_task",
            title="General task",
            description="Do something",
            tags=[],
        )

        criteria = CompletionCriteriaFactory.create_for_task(task, autonomy_level=3)

        assert criteria.agent_exit_signal is True
        assert criteria.min_completion_indicators == 2

    def test_detect_task_type_code(self):
        """Test task type detection for code."""
        task = Task(
            id="test_task",
            title="Implement feature",
            description="Implement a new function for processing data",
            tags=[],
        )

        task_type = CompletionCriteriaFactory._detect_task_type(task)
        assert task_type == "code_implementation"

    def test_detect_task_type_documentation(self):
        """Test task type detection for documentation."""
        task = Task(
            id="test_task",
            title="Write docs",
            description="Write a guide for users",
            tags=[],
        )

        task_type = CompletionCriteriaFactory._detect_task_type(task)
        assert task_type == "documentation"

    def test_detect_task_type_research(self):
        """Test task type detection for research."""
        task = Task(
            id="test_task",
            title="Research",
            description="Investigate authentication methods",
            tags=[],
        )

        task_type = CompletionCriteriaFactory._detect_task_type(task)
        assert task_type == "research"
