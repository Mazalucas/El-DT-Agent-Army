"""Memory Agent - Agent wrapper for MemorySystem."""

from typing import Any, Dict, Optional

from agents_army.core.agent import Agent, AgentConfig, LLMProvider
from agents_army.memory.models import RetentionPolicy
from agents_army.memory.system import MemorySystem
from agents_army.memory.backend import InMemoryBackend, MemoryBackend
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class MemoryAgent(Agent):
    """
    Memory Agent - Provides memory functionality as an agent.

    Wraps MemorySystem to provide agent interface for memory operations.
    """

    def __init__(
        self,
        name: str = "Memory Agent",
        backend: Optional[MemoryBackend] = None,
        retention_policy: Optional[RetentionPolicy] = None,
        llm_provider: Optional[LLMProvider] = None,
    ):
        """
        Initialize Memory Agent.

        Args:
            name: Agent name
            backend: Optional memory backend (uses InMemoryBackend if None)
            retention_policy: Optional retention policy
            llm_provider: Optional LLM provider (not used but required by Agent)
        """
        config = AgentConfig(
            name=name,
            role=AgentRole.MEMORY,
            goal="Store and retrieve agent memories",
            backstory=(
                "You are the memory system for the agent army. You store "
                "and retrieve information to help agents maintain context "
                "across interactions."
            ),
            instructions="Store and retrieve memories as requested by agents.",
            model="gpt-4",  # Not used but required
            allow_delegation=False,
            max_iterations=1,
        )

        super().__init__(config, llm_provider)

        self.memory_system = MemorySystem(
            backend=backend or InMemoryBackend(),
            retention_policy=retention_policy,
        )

    async def store(
        self,
        key: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[list] = None,
        memory_type: str = "general",
    ) -> None:
        """
        Store a memory.

        Args:
            key: Memory key
            value: Memory value
            metadata: Optional metadata
            tags: Optional tags
            memory_type: Memory type
        """
        await self.memory_system.store(
            key=key,
            value=value,
            metadata=metadata,
            tags=tags,
            memory_type=memory_type,
        )

    async def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve a memory.

        Args:
            key: Memory key

        Returns:
            Memory value or None
        """
        item = await self.memory_system.retrieve(key)
        return item.value if item else None

    async def search(
        self, query: str, tags: Optional[list] = None, limit: int = 10
    ) -> list:
        """
        Search memories.

        Args:
            query: Search query
            tags: Optional tags
            limit: Maximum results

        Returns:
            List of memory items
        """
        return await self.memory_system.search(query, tags=tags, limit=limit)

    async def search_semantic(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        tags: Optional[list] = None,
    ) -> list:
        """
        Perform semantic search.

        Args:
            query: Search query
            limit: Maximum results
            threshold: Similarity threshold (0.0 - 1.0)
            tags: Optional tags

        Returns:
            List of memory items sorted by similarity
        """
        return await self.memory_system.search_semantic(
            query, limit=limit, threshold=threshold, tags=tags
        )

    async def _process_message(
        self, message: AgentMessage
    ) -> Optional[AgentMessage]:
        """
        Process incoming message.

        Args:
            message: Incoming message

        Returns:
            Optional response message
        """
        if message.type == MessageType.MEMORY_STORE:
            # Store memory
            payload = message.payload
            await self.store(
                key=payload["key"],
                value=payload["value"],
                metadata=payload.get("metadata"),
                tags=payload.get("tags"),
                memory_type=payload.get("memory_type", "general"),
            )

            return AgentMessage(
                from_role=self.role,
                to_role=message.from_role,
                type=MessageType.MEMORY_RESPONSE,
                payload={"status": "stored", "key": payload["key"]},
                reply_to=message.id,
            )

        elif message.type == MessageType.MEMORY_QUERY:
            # Query memory
            payload = message.payload

            if "key" in payload:
                # Retrieve by key
                value = await self.retrieve(payload["key"])

                return AgentMessage(
                    from_role=self.role,
                    to_role=message.from_role,
                    type=MessageType.MEMORY_RESPONSE,
                    payload={"key": payload["key"], "value": value},
                    reply_to=message.id,
                )

            elif "query" in payload:
                # Search
                results = await self.search(
                    query=payload["query"],
                    tags=payload.get("tags"),
                    limit=payload.get("limit", 10),
                )

                return AgentMessage(
                    from_role=self.role,
                    to_role=message.from_role,
                    type=MessageType.MEMORY_RESPONSE,
                    payload={
                        "query": payload["query"],
                        "results": [item.to_dict() for item in results],
                    },
                    reply_to=message.id,
                )

        return None
