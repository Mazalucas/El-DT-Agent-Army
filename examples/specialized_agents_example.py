"""
Example of using specialized agents.

This example demonstrates:
- Creating specialized agents
- Registering them with the system
- Sending tasks to specialized agents
- Coordinating through El DT
"""

import asyncio
from typing import Any

from agents_army import (
    BackendArchitect,
    DT,
    MarketingStrategist,
    QATester,
    Researcher,
)
from agents_army.core.agent import LLMProvider
from agents_army.core.system import AgentSystem
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType, Priority


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for example."""

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate mock response."""
        if "research" in prompt.lower() or "query" in prompt.lower():
            return "Research findings: AI agents are becoming increasingly important..."
        elif "architecture" in prompt.lower() or "design" in prompt.lower():
            return "Architecture Design:\n- API Layer\n- Business Logic\n- Database Layer"
        elif "marketing" in prompt.lower() or "strategy" in prompt.lower():
            return "Marketing Strategy:\n- Target: Tech professionals\n- Channels: LinkedIn, Twitter"
        elif "test" in prompt.lower() or "qa" in prompt.lower():
            return "Test Plan:\n1. Unit tests\n2. Integration tests\n3. E2E tests"
        return "Mock response"


async def main():
    """Main example function."""
    print("Specialized Agents Example\n")

    # 1. Create agent system
    print("1. Creating agent system...")
    system = AgentSystem()
    print("   System created\n")

    # 2. Create specialized agents
    print("2. Creating specialized agents...")
    llm = MockLLMProvider()

    researcher = Researcher(llm_provider=llm)
    backend_architect = BackendArchitect(llm_provider=llm)
    marketing_strategist = MarketingStrategist(llm_provider=llm)
    qa_tester = QATester(llm_provider=llm)
    dt = DT(llm_provider=llm)

    print(f"   Created: {researcher.name} ({researcher.role.value})")
    print(f"   Created: {backend_architect.name} ({backend_architect.role.value})")
    print(f"   Created: {marketing_strategist.name} ({marketing_strategist.role.value})")
    print(f"   Created: {qa_tester.name} ({qa_tester.role.value})")
    print(f"   Created: {dt.name} ({dt.role.value})\n")

    # 3. Register agents
    print("3. Registering agents...")
    system.register_agent(researcher)
    system.register_agent(backend_architect)
    system.register_agent(marketing_strategist)
    system.register_agent(qa_tester)
    system.register_agent(dt)
    dt.set_system(system)
    print("   All agents registered\n")

    # 4. Start system
    print("4. Starting system...")
    await system.start()
    print("   System started\n")

    # 5. Send research task
    print("5. Sending research task to Researcher...")
    research_message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.RESEARCHER,
        type=MessageType.TASK_REQUEST,
        payload={
            "query": "Best practices for multi-agent systems",
            "task_id": "task_research_001",
        },
        metadata={"priority": Priority.HIGH},
    )

    await system.send_message(research_message)
    await asyncio.sleep(0.2)
    print("   Research task sent\n")

    # 6. Send architecture design task
    print("6. Sending architecture design task to Backend Architect...")
    arch_message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.BACKEND_ARCHITECT,
        type=MessageType.TASK_REQUEST,
        payload={
            "requirements": {
                "type": "REST API",
                "scale": "10000 users",
                "features": ["auth", "data storage"],
            },
            "task_id": "task_arch_001",
        },
    )

    await system.send_message(arch_message)
    await asyncio.sleep(0.2)
    print("   Architecture task sent\n")

    # 7. Send marketing strategy task
    print("7. Sending marketing strategy task to Marketing Strategist...")
    marketing_message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.MARKETING_STRATEGIST,
        type=MessageType.TASK_REQUEST,
        payload={
            "context": {
                "product": "Agents_Army Framework",
                "target_audience": "Developers",
                "goal": "Increase adoption",
            },
            "task_id": "task_marketing_001",
        },
    )

    await system.send_message(marketing_message)
    await asyncio.sleep(0.2)
    print("   Marketing task sent\n")

    # 8. Send QA validation task
    print("8. Sending QA validation task to QA Tester...")
    qa_message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.QA_TESTER,
        type=MessageType.TASK_REQUEST,
        payload={
            "output": "Login successful",
            "expected": "Login successful",
            "task_id": "task_qa_001",
        },
    )

    await system.send_message(qa_message)
    await asyncio.sleep(0.2)
    print("   QA task sent\n")

    # 9. Check agent statuses
    print("9. Checking agent statuses...")
    for agent in system.get_all_agents():
        print(f"   {agent.name}: {agent.status} ({len(agent.get_message_history())} messages)")

    print()

    # 10. Stop system
    print("10. Stopping system...")
    await system.stop()
    print("   System stopped\n")

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
