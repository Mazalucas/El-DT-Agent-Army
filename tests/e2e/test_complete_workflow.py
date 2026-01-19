"""End-to-end tests for complete workflows."""

import asyncio
import tempfile
from pathlib import Path

import pytest

from agents_army import (
    BackendArchitect,
    DT,
    InMemoryBackend,
    MarketingStrategist,
    MemoryAgent,
    QATester,
    Researcher,
)
from agents_army.core.agent import LLMProvider
from agents_army.core.system import AgentSystem
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType, Priority


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for E2E tests."""

    def __init__(self):
        self.responses = {}
        self.call_count = 0

    async def generate(self, prompt: str, **kwargs):
        """Generate mock response."""
        self.call_count += 1

        if "PRD" in prompt or "parse" in prompt.lower():
            return '''[
  {
    "title": "Research market trends",
    "description": "Research current market trends for AI agents",
    "priority": 5,
    "tags": ["research", "market"]
  },
  {
    "title": "Design backend architecture",
    "description": "Design scalable backend architecture",
    "priority": 4,
    "tags": ["engineering", "architecture"]
  },
  {
    "title": "Create marketing strategy",
    "description": "Develop comprehensive marketing strategy",
    "priority": 4,
    "tags": ["marketing", "strategy"]
  }
]'''
        elif "architecture" in prompt.lower() or "design" in prompt.lower():
            return """Architecture Design:
- API Layer: RESTful API with GraphQL support
- Business Logic: Microservices architecture
- Database: PostgreSQL with Redis cache
- Scalability: Horizontal scaling with load balancer"""
        elif "marketing" in prompt.lower() or "strategy" in prompt.lower():
            return """Marketing Strategy:
- Target Audience: Developers and tech companies
- Channels: LinkedIn, Twitter, GitHub
- Content: Technical blogs, case studies
- Budget: $10,000/month"""
        elif "research" in prompt.lower():
            return "Research findings: AI agents are becoming increasingly important in software development..."
        elif "test" in prompt.lower() or "qa" in prompt.lower():
            return "Test Plan:\n1. Unit tests\n2. Integration tests\n3. E2E tests\n4. Performance tests"

        return f"Mock response {self.call_count}"


class TestCompleteWorkflow:
    """Test complete end-to-end workflows."""

    @pytest.mark.asyncio
    async def test_complete_project_workflow(self):
        """Test complete project workflow from initialization to completion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Setup system
            system = AgentSystem()
            llm = MockLLMProvider()

            # 2. Create agents
            prd_path = Path(tmpdir) / "docs" / "prd.txt"
            dt = DT(project_path=tmpdir, prd_path=str(prd_path), llm_provider=llm)
            researcher = Researcher(llm_provider=llm)
            backend_architect = BackendArchitect(llm_provider=llm)
            marketing_strategist = MarketingStrategist(llm_provider=llm)
            qa_tester = QATester(llm_provider=llm)
            memory_agent = MemoryAgent(backend=InMemoryBackend())

            # 3. Register agents
            system.register_agent(dt)
            system.register_agent(researcher)
            system.register_agent(backend_architect)
            system.register_agent(marketing_strategist)
            system.register_agent(qa_tester)
            system.register_agent(memory_agent)

            dt.set_system(system)

            # 4. Start system
            await system.start()

            # 5. Initialize project
            project = await dt.initialize_project(
                project_name="E2E Test Project",
                description="A complete test project",
                rules=["Always test", "Document everything"],
            )

            assert project.name == "E2E Test Project"

            # 6. Create and parse PRD
            prd_file = Path(tmpdir) / "docs" / "prd.txt"
            prd_file.write_text(
                """# Project PRD

## Overview
Build a multi-agent system for project management.

## Features
1. Research market trends
2. Design backend architecture
3. Create marketing strategy
"""
            )

            tasks = await dt.parse_prd()
            assert len(tasks) > 0

            # 7. Get next task and assign
            next_task = await dt.get_next_task()
            assert next_task is not None

            # Assign to appropriate agent based on task
            if "research" in next_task.title.lower():
                assignment = await dt.assign_task(next_task, AgentRole.RESEARCHER)
                assert assignment.agent_role == AgentRole.RESEARCHER

                # Send task to researcher
                message = AgentMessage(
                    from_role=AgentRole.DT,
                    to_role=AgentRole.RESEARCHER,
                    type=MessageType.TASK_REQUEST,
                    payload={
                        "query": next_task.description,
                        "task_id": next_task.id,
                    },
                )

                await system.send_message(message)
                await asyncio.sleep(0.2)

            # 8. Store in memory
            await memory_agent.store(
                key=f"task_{next_task.id}",
                value=next_task.to_dict(),
                memory_type="task",
            )

            # 9. Update task status
            await dt.update_task_status(next_task.id, "done")

            # 10. Verify task is done
            updated_task = dt.task_storage.load_task(next_task.id)
            assert updated_task is not None
            assert updated_task.status == "done"

            # 11. Stop system
            await system.stop()

    @pytest.mark.asyncio
    async def test_multi_agent_coordination(self):
        """Test coordination between multiple agents."""
        system = AgentSystem()
        llm = MockLLMProvider()

        # Create agents
        dt = DT(llm_provider=llm)
        researcher = Researcher(llm_provider=llm)
        backend_architect = BackendArchitect(llm_provider=llm)

        # Register
        system.register_agent(dt)
        system.register_agent(researcher)
        system.register_agent(backend_architect)
        dt.set_system(system)

        await system.start()

        # DT sends research task to researcher
        research_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"query": "Best practices for API design", "task_id": "task_001"},
            metadata={"priority": Priority.HIGH},
        )

        await system.send_message(research_message)
        await asyncio.sleep(0.2)

        # Verify researcher received message
        researcher_messages = researcher.get_message_history()
        assert len(researcher_messages) == 1

        # DT sends architecture task to backend architect
        arch_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.BACKEND_ARCHITECT,
            type=MessageType.TASK_REQUEST,
            payload={
                "requirements": {"type": "REST API", "scale": "10000 users"},
                "task_id": "task_002",
            },
        )

        await system.send_message(arch_message)
        await asyncio.sleep(0.2)

        # Verify backend architect received message
        arch_messages = backend_architect.get_message_history()
        assert len(arch_messages) == 1

        await system.stop()

    @pytest.mark.asyncio
    async def test_memory_integration(self):
        """Test memory system integration with agents."""
        system = AgentSystem()
        memory_agent = MemoryAgent(backend=InMemoryBackend())

        system.register_agent(memory_agent)
        await system.start()

        # Store memory
        store_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.MEMORY,
            type=MessageType.MEMORY_STORE,
            payload={
                "key": "user_preference",
                "value": "User prefers dark mode",
                "tags": ["user", "preference"],
                "memory_type": "user",
            },
        )

        await system.send_message(store_message)
        await asyncio.sleep(0.1)

        # Query memory
        query_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.MEMORY,
            type=MessageType.MEMORY_QUERY,
            payload={"key": "user_preference"},
        )

        await system.send_message(query_message)
        await asyncio.sleep(0.1)

        # Verify memory was stored and retrieved
        retrieved = await memory_agent.retrieve("user_preference")
        assert retrieved == "User prefers dark mode"

        await system.stop()
