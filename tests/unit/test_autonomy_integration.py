"""Integration tests for DTAutonomyEngine with autonomous loops."""

import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents_army.core.autonomy import DTAutonomyEngine
from agents_army.core.models import (
    ActionResult,
    Decision,
    Situation,
    Task,
)
from agents_army.core.rules import RulesLoader
from agents_army.protocol.types import AgentRole


class TestDTAutonomyEngineIntegration:
    """Integration tests for DTAutonomyEngine."""

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
    def autonomy_engine(self, mock_dt):
        """Create DTAutonomyEngine instance."""
        rules_loader = RulesLoader()
        return DTAutonomyEngine(
            rules_loader=rules_loader,
            dt=mock_dt,
        )

    @pytest.fixture
    def task(self):
        """Create test task."""
        return Task(
            id="test_task",
            title="Test task",
            description="Test description",
            assigned_agent=AgentRole.BACKEND_ARCHITECT,
        )

    @pytest.mark.asyncio
    async def test_level_4_executes_autonomous_loop(self, autonomy_engine, task, mock_dt):
        """Test level 4 decision executes autonomous loop."""
        situation = Situation(
            task=task,
            context={},
            available_agents=[AgentRole.BACKEND_ARCHITECT],
        )

        # Mock decision with level 4
        decision = Decision(
            autonomous=True,
            confidence=0.95,
            risk=0.1,
            action="execute_autonomously",
            level=4,
        )

        # Mock executor
        with patch(
            "agents_army.core.autonomous_executor.AutonomousTaskExecutor"
        ) as mock_executor_class:
            mock_executor = AsyncMock()
            mock_executor.execute_until_complete.return_value = ActionResult(
                success=True,
                action_taken="completed",
            )
            mock_executor_class.return_value = mock_executor

            result = await autonomy_engine._execute_autonomously(situation, decision)

            assert result.success is True
            mock_executor.execute_until_complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_level_3_executes_validated_loop(self, autonomy_engine, task, mock_dt):
        """Test level 3 decision executes validated loop."""
        situation = Situation(
            task=task,
            context={},
            available_agents=[AgentRole.BACKEND_ARCHITECT],
        )

        decision = Decision(
            autonomous=True,
            confidence=0.85,
            risk=0.3,
            action="execute_with_validation",
            level=3,
        )

        with patch(
            "agents_army.core.autonomous_executor.AutonomousTaskExecutor"
        ) as mock_executor_class:
            mock_executor = AsyncMock()
            mock_executor.execute_until_complete.return_value = ActionResult(
                success=True,
                action_taken="completed",
            )
            mock_executor_class.return_value = mock_executor

            result = await autonomy_engine._execute_autonomously(situation, decision)

            assert result.success is True
            # Should be called with validate_each_iteration=True
            call_kwargs = mock_executor.execute_until_complete.call_args[1]
            assert call_kwargs.get("validate_each_iteration") is True

    @pytest.mark.asyncio
    async def test_level_2_executes_simple(self, autonomy_engine, task, mock_dt):
        """Test level 2 decision executes simple execution."""
        situation = Situation(
            task=task,
            context={},
            available_agents=[AgentRole.BACKEND_ARCHITECT],
        )

        decision = Decision(
            autonomous=True,
            confidence=0.7,
            risk=0.5,
            action="execute_simple",
            level=2,
        )

        # Mock agent execution
        mock_agent = AsyncMock()
        mock_response = MagicMock()
        mock_response.payload = {"status": "completed", "result": {}}
        mock_agent.handle_message.return_value = mock_response
        mock_dt.system.get_agent.return_value = mock_agent

        result = await autonomy_engine._execute_autonomously(situation, decision)

        # Should execute once and validate
        assert mock_agent.handle_message.called

    @pytest.mark.asyncio
    async def test_level_1_escalates(self, autonomy_engine, task):
        """Test level 1 escalates to human."""
        situation = Situation(
            task=task,
            context={},
            available_agents=[AgentRole.BACKEND_ARCHITECT],
        )

        decision = Decision(
            autonomous=False,
            confidence=0.5,
            risk=0.7,
            action="escalate",
            level=1,
            escalation_reason="Low confidence",
        )

        result = await autonomy_engine._escalate_to_human(situation, decision)

        assert result.escalated is True
        assert result.success is False
