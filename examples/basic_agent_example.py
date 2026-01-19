"""
Basic example of using Agents_Army agents.

This example demonstrates:
- Creating agents
- Registering agents
- Sending messages between agents
"""

import asyncio
from agents_army.core.agent import Agent, AgentConfig
from agents_army.core.system import AgentSystem
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType, Priority


class ResearcherAgent(Agent):
    """Simple researcher agent implementation."""

    async def _process_message(self, message: AgentMessage):
        """Process research task."""
        print(f"[{self.name}] Processing research task: {message.payload.get('task_id')}")

        # Simulate research
        await asyncio.sleep(0.1)

        # Create response
        response = AgentMessage(
            from_role=self.role,
            to_role=message.from_role,
            type=MessageType.TASK_RESPONSE,
            payload={
                "task_id": message.payload.get("task_id"),
                "status": "completed",
                "result": {
                    "content": "Research completed successfully",
                    "sources": ["source1", "source2", "source3"],
                },
            },
            reply_to=message.id,
        )

        return response


async def main():
    """Main example function."""
    print("Agents_Army Agent System Example\n")

    # 1. Create agent system
    print("1. Creating agent system...")
    system = AgentSystem()
    print("   System created\n")

    # 2. Create agents
    print("2. Creating agents...")
    researcher_config = AgentConfig(
        name="Researcher",
        role=AgentRole.RESEARCHER,
        goal="Research topics thoroughly",
        backstory="You are an expert researcher",
        model="gpt-4",
        verbose=True,
    )

    researcher = ResearcherAgent(researcher_config)
    print(f"   Created: {researcher.name} ({researcher.role.value})\n")

    # 3. Register agents
    print("3. Registering agents...")
    system.register_agent(researcher)
    print(f"   Registered: {researcher.name}\n")

    # 4. Start system
    print("4. Starting system...")
    await system.start()
    print("   System started\n")

    # 5. Send message
    print("5. Sending task request...")
    message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.RESEARCHER,
        type=MessageType.TASK_REQUEST,
        payload={
            "task_id": "task_001",
            "description": "Research best practices for AI agents",
            "parameters": {"topic": "AI agents", "depth": "medium"},
        },
        metadata={"priority": Priority.HIGH},
    )

    await system.send_message(message)
    await asyncio.sleep(0.2)  # Wait for processing
    print("   Message sent\n")

    # 6. Check agent status
    print("6. Checking agent status...")
    retrieved_agent = system.get_agent(AgentRole.RESEARCHER)
    if retrieved_agent:
        print(f"   Agent: {retrieved_agent.name}")
        print(f"   Status: {retrieved_agent.status}")
        print(f"   Available: {retrieved_agent.is_available}")
        print(f"   Messages handled: {len(retrieved_agent.get_message_history())}\n")

    # 7. Stop system
    print("7. Stopping system...")
    await system.stop()
    print("   System stopped\n")

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
