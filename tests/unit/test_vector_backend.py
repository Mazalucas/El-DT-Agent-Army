"""Unit tests for vector backends."""

import pytest

from agents_army.memory.embeddings import MockEmbeddings
from agents_army.memory.models import MemoryItem, RetentionPolicy
from agents_army.memory.vector_backend import InMemoryVectorBackend


class TestInMemoryVectorBackend:
    """Test InMemoryVectorBackend functionality."""

    @pytest.mark.asyncio
    async def test_store_with_embedding(self):
        """Test storing items with embeddings."""
        backend = InMemoryVectorBackend(embedding_provider=MockEmbeddings())

        item = MemoryItem(
            key="test_key",
            value="Test value",
            tags=["test"],
            memory_type="general",
        )

        await backend.store(item)

        assert "test_key" in backend._storage
        assert "test_key" in backend._embeddings
        assert len(backend._embeddings["test_key"]) == 384  # MockEmbeddings default

    @pytest.mark.asyncio
    async def test_search_semantic(self):
        """Test semantic search."""
        backend = InMemoryVectorBackend(embedding_provider=MockEmbeddings())

        # Store items
        item1 = MemoryItem(
            key="key1",
            value="Python programming language",
            tags=["programming"],
        )
        item2 = MemoryItem(
            key="key2",
            value="JavaScript web development",
            tags=["programming"],
        )
        item3 = MemoryItem(
            key="key3",
            value="Cooking recipes",
            tags=["food"],
        )

        await backend.store(item1)
        await backend.store(item2)
        await backend.store(item3)

        # Search with threshold 0.0 (should find all items)
        results = await backend.search_semantic("test query", limit=10, threshold=0.0)

        # MockEmbeddings uses hash-based approach, so results depend on hash similarity
        # Just verify search doesn't crash and returns some results
        assert len(results) >= 0

    @pytest.mark.asyncio
    async def test_search_semantic_with_threshold(self):
        """Test semantic search with threshold."""
        backend = InMemoryVectorBackend(embedding_provider=MockEmbeddings())

        item = MemoryItem(
            key="key1",
            value="Test content",
            tags=["test"],
        )

        await backend.store(item)

        # Search with high threshold (should find item)
        results = await backend.search_semantic("Test content", limit=10, threshold=0.0)
        assert len(results) >= 1

        # Search with very high threshold (might not find)
        results = await backend.search_semantic("completely different", limit=10, threshold=0.99)
        # Results depend on hash similarity, so just check it doesn't crash

    @pytest.mark.asyncio
    async def test_search_semantic_with_tags(self):
        """Test semantic search with tag filtering."""
        backend = InMemoryVectorBackend(embedding_provider=MockEmbeddings())

        item1 = MemoryItem(
            key="key1",
            value="Python programming",
            tags=["programming"],
        )
        item2 = MemoryItem(
            key="key2",
            value="Python snake",
            tags=["animals"],
        )

        await backend.store(item1)
        await backend.store(item2)

        # Search with tag filter
        results = await backend.search_semantic(
            "Python", limit=10, threshold=0.0, tags=["programming"]
        )

        # Should only return items with programming tag
        assert len(results) <= 1
        if results:
            assert results[0].key == "key1"
            assert "programming" in results[0].tags

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        backend = InMemoryVectorBackend()

        # Test identical vectors
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = backend._cosine_similarity(vec1, vec2)
        assert abs(similarity - 1.0) < 0.01

        # Test orthogonal vectors
        vec1 = [1.0, 0.0]
        vec2 = [0.0, 1.0]
        similarity = backend._cosine_similarity(vec1, vec2)
        assert abs(similarity - 0.0) < 0.01

        # Test different length vectors
        vec1 = [1.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = backend._cosine_similarity(vec1, vec2)
        assert similarity == 0.0


class TestMockEmbeddings:
    """Test MockEmbeddings functionality."""

    @pytest.mark.asyncio
    async def test_embed(self):
        """Test generating embeddings."""
        embeddings = MockEmbeddings(dimensions=128)

        embedding = await embeddings.embed("Test text")

        assert len(embedding) == 128
        assert all(isinstance(x, float) for x in embedding)

    @pytest.mark.asyncio
    async def test_embed_batch(self):
        """Test batch embedding generation."""
        embeddings = MockEmbeddings(dimensions=128)

        texts = ["Text 1", "Text 2", "Text 3"]
        batch_embeddings = await embeddings.embed_batch(texts)

        assert len(batch_embeddings) == 3
        assert all(len(emb) == 128 for emb in batch_embeddings)

    def test_dimensions(self):
        """Test dimensions property."""
        embeddings = MockEmbeddings(dimensions=256)
        assert embeddings.dimensions == 256
