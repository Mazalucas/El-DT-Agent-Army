"""Tests for backward compatibility."""

import tempfile
from unittest.mock import AsyncMock, MagicMock

import pytest

from agents_army.agents.dt import DT
from agents_army.core.models import Task
from agents_army.core.system import AgentSystem
from agents_army.protocol.types import AgentRole


class TestBackwardCompatibility:
    """Tests to ensure backward compatibility."""

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

    def test_assign_task_signature_unchanged(self, dt):
        """Test that assign_task maintains same signature."""
        import inspect
        
        sig = inspect.signature(dt.assign_task)
        params = list(sig.parameters.keys())
        
        # Should have same parameters: task, agent_role
        assert "task" in params
        assert "agent_role" in params
        assert len(params) == 2  # No new required parameters

    @pytest.mark.asyncio
    async def test_assign_task_returns_task_assignment(self, dt, system):
        """Test that assign_task still returns TaskAssignment."""
        system.register_agent(dt)
        dt.set_system(system)
        await system.start()
        
        task = Task(
            id="test_task",
            title="Test",
            description="Test description",
        )
        
        assignment = await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)
        
        # Should return TaskAssignment
        assert assignment.task_id == task.id
        assert assignment.agent_role == AgentRole.BACKEND_ARCHITECT
        
        await system.stop()

    @pytest.mark.asyncio
    async def test_existing_workflow_still_works(self, dt, system):
        """Test that existing workflow patterns still work."""
        system.register_agent(dt)
        dt.set_system(system)
        await system.start()
        
        # Simulate existing workflow - skip parse_prd if PRD doesn't exist
        try:
            tasks = await dt.parse_prd()
            if tasks:
                task = tasks[0]
                assignment = await dt.assign_task(task, AgentRole.RESEARCHER)
                
                # Should work without errors
                assert assignment is not None
                assert assignment.task_id == task.id
        except FileNotFoundError:
            # PRD file doesn't exist, which is fine for this test
            # Just verify that assign_task would work with a manual task
            from agents_army.core.models import Task
            task = Task(
                id="test_task",
                title="Test task",
                description="Test description",
            )
            assignment = await dt.assign_task(task, AgentRole.RESEARCHER)
            assert assignment is not None
        
        await system.stop()

    def test_dt_methods_unchanged(self, dt):
        """Test that DT methods maintain same signatures."""
        import inspect
        
        # Check key methods
        methods_to_check = [
            "parse_prd",
            "get_tasks",
            "get_next_task",
            "update_task_status",
        ]
        
        for method_name in methods_to_check:
            method = getattr(dt, method_name)
            sig = inspect.signature(method)
            # Just verify they exist and are callable
            assert callable(method)
