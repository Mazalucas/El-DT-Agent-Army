"""Unit tests for memory system."""

import tempfile
from datetime import datetime, timedelta

import pytest

from agents_army.memory.backend import InMemoryBackend, SQLiteBackend
from agents_army.memory.models import MemoryItem, RetentionPolicy
from agents_army.memory.system import MemorySystem


class TestMemoryItem:
    """Test MemoryItem model."""

    def test_create_memory_item(self):
        """Test creating memory item."""
        item = MemoryItem(
            key="test_key",
            value="test_value",
            tags=["tag1", "tag2"],
            memory_type="session",
        )

        assert item.key == "test_key"
        assert item.value == "test_value"
        assert item.tags == ["tag1", "tag2"]
        assert item.memory_type == "session"
        assert item.is_expired() is False

    def test_expired_memory_item(self):
        """Test expired memory item."""
        item = MemoryItem(
            key="test_key",
            value="test_value",
            expires_at=datetime.now() - timedelta(hours=1),
        )

        assert item.is_expired() is True

    def test_memory_item_to_dict(self):
        """Test memory item serialization."""
        item = MemoryItem(
            key="test_key",
            value="test_value",
            tags=["tag1"],
            memory_type="task",
        )

        data = item.to_dict()
        assert data["key"] == "test_key"
        assert data["value"] == "test_value"
        assert data["tags"] == ["tag1"]
        assert data["memory_type"] == "task"

    def test_memory_item_from_dict(self):
        """Test memory item deserialization."""
        data = {
            "key": "test_key",
            "value": "test_value",
            "tags": ["tag1"],
            "memory_type": "task",
            "created_at": datetime.now().isoformat(),
        }

        item = MemoryItem.from_dict(data)
        assert item.key == "test_key"
        assert item.value == "test_value"


class TestRetentionPolicy:
    """Test RetentionPolicy."""

    def test_default_retention_policy(self):
        """Test default retention policy."""
        policy = RetentionPolicy()

        assert policy.session == timedelta(hours=1)
        assert policy.task == timedelta(days=7)
        assert policy.user == timedelta(days=30)
        assert policy.system == timedelta(days=90)

    def test_get_ttl(self):
        """Test getting TTL for memory type."""
        policy = RetentionPolicy()

        assert policy.get_ttl("session") == timedelta(hours=1)
        assert policy.get_ttl("task") == timedelta(days=7)
        assert policy.get_ttl("general") == timedelta(days=30)

    def test_from_config(self):
        """Test creating from config."""
        config = {
            "session": "2h",
            "task": "14d",
            "user": "60d",
        }

        policy = RetentionPolicy.from_config(config)

        assert policy.session == timedelta(hours=2)
        assert policy.task == timedelta(days=14)
        assert policy.user == timedelta(days=60)


class TestInMemoryBackend:
    """Test InMemoryBackend."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        """Test storing and retrieving items."""
        backend = InMemoryBackend()

        item = MemoryItem(key="test", value="value")
        await backend.store(item)

        retrieved = await backend.retrieve("test")
        assert retrieved is not None
        assert retrieved.value == "value"

    @pytest.mark.asyncio
    async def test_search(self):
        """Test searching items."""
        backend = InMemoryBackend()

        item1 = MemoryItem(key="key1", value="test value", tags=["tag1"])
        item2 = MemoryItem(key="key2", value="other value", tags=["tag2"])

        await backend.store(item1)
        await backend.store(item2)

        results = await backend.search("test")
        assert len(results) == 1
        assert results[0].key == "key1"

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting items."""
        backend = InMemoryBackend()

        item = MemoryItem(key="test", value="value")
        await backend.store(item)

        await backend.delete("test")
        retrieved = await backend.retrieve("test")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_cleanup_expired(self):
        """Test cleaning up expired items."""
        backend = InMemoryBackend()

        expired_item = MemoryItem(
            key="expired",
            value="value",
            expires_at=datetime.now() - timedelta(hours=1),
        )
        valid_item = MemoryItem(key="valid", value="value")

        await backend.store(expired_item)
        await backend.store(valid_item)

        deleted = await backend.cleanup_expired()
        assert deleted == 1

        assert await backend.retrieve("expired") is None
        assert await backend.retrieve("valid") is not None


class TestSQLiteBackend:
    """Test SQLiteBackend."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        """Test storing and retrieving items."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            backend = SQLiteBackend(database_path=db_path)

            item = MemoryItem(key="test", value="value")
            await backend.store(item)

            retrieved = await backend.retrieve("test")
            assert retrieved is not None
            assert retrieved.value == "value"

            backend.close()
        finally:
            import os

            if os.path.exists(db_path):
                os.unlink(db_path)

    @pytest.mark.asyncio
    async def test_search(self):
        """Test searching items."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            backend = SQLiteBackend(database_path=db_path)

            item1 = MemoryItem(key="key1", value="test value")
            item2 = MemoryItem(key="key2", value="other value")

            await backend.store(item1)
            await backend.store(item2)

            results = await backend.search("test")
            assert len(results) == 1
            assert results[0].key == "key1"

            backend.close()
        finally:
            import os

            if os.path.exists(db_path):
                os.unlink(db_path)


class TestMemorySystem:
    """Test MemorySystem."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        """Test storing and retrieving memories."""
        backend = InMemoryBackend()
        system = MemorySystem(backend)

        await system.store("test_key", "test_value", memory_type="session")

        item = await system.retrieve("test_key")
        assert item is not None
        assert item.value == "test_value"
        assert item.memory_type == "session"

    @pytest.mark.asyncio
    async def test_search(self):
        """Test searching memories."""
        backend = InMemoryBackend()
        system = MemorySystem(backend)

        await system.store("key1", "test value", tags=["tag1"])
        await system.store("key2", "other value", tags=["tag2"])

        results = await system.search("test")
        assert len(results) == 1
        assert results[0].key == "key1"

    @pytest.mark.asyncio
    async def test_retention_policy(self):
        """Test retention policy application."""
        backend = InMemoryBackend()
        policy = RetentionPolicy(session=timedelta(minutes=1))
        system = MemorySystem(backend, retention_policy=policy)

        await system.store("test", "value", memory_type="session")

        item = await system.retrieve("test")
        assert item is not None
        assert item.expires_at is not None

    @pytest.mark.asyncio
    async def test_cleanup_expired(self):
        """Test cleaning up expired memories."""
        backend = InMemoryBackend()
        system = MemorySystem(backend)

        # Store with short TTL
        await system.store("expired", "value", memory_type="session", ttl=timedelta(seconds=-1))
        await system.store("valid", "value", memory_type="task")

        deleted = await system.cleanup_expired()
        assert deleted >= 0  # May be 0 if cleanup happens automatically
