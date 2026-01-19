"""
Basic example of using the Agents_Army protocol.

This example demonstrates:
- Creating messages
- Serializing/deserializing
- Routing messages between agents
"""

import asyncio
from agents_army.protocol import (
    AgentMessage,
    AgentRole,
    MessageRouter,
    MessageSerializer,
    MessageType,
    Priority,
)


async def researcher_handler(message: AgentMessage):
    """Handler for researcher agent."""
    print(f"[Researcher] Received: {message.type}")
    print(f"   Task: {message.payload.get('task_id', 'N/A')}")
    print(f"   Description: {message.payload.get('description', 'N/A')}")

    # Simulate work
    await asyncio.sleep(0.1)

    # Create response
    response = AgentMessage(
        from_role=AgentRole.RESEARCHER,
        to_role=AgentRole.DT,
        type=MessageType.TASK_RESPONSE,
        payload={
            "task_id": message.payload["task_id"],
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
    print("Agents_Army Protocol Example\n")

    # 1. Create a message
    print("1. Creating a task request message...")
    message = AgentMessage(
        from_role=AgentRole.DT,
        to_role=AgentRole.RESEARCHER,
        type=MessageType.TASK_REQUEST,
        payload={
            "task_id": "task_001",
            "description": "Research best practices for AI agents",
            "parameters": {
                "topic": "AI agents",
                "depth": "medium",
                "sources": 5,
            },
        },
        metadata={
            "priority": Priority.HIGH,
            "tags": ["research", "ai"],
        },
    )

    print(f"   Message ID: {message.id}")
    print(f"   From: {message.from_role.value}")
    print(f"   To: {message.to_role.value}")
    print(f"   Type: {message.type.value}")
    print(f"   Priority: {message.metadata.priority.value}\n")

    # 2. Serialize message
    print("2. Serializing message to JSON...")
    json_str = MessageSerializer.serialize(message)
    print(f"   JSON length: {len(json_str)} characters\n")

    # 3. Deserialize message
    print("3. Deserializing message from JSON...")
    deserialized = MessageSerializer.deserialize(json_str)
    print(f"   Deserialized message ID: {deserialized.id}")
    print(f"   Match: {deserialized.id == message.id}\n")

    # 4. Setup router and handler
    print("4. Setting up message router...")
    router = MessageRouter()
    router.register_handler(AgentRole.RESEARCHER, researcher_handler)
    print("   Router configured\n")

    # 5. Route message
    print("5. Routing message to researcher...")
    await router.route(message)
    print("   Message routed successfully\n")

    # 6. Test message queue
    print("6. Testing message queue...")
    await router.start()

    for i in range(3):
        task_message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={
                "task_id": f"task_{i:03d}",
                "description": f"Task {i}",
            },
        )
        await router.send(task_message)

    await asyncio.sleep(0.2)  # Wait for processing
    await router.stop()
    print("   Queue processing completed\n")

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
