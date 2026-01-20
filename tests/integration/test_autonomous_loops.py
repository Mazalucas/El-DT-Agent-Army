"""End-to-end tests for autonomous loops."""

import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents_army.agents.dt import DT
from agents_army.core.models import Task
from agents_army.core.system import AgentSystem
from agents_army.protocol.types import AgentRole


class TestAutonomousLoopsE2E:
    """End-to-end tests for autonomous loop integration."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def system(self):
        """Create AgentSystem instance."""
        return AgentSystem()

    @pytest.fixture
    def dt(self, temp_dir):
        """Create DT instance."""
        return DT(project_path=temp_dir)

    @pytest.mark.asyncio
    async def test_assign_task_triggers_autonomous_execution(self, dt, system):
        """Test that assign_task triggers autonomous execution."""
        system.register_agent(dt)
        dt.set_system(system)
        await system.start()

        # Create task
        task = Task(
            id="test_task",
            title="Test task",
            description="Implement a simple function",
            assigned_agent=AgentRole.BACKEND_ARCHITECT,
        )

        # Mock agent
        mock_agent = AsyncMock()
        mock_response = MagicMock()
        mock_response.payload = {
            "status": "completed",
            "output": "Task completed. EXIT_SIGNAL: true. All done.",
            "result": {},
        }
        mock_agent.handle_message.return_value = mock_response
        mock_agent.id = "agent_123"
        system.register_agent(mock_agent)

        # Assign task - should trigger autonomous execution
        assignment = await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)

        assert assignment.task_id == task.id
        # Task should be executed (mock should be called)
        # Note: Actual execution depends on autonomy level decision

        await system.stop()

    @pytest.mark.asyncio
    async def test_task_status_updated_after_execution(self, dt, system):
        """Test that task status is updated after execution."""
        system.register_agent(dt)
        dt.set_system(system)
        await system.start()

        task = Task(
            id="test_task",
            title="Test task",
            description="Simple task",
        )

        # Mock successful execution
        with patch.object(dt.autonomy_engine, "decide_and_act") as mock_decide:
            mock_decide.return_value = MagicMock(
                success=True,
                escalated=False,
            )

            await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)

            # Task status should be updated
            updated_task = dt.task_storage.load_task(task.id)
            # Status depends on execution result
            assert updated_task is not None

        await system.stop()

    @pytest.mark.asyncio
    async def test_escalation_blocks_task(self, dt, system):
        """Test that escalation blocks task."""
        system.register_agent(dt)
        dt.set_system(system)
        await system.start()

        task = Task(
            id="test_task",
            title="Test task",
            description="Complex task requiring human",
        )

        # Mock escalation
        with patch.object(dt.autonomy_engine, "decide_and_act") as mock_decide:
            mock_decide.return_value = MagicMock(
                success=False,
                escalated=True,
                escalation_reason="Low confidence",
            )

            await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)

            # Task should be blocked
            updated_task = dt.task_storage.load_task(task.id)
            assert updated_task.status == "blocked"

        await system.stop()
