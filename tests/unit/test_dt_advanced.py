"""Unit tests for advanced DT functionalities."""

import pytest

from agents_army.agents.dt import DT
from agents_army.core.agent import LLMProvider
from agents_army.core.models import (
    AgentConflict,
    ConflictResolution,
    Task,
    TaskResult,
)
from agents_army.protocol.types import AgentRole


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    async def generate(self, prompt: str, **kwargs):
        """Generate mock response."""
        if "synthesize" in prompt.lower():
            return "Synthesized result combining all agent outputs"
        elif "resolve" in prompt.lower() or "conflict" in prompt.lower():
            return "Resolution: Choose approach A as it aligns best with project goals"
        elif "decompose" in prompt.lower():
            return """[
                {"title": "Subtask 1", "description": "First part", "priority": 5, "tags": ["tag1"], "dependencies": []},
                {"title": "Subtask 2", "description": "Second part", "priority": 4, "tags": ["tag2"], "dependencies": ["Subtask 1"]}
            ]"""
        return "Mock response"


class TestDTSynthesizeResults:
    """Test synthesize_results functionality."""

    @pytest.mark.asyncio
    async def test_synthesize_results_success(self):
        """Test synthesizing successful results."""
        dt = DT(llm_provider=MockLLMProvider())

        task_results = [
            TaskResult(
                task_id="task_001",
                status="completed",
                result={"output": "Result 1"},
                quality_score=0.8,
            ),
            TaskResult(
                task_id="task_001",
                status="completed",
                result={"output": "Result 2"},
                quality_score=0.9,
            ),
        ]

        synthesized = await dt.synthesize_results(task_results)

        assert synthesized.task_id == "task_001"
        assert synthesized.status == "completed"
        assert "synthesized" in synthesized.result
        assert abs(synthesized.quality_score - 0.85) < 0.01  # Average of 0.8 and 0.9

    @pytest.mark.asyncio
    async def test_synthesize_results_partial(self):
        """Test synthesizing partial results."""
        dt = DT(llm_provider=MockLLMProvider())

        task_results = [
            TaskResult(
                task_id="task_001",
                status="completed",
                result={"output": "Result 1"},
            ),
            TaskResult(
                task_id="task_001",
                status="failed",
                result={},
                error="Error occurred",
            ),
        ]

        synthesized = await dt.synthesize_results(task_results)

        assert synthesized.status == "partial"

    @pytest.mark.asyncio
    async def test_synthesize_results_empty(self):
        """Test synthesizing empty results raises error."""
        dt = DT(llm_provider=MockLLMProvider())

        with pytest.raises(ValueError):
            await dt.synthesize_results([])


class TestDTResolveConflict:
    """Test resolve_conflict functionality."""

    @pytest.mark.asyncio
    async def test_resolve_conflict(self):
        """Test resolving a conflict."""
        dt = DT(llm_provider=MockLLMProvider())

        conflict = AgentConflict(
            conflict_id="conflict_001",
            task_id="task_001",
            conflicting_agents=[AgentRole.BACKEND_ARCHITECT, AgentRole.FRONTEND_DEVELOPER],
            conflict_type="approach",
            description="Disagreement on API design approach",
            agent_opinions={
                AgentRole.BACKEND_ARCHITECT: {"approach": "REST API"},
                AgentRole.FRONTEND_DEVELOPER: {"approach": "GraphQL"},
            },
            severity="medium",
        )

        resolution = await dt.resolve_conflict(conflict)

        assert resolution.conflict_id == "conflict_001"
        assert resolution.resolved_by == AgentRole.DT
        assert resolution.success is True
        assert resolution.resolution_type in ["merge", "choose_one", "compromise", "escalate"]
        assert "description" in resolution.chosen_approach


class TestTaskDecomposer:
    """Test TaskDecomposer functionality."""

    @pytest.mark.asyncio
    async def test_decompose_task(self):
        """Test task decomposition."""
        dt = DT(llm_provider=MockLLMProvider())

        task = Task(
            id="task_001",
            title="Complex Task",
            description="This is a complex task that needs decomposition. It has multiple parts.",
            priority=5,
            tags=["complex"],
        )

        subtasks = await dt.task_decomposer.decompose(task, max_subtasks=3)

        assert len(subtasks) > 0
        assert len(subtasks) <= 3
        assert all(isinstance(st, Task) for st in subtasks)
        assert all(st.metadata.get("parent_task") == task.id for st in subtasks)

    def test_estimate_complexity(self):
        """Test complexity estimation."""
        dt = DT(llm_provider=MockLLMProvider())

        simple_task = Task(
            id="task_001",
            title="Simple Task",
            description="Short description",
        )

        complex_task = Task(
            id="task_002",
            title="Complex Task",
            description="A" * 600,  # Long description
            dependencies=["dep1", "dep2", "dep3", "dep4"],
        )

        assert dt.task_decomposer.estimate_complexity(simple_task) == "low"
        assert dt.task_decomposer.estimate_complexity(complex_task) == "high"


class TestTaskScheduler:
    """Test TaskScheduler functionality."""

    def test_schedule_tasks(self):
        """Test task scheduling."""
        dt = DT(llm_provider=MockLLMProvider())

        task1 = Task(
            id="task_001",
            title="Task 1",
            description="First task",
            priority=5,
        )

        task2 = Task(
            id="task_002",
            title="Task 2",
            description="Second task",
            priority=3,
            dependencies=["task_001"],
        )

        task3 = Task(
            id="task_003",
            title="Task 3",
            description="Third task",
            priority=4,
        )

        tasks = [task2, task3, task1]  # Out of order
        scheduled = dt.task_scheduler.schedule_tasks(tasks)

        # Task 1 should come before task 2 (dependency)
        task1_idx = next(i for i, t in enumerate(scheduled) if t.id == "task_001")
        task2_idx = next(i for i, t in enumerate(scheduled) if t.id == "task_002")
        assert task1_idx < task2_idx

    def test_find_critical_path(self):
        """Test finding critical path."""
        dt = DT(llm_provider=MockLLMProvider())

        task1 = Task(id="task_001", title="Task 1", description="Task 1")
        task2 = Task(
            id="task_002",
            title="Task 2",
            description="Task 2",
            dependencies=["task_001"],
        )
        task3 = Task(
            id="task_003",
            title="Task 3",
            description="Task 3",
            dependencies=["task_002"],
        )

        tasks = [task1, task2, task3]
        critical_path = dt.task_scheduler.find_critical_path(tasks)

        assert "task_001" in critical_path
        assert "task_002" in critical_path
        assert "task_003" in critical_path

    def test_estimate_duration(self):
        """Test duration estimation."""
        dt = DT(llm_provider=MockLLMProvider())

        task = Task(
            id="task_001",
            title="Task",
            description="A" * 500,  # Long description
            priority=5,
            dependencies=["dep1", "dep2"],
        )

        duration = dt.task_scheduler.estimate_duration(task)
        assert duration.total_seconds() > 0
