"""
Example of using the Memory System.

This example demonstrates:
- Storing memories
- Retrieving memories
- Searching memories
- Using different backends
- Retention policies
"""

import asyncio
from datetime import timedelta

from agents_army.memory import (
    InMemoryBackend,
    MemoryAgent,
    MemorySystem,
    RetentionPolicy,
    SQLiteBackend,
)


async def main():
    """Main example function."""
    print("Memory System Example\n")

    # 1. Create memory system with in-memory backend
    print("1. Creating memory system (in-memory backend)...")
    backend = InMemoryBackend()
    memory = MemorySystem(backend)
    print("   Memory system created\n")

    # 2. Store memories
    print("2. Storing memories...")
    await memory.store(
        key="user_preference_1",
        value="User prefers dark mode",
        tags=["user", "preference"],
        memory_type="user",
    )

    await memory.store(
        key="task_result_1",
        value="Task completed successfully",
        tags=["task", "result"],
        memory_type="task",
    )

    await memory.store(
        key="session_context_1",
        value="Current session: working on feature X",
        tags=["session"],
        memory_type="session",
    )

    print("   Stored 3 memories\n")

    # 3. Retrieve memory
    print("3. Retrieving memory...")
    item = await memory.retrieve("user_preference_1")
    if item:
        print(f"   Retrieved: {item.key} = {item.value}")
        print(f"   Type: {item.memory_type}, Tags: {item.tags}\n")

    # 4. Search memories
    print("4. Searching memories...")
    results = await memory.search("task", tags=["task"])
    print(f"   Found {len(results)} memories matching 'task':")
    for result in results:
        print(f"     - {result.key}: {result.value}\n")

    # 5. List all memories
    print("5. Listing all memories...")
    all_memories = await memory.list_all()
    print(f"   Total memories: {len(all_memories)}")
    for mem in all_memories:
        print(f"     - {mem.key} ({mem.memory_type})\n")

    # 6. Test with SQLite backend
    print("6. Testing SQLite backend...")
    sqlite_backend = SQLiteBackend(database_path=":memory:")  # In-memory SQLite
    sqlite_memory = MemorySystem(sqlite_backend)

    await sqlite_memory.store(
        key="sqlite_test",
        value="SQLite storage test",
        memory_type="system",
    )

    retrieved = await sqlite_memory.retrieve("sqlite_test")
    if retrieved:
        print(f"   Retrieved from SQLite: {retrieved.value}\n")

    sqlite_backend.close()

    # 7. Test retention policy
    print("7. Testing retention policy...")
    policy = RetentionPolicy(
        session=timedelta(hours=1),
        task=timedelta(days=7),
        user=timedelta(days=30),
    )

    policy_memory = MemorySystem(InMemoryBackend(), retention_policy=policy)

    await policy_memory.store(
        key="session_memory",
        value="Session data",
        memory_type="session",
    )

    item = await policy_memory.retrieve("session_memory")
    if item:
        print(f"   Session memory TTL: {item.expires_at}\n")

    # 8. Test Memory Agent
    print("8. Testing Memory Agent...")
    memory_agent = MemoryAgent(backend=InMemoryBackend())

    await memory_agent.store(
        key="agent_memory",
        value="Stored via agent",
        memory_type="general",
    )

    retrieved_value = await memory_agent.retrieve("agent_memory")
    print(f"   Retrieved via agent: {retrieved_value}\n")

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
