"""
Complete Application Example - Agents_Army

This example demonstrates a complete application using Agents_Army:
- Project initialization
- Task generation from PRD
- Multi-agent coordination
- Memory integration
- Tool usage
- Complete workflow execution
"""

import asyncio
import tempfile
from pathlib import Path
from typing import Any

from agents_army import (
    BackendArchitect,
    DT,
    InMemoryBackend,
    MarketingStrategist,
    MemoryAgent,
    QATester,
    Researcher,
    create_default_tools,
)
from agents_army.core.agent import LLMProvider
from agents_army.core.system import AgentSystem
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType, Priority


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for complete example."""

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate mock response based on prompt."""
        if "PRD" in prompt or "parse" in prompt.lower():
            return '''[
  {
    "title": "Research AI agent frameworks",
    "description": "Research existing AI agent frameworks and best practices",
    "priority": 5,
    "tags": ["research", "ai"]
  },
  {
    "title": "Design system architecture",
    "description": "Design scalable architecture for multi-agent system",
    "priority": 5,
    "tags": ["engineering", "architecture"]
  },
  {
    "title": "Develop marketing strategy",
    "description": "Create comprehensive marketing strategy for launch",
    "priority": 4,
    "tags": ["marketing"]
  },
  {
    "title": "Create test suite",
    "description": "Develop comprehensive test suite",
    "priority": 3,
    "tags": ["testing", "qa"]
  }
]'''
        elif "architecture" in prompt.lower():
            return """Architecture Design:
Components:
- API Gateway
- Agent Orchestrator
- Message Bus
- Memory System
- Tool Registry

Technology Stack:
- Python 3.10+
- FastAPI for API
- PostgreSQL for persistence
- Redis for caching
- Docker for deployment"""
        elif "marketing" in prompt.lower():
            return """Marketing Strategy:
Target Audience: Developers and tech companies
Channels:
- Developer communities (Reddit, HackerNews)
- Technical blogs
- GitHub presence
- Conference talks

Content Strategy:
- Technical tutorials
- Case studies
- Open source contributions"""
        elif "research" in prompt.lower():
            return """Research Findings:
1. LangChain: Popular but complex
2. AutoGPT: Good for autonomous agents
3. CrewAI: Excellent for multi-agent coordination
4. Best Practice: Clear role definitions and communication protocols"""
        elif "test" in prompt.lower():
            return """Test Plan:
1. Unit Tests: >80% coverage
2. Integration Tests: All agent interactions
3. E2E Tests: Complete workflows
4. Performance Tests: Load and stress testing"""
        return "Mock response"


