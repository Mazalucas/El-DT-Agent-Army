"""Unit tests for El DT."""

import tempfile
from pathlib import Path

import pytest

from typing import Any

import pytest

from agents_army.agents.dt import DT
from agents_army.core.agent import LLMProvider
from agents_army.core.models import Task
from agents_army.protocol.types import AgentRole


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    def __init__(self):
        self.responses = {}

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate mock response."""
        if "PRD" in prompt or "parse" in prompt.lower():
            return '[{"title": "Test Task", "description": "Test description", "priority": 3, "tags": []}]'
        return "Mock response"

    def set_response(self, prompt: str, response: str):
        """Set response for a prompt."""
        self.responses[prompt] = response


class TestDT:
    """Test DT class."""

    def test_create_dt(self):
        """Test creating El DT."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)

            assert dt.name == "El DT"
            assert dt.role == AgentRole.DT
            assert dt.project_path == Path(tmpdir)

    @pytest.mark.asyncio
    async def test_initialize_project(self):
        """Test project initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)

            project = await dt.initialize_project(
                project_name="Test Project",
                description="Test description",
                rules=["Rule 1", "Rule 2"],
            )

            assert project.name == "Test Project"
            assert project.description == "Test description"
            assert len(project.rules) == 2
            assert dt.current_project == project

            # Check directories created
            assert (Path(tmpdir) / "docs").exists()
            assert (Path(tmpdir) / "tasks").exists()
            assert (Path(tmpdir) / "rules").exists()

    @pytest.mark.asyncio
    async def test_parse_prd(self):
        """Test parsing PRD."""
        with tempfile.TemporaryDirectory() as tmpdir:
            prd_file = Path(tmpdir) / "docs" / "prd.txt"
            dt = DT(project_path=tmpdir, prd_path=str(prd_file), llm_provider=MockLLMProvider())
            await dt.initialize_project("Test", "Test")

            # Create PRD file
            prd_file.write_text("# Test PRD\n\nFeature 1: Implement X\nFeature 2: Implement Y")

            tasks = await dt.parse_prd()

            assert len(tasks) > 0
            assert tasks[0].title == "Test Task"

    @pytest.mark.asyncio
    async def test_get_tasks(self):
        """Test getting tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)
            await dt.initialize_project("Test", "Test")

            # Create a task
            task = Task(
                id="task_001",
                title="Test Task",
                description="Test description",
                status="pending",
            )
            dt.task_storage.save_task(task)

            tasks = await dt.get_tasks()
            assert len(tasks) == 1
            assert tasks[0].id == "task_001"

    @pytest.mark.asyncio
    async def test_get_next_task(self):
        """Test getting next task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)
            await dt.initialize_project("Test", "Test")

            # Create tasks with different priorities
            task1 = Task(
                id="task_001",
                title="Low Priority",
                description="Test",
                priority=1,
                status="pending",
            )
            task2 = Task(
                id="task_002",
                title="High Priority",
                description="Test",
                priority=5,
                status="pending",
            )

            dt.task_storage.save_task(task1)
            dt.task_storage.save_task(task2)

            next_task = await dt.get_next_task()
            assert next_task is not None
            assert next_task.priority == 5  # Should get highest priority

    @pytest.mark.asyncio
    async def test_assign_task(self):
        """Test assigning task to agent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)
            await dt.initialize_project("Test", "Test")

            task = Task(
                id="task_001",
                title="Test Task",
                description="Test",
                status="pending",
            )
            dt.task_storage.save_task(task)

            assignment = await dt.assign_task(task, AgentRole.RESEARCHER)

            assert assignment.task_id == task.id
            assert assignment.agent_role == AgentRole.RESEARCHER
            assert task.assigned_agent == AgentRole.RESEARCHER
            assert task.status == "in-progress"

    @pytest.mark.asyncio
    async def test_update_task_status(self):
        """Test updating task status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dt = DT(project_path=tmpdir)
            await dt.initialize_project("Test", "Test")

            task = Task(
                id="task_001",
                title="Test Task",
                description="Test",
                status="pending",
            )
            dt.task_storage.save_task(task)

            updated = await dt.update_task_status("task_001", "done")

            assert updated.status == "done"
            assert updated.id == task.id
