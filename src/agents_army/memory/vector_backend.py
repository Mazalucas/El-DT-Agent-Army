"""Vector backends for semantic search in memory."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents_army.memory.backend import MemoryBackend
from agents_army.memory.embeddings import EmbeddingProvider, MockEmbeddings
from agents_army.memory.models import MemoryItem, RetentionPolicy


class VectorBackend(MemoryBackend):
    """
    Abstract base class for vector-based memory backends.
    
    Extends MemoryBackend with semantic search capabilities using embeddings.
    """

    def __init__(self, embedding_provider: Optional[EmbeddingProvider] = None):
        """
        Initialize VectorBackend.

        Args:
            embedding_provider: Optional embedding provider (uses MockEmbeddings if None)
        """
        self.embedding_provider = embedding_provider or MockEmbeddings()

    @abstractmethod
    async def search_semantic(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        tags: Optional[List[str]] = None,
    ) -> List[MemoryItem]:
        """
        Perform semantic search using embeddings.

        Args:
            query: Search query
            limit: Maximum number of results
            threshold: Similarity threshold (0.0 - 1.0)
            tags: Optional tags to filter by

        Returns:
            List of matching memory items
        """
        pass

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (0.0 - 1.0)
        """
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


class InMemoryVectorBackend(VectorBackend):
    """
    In-memory vector backend for semantic search.
    
    Stores embeddings in memory and performs similarity search.
    Suitable for development and small-scale deployments.
    """

    def __init__(self, embedding_provider: Optional[EmbeddingProvider] = None):
        """
        Initialize InMemoryVectorBackend.

        Args:
            embedding_provider: Optional embedding provider
        """
        super().__init__(embedding_provider)
        self._storage: Dict[str, MemoryItem] = {}
        self._embeddings: Dict[str, List[float]] = {}

    async def store(self, item: MemoryItem) -> None:
        """
        Store memory item with embedding.

        Args:
            item: Memory item to store
        """
        # Generate embedding for value
        value_text = str(item.value)
        embedding = await self.embedding_provider.embed(value_text)
        self._embeddings[item.key] = embedding

        # Store item
        self._storage[item.key] = item

    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """
        Retrieve memory item by key.

        Args:
            key: Memory key

        Returns:
            Memory item or None
        """
        item = self._storage.get(key)
        if item and item.is_expired():
            del self._storage[key]
            self._embeddings.pop(key, None)
            return None
        return item

    async def search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[MemoryItem]:
        """
        Search memory items by text (uses semantic search).

        Args:
            query: Search query
            tags: Optional tags
            limit: Maximum results

        Returns:
            List of matching items
        """
        return await self.search_semantic(query, limit=limit, tags=tags, threshold=0.0)

    async def search_semantic(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        tags: Optional[List[str]] = None,
    ) -> List[MemoryItem]:
        """
        Perform semantic search.

        Args:
            query: Search query
            limit: Maximum results
            threshold: Similarity threshold
            tags: Optional tags

        Returns:
            List of matching items sorted by similarity
        """
        # Generate query embedding
        query_embedding = await self.embedding_provider.embed(query)

        # Calculate similarities
        results = []
        for item in self._storage.values():
            if item.is_expired():
                continue

            # Filter by tags if provided
            if tags and not any(tag in item.tags for tag in tags):
                continue

            # Get item embedding
            item_embedding = self._embeddings.get(item.key)
            if not item_embedding:
                continue

            # Calculate similarity
            similarity = self._cosine_similarity(query_embedding, item_embedding)

            if similarity >= threshold:
                results.append((similarity, item))

        # Sort by similarity (descending) and return top results
        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:limit]]

    async def delete(self, key: str) -> None:
        """
        Delete memory item.

        Args:
            key: Memory key
        """
        if key in self._storage:
            del self._storage[key]
            self._embeddings.pop(key, None)

    async def list_all(self, limit: Optional[int] = None) -> List[MemoryItem]:
        """
        List all memory items.

        Args:
            limit: Optional limit

        Returns:
            List of items
        """
        items = [item for item in self._storage.values() if not item.is_expired()]

        if limit:
            items = items[:limit]

        return items

    async def cleanup_expired(self) -> int:
        """
        Clean up expired memory items.

        Returns:
            Number of items deleted
        """
        expired_keys = [
            key for key, item in self._storage.items() if item.is_expired()
        ]

        for key in expired_keys:
            del self._storage[key]
            self._embeddings.pop(key, None)

        return len(expired_keys)
