"""Tests for AutonomousTaskExecutor."""

import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents_army.core.autonomous_executor import AutonomousTaskExecutor
from agents_army.core.completion import CompletionCriteria
from agents_army.core.models import Task, TaskResult
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class TestAutonomousTaskExecutor:
    """Tests for AutonomousTaskExecutor class."""

    @pytest.fixture
    def mock_dt(self):
        """Create mock DT instance."""
        dt = MagicMock()
        dt.task_storage = MagicMock()
        dt.task_storage.project_path = tempfile.mkdtemp()
        dt.project_path = MagicMock()
        dt.project_path.name = ".dt"
        dt.project_path.parent = MagicMock()
        dt.current_project = None
        dt.system = MagicMock()
        return dt

    @pytest.fixture
    def executor(self, mock_dt):
        """Create AutonomousTaskExecutor instance."""
        return AutonomousTaskExecutor(
            dt=mock_dt,
            max_iterations=5,
            enable_circuit_breaker=True,
            enable_sessions=True,
        )

    @pytest.fixture
    def task(self):
        """Create test task."""
        return Task(
            id="test_task",
            title="Test task",
            description="Test description",
        )

    @pytest.fixture
    def completion_criteria(self):
        """Create completion criteria."""
        criteria = CompletionCriteria(
            agent_exit_signal=True,
            min_completion_indicators=2,
            min_file_changes=1,
        )
        return criteria

    @pytest.mark.asyncio
    async def test_execute_until_complete_success(self, executor, task, completion_criteria):
        """Test successful execution until completion."""
        # Mock agent response with completion signal
        mock_agent = AsyncMock()
        mock_response = AgentMessage(
            from_role=AgentRole.BACKEND_ARCHITECT,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={
                "status": "completed",
                "output": "Task completed successfully. EXIT_SIGNAL: true. All done.",
                "result": {},
            },
        )
        mock_agent.handle_message.return_value = mock_response
        mock_agent.id = "agent_123"

        executor.dt.system.get_agent.return_value = mock_agent

        # Mock file detector to return changes (so progress is detected)
        executor.file_detector.detect_changes = MagicMock(return_value=["file1.py"])

        # Disable circuit breaker for this test
        executor.enable_circuit_breaker = False
        executor.circuit_breaker = None

        result = await executor.execute_until_complete(
            task=task,
            agent_role=AgentRole.BACKEND_ARCHITECT,
            completion_criteria=completion_criteria,
        )

        assert result.success is True
        assert result.action_taken == "completed"

    @pytest.mark.asyncio
    async def test_execute_until_complete_max_iterations(self, executor, task, completion_criteria):
        """Test execution reaching max iterations."""
        # Mock agent response without completion
        mock_agent = AsyncMock()
        mock_response = AgentMessage(
            from_role=AgentRole.BACKEND_ARCHITECT,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={
                "status": "in_progress",
                "output": "Still working",
            },
        )
        mock_agent.handle_message.return_value = mock_response
        mock_agent.id = "agent_123"

        executor.dt.system.get_agent.return_value = mock_agent

        # Set low max iterations for test
        executor.max_iterations = 2

        result = await executor.execute_until_complete(
            task=task,
            agent_role=AgentRole.BACKEND_ARCHITECT,
            completion_criteria=completion_criteria,
        )

        assert result.success is False
        assert "max_iterations" in result.action_taken

    @pytest.mark.asyncio
    async def test_execute_iteration(self, executor, task):
        """Test executing a single iteration."""
        mock_agent = AsyncMock()
        mock_response = AgentMessage(
            from_role=AgentRole.BACKEND_ARCHITECT,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={
                "status": "completed",
                "output": "Done",
                "result": {},
            },
        )
        mock_agent.handle_message.return_value = mock_response
        mock_agent.id = "agent_123"

        executor.dt.system.get_agent.return_value = mock_agent

        task_result, agent_output, file_changes = await executor._execute_iteration(
            task=task,
            agent_role=AgentRole.BACKEND_ARCHITECT,
            session=None,
            iteration=1,
        )

        assert task_result is not None
        assert isinstance(agent_output, str)
        assert isinstance(file_changes, list)

    def test_extract_agent_output(self, executor):
        """Test extracting agent output from response."""
        response = AgentMessage(
            from_role=AgentRole.BACKEND_ARCHITECT,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={"output": "Test output"},
        )

        output = executor._extract_agent_output(response)
        assert output == "Test output"

    def test_extract_agent_output_fallback(self, executor):
        """Test extracting agent output with fallback."""
        response = AgentMessage(
            from_role=AgentRole.BACKEND_ARCHITECT,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={"result": "Fallback output"},
        )

        output = executor._extract_agent_output(response)
        assert output == "Fallback output"