async def main():
    """Main application example."""
    print("=" * 60)
    print("Agents_Army - Complete Application Example")
    print("=" * 60)
    print()

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Initialize System
        print("1. Initializing Agent System...")
        system = AgentSystem()
        llm = MockLLMProvider()
        tool_registry = create_default_tools(llm_provider=llm)

        # 2. Create Agents
        print("2. Creating specialized agents...")
        prd_path = Path(tmpdir) / "docs" / "prd.txt"
        dt = DT(project_path=tmpdir, prd_path=str(prd_path), llm_provider=llm)
        researcher = Researcher(llm_provider=llm)
        backend_architect = BackendArchitect(llm_provider=llm)
        marketing_strategist = MarketingStrategist(llm_provider=llm)
        qa_tester = QATester(llm_provider=llm)
        memory_agent = MemoryAgent(backend=InMemoryBackend())

        # Register tools with agents
        for tool in tool_registry.get_all_tools():
            researcher.register_tool(tool.name, tool)

        print(f"   Created: {dt.name}")
        print(f"   Created: {researcher.name}")
        print(f"   Created: {backend_architect.name}")
        print(f"   Created: {marketing_strategist.name}")
        print(f"   Created: {qa_tester.name}")
        print(f"   Created: {memory_agent.name}")
        print(f"   Registered {tool_registry.count_tools()} tools")
        print()

        # 3. Register Agents
        print("3. Registering agents with system...")
        system.register_agent(dt)
        system.register_agent(researcher)
        system.register_agent(backend_architect)
        system.register_agent(marketing_strategist)
        system.register_agent(qa_tester)
        system.register_agent(memory_agent)
        dt.set_system(system)
        print("   All agents registered\n")

        # 4. Start System
        print("4. Starting system...")
        await system.start()
        print("   System started\n")

        # 5. Initialize Project
        print("5. Initializing project...")
        project = await dt.initialize_project(
            project_name="Agents_Army Framework",
            description="A complete multi-agent framework for project management",
            rules=[
                "Always test code",
                "Document all decisions",
                "Follow best practices",
            ],
        )
        print(f"   Project: {project.name}")
        print(f"   Path: {project.path}\n")

        # 6. Create PRD
        print("6. Creating Product Requirements Document...")
        prd_content = """# Agents_Army Framework - PRD

## Overview
Build a comprehensive multi-agent framework for project management.

## Requirements
1. Research existing frameworks and best practices
2. Design scalable system architecture
3. Develop marketing strategy for launch
4. Create comprehensive test suite

## Success Criteria
- Framework is easy to use
- Supports multiple agent types
- Has good documentation
- Includes examples
"""
        prd_file = Path(tmpdir) / "docs" / "prd.txt"
        prd_file.write_text(prd_content)
        print(f"   PRD created at: {prd_file}\n")

        # 7. Parse PRD and Generate Tasks
        print("7. Parsing PRD and generating tasks...")
        tasks = await dt.parse_prd()
        print(f"   Generated {len(tasks)} tasks:")
        for task in tasks:
            print(f"     - {task.title} (Priority: {task.priority})")
        print()

        # 8. Execute Tasks with Agents
        print("8. Executing tasks with specialized agents...")
        for task in tasks:
            print(f"\n   Processing: {task.title}")

            # Determine which agent to use
            if "research" in task.title.lower():
                agent_role = AgentRole.RESEARCHER
                payload = {"query": task.description, "task_id": task.id}
            elif "architecture" in task.title.lower() or "design" in task.title.lower():
                agent_role = AgentRole.BACKEND_ARCHITECT
                payload = {
                    "requirements": {"description": task.description},
                    "task_id": task.id,
                }
            elif "marketing" in task.title.lower():
                agent_role = AgentRole.MARKETING_STRATEGIST
                payload = {
                    "context": {"product": "Agents_Army", "description": task.description},
                    "task_id": task.id,
                }
            elif "test" in task.title.lower():
                agent_role = AgentRole.QA_TESTER
                payload = {"feature_spec": {"name": task.title, "description": task.description}, "task_id": task.id}
            else:
                continue

            # Assign task
            await dt.assign_task(task, agent_role)

            # Send message to agent
            message = AgentMessage(
                from_role=AgentRole.DT,
                to_role=agent_role,
                type=MessageType.TASK_REQUEST,
                payload=payload,
                metadata={"priority": Priority.HIGH if task.priority >= 4 else Priority.NORMAL},
            )

            await system.send_message(message)
            await asyncio.sleep(0.3)  # Wait for processing

            # Store in memory
            await memory_agent.store(
                key=f"task_{task.id}",
                value={"task": task.title, "status": "in_progress"},
                memory_type="task",
            )

            # Update task status
            await dt.update_task_status(task.id, "done")
            print(f"     [OK] Completed")

        print()

        # 9. Query Memory
        print("9. Querying memory system...")
        all_tasks = await memory_agent.search("task")
        # Filter by memory_type manually
        task_memories = [mem for mem in all_tasks if mem.memory_type == "task"]
        print(f"   Found {len(task_memories)} task memories")
        for mem in task_memories[:3]:
            print(f"     - {mem.key}: {mem.value}")
        print()

        # 10. Get Project Status
        print("10. Getting project status...")
        status_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.DT,
            type=MessageType.STATUS_QUERY,
            payload={"query": "status"},
        )

        await system.send_message(status_message)
        await asyncio.sleep(0.2)

        all_tasks = await dt.get_tasks()
        pending = [t for t in all_tasks if t.status == "pending"]
        done = [t for t in all_tasks if t.status == "done"]

        print(f"   Total tasks: {len(all_tasks)}")
        print(f"   Pending: {len(pending)}")
        print(f"   Done: {len(done)}")
        print()

        # 11. Agent Statistics
        print("11. Agent statistics...")
        for agent in system.get_all_agents():
            messages = agent.get_message_history()
            print(f"   {agent.name}: {len(messages)} messages processed, status: {agent.status}")
        print()

        # 12. Stop System
        print("12. Stopping system...")
        await system.stop()
        print("   System stopped\n")

    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
