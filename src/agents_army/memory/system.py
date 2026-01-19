"""Memory system for storing and retrieving agent memories."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from agents_army.memory.backend import MemoryBackend
from agents_army.memory.models import MemoryItem, RetentionPolicy


class MemorySystem:
    """
    Memory system for storing and retrieving agent memories.

    Provides persistent storage with retention policies and search capabilities.
    """

    def __init__(
        self,
        backend: MemoryBackend,
        retention_policy: Optional[RetentionPolicy] = None,
    ):
        """
        Initialize memory system.

        Args:
            backend: Memory backend implementation
            retention_policy: Optional retention policy (uses default if None)
        """
        self.backend = backend
        self.retention_policy = retention_policy or RetentionPolicy()

    async def store(
        self,
        key: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        memory_type: str = "general",
        ttl: Optional[timedelta] = None,
    ) -> None:
        """
        Store a memory item.

        Args:
            key: Unique identifier
            value: Value to store
            metadata: Optional metadata
            tags: Optional tags for searching
            memory_type: Type of memory (session, task, user, system, general)
            ttl: Optional time to live (uses retention policy if None)
        """
        if ttl is None:
            ttl = self.retention_policy.get_ttl(memory_type)

        expires_at = datetime.now() + ttl if ttl else None

        item = MemoryItem(
            key=key,
            value=value,
            metadata=metadata or {},
            tags=tags or [],
            memory_type=memory_type,
            created_at=datetime.now(),
            expires_at=expires_at,
        )

        await self.backend.store(item)

    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """
        Retrieve a memory item by key.

        Args:
            key: Memory item key

        Returns:
            Memory item or None if not found or expired
        """
        item = await self.backend.retrieve(key)
        if item and item.is_expired():
            await self.backend.delete(key)
            return None
        return item

    async def search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[MemoryItem]:
        """
        Search memory items.

        Args:
            query: Search query (text search)
            tags: Optional tags to filter by
            memory_type: Optional memory type to filter by
            limit: Maximum number of results

        Returns:
            List of matching memory items
        """
        results = await self.backend.search(query, tags=tags, limit=limit)

        # Filter by memory type if specified
        if memory_type:
            results = [r for r in results if r.memory_type == memory_type]

        # Remove expired items
        valid_results = []
        for item in results:
            if item.is_expired():
                await self.backend.delete(item.key)
            else:
                valid_results.append(item)

        return valid_results

    async def delete(self, key: str) -> None:
        """
        Delete a memory item.

        Args:
            key: Memory item key
        """
        await self.backend.delete(key)

    async def list_all(
        self, memory_type: Optional[str] = None, limit: Optional[int] = None
    ) -> List[MemoryItem]:
        """
        List all memory items.

        Args:
            memory_type: Optional memory type to filter by
            limit: Optional limit on number of items

        Returns:
            List of memory items
        """
        items = await self.backend.list_all(limit=limit)

        if memory_type:
            items = [item for item in items if item.memory_type == memory_type]

        return items

    async def cleanup_expired(self) -> int:
        """
        Clean up expired memory items.

        Returns:
            Number of items deleted
        """
        return await self.backend.cleanup_expired()
