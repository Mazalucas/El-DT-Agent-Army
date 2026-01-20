"""Memory backends - storage implementations."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents_army.memory.models import MemoryItem


class MemoryBackend(ABC):
    """Abstract base class for memory backends."""

    @abstractmethod
    async def store(self, item: MemoryItem) -> None:
        """
        Store a memory item.

        Args:
            item: Memory item to store
        """
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """
        Retrieve a memory item by key.

        Args:
            key: Memory item key

        Returns:
            Memory item or None if not found
        """
        pass

    @abstractmethod
    async def search(
        self, query: str, tags: Optional[List[str]] = None, limit: int = 10
    ) -> List[MemoryItem]:
        """
        Search memory items.

        Args:
            query: Search query (text search)
            tags: Optional tags to filter by
            limit: Maximum number of results

        Returns:
            List of matching memory items
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete a memory item.

        Args:
            key: Memory item key
        """
        pass

    @abstractmethod
    async def list_all(self, limit: Optional[int] = None) -> List[MemoryItem]:
        """
        List all memory items.

        Args:
            limit: Optional limit on number of items

        Returns:
            List of memory items
        """
        pass

    @abstractmethod
    async def cleanup_expired(self) -> int:
        """
        Clean up expired memory items.

        Returns:
            Number of items deleted
        """
        pass


class InMemoryBackend(MemoryBackend):
    """In-memory backend for development and testing."""

    def __init__(self):
        """Initialize in-memory backend."""
        self._storage: Dict[str, MemoryItem] = {}

    async def store(self, item: MemoryItem) -> None:
        """Store a memory item."""
        self._storage[item.key] = item

    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """Retrieve a memory item by key."""
        item = self._storage.get(key)
        if item and item.is_expired():
            del self._storage[key]
            return None
        return item

    async def search(
        self, query: str, tags: Optional[List[str]] = None, limit: int = 10
    ) -> List[MemoryItem]:
        """Search memory items."""
        results = []

        query_lower = query.lower()

        for item in self._storage.values():
            if item.is_expired():
                continue

            # Simple text search
            value_str = str(item.value).lower()
            key_lower = item.key.lower()

            if query_lower in value_str or query_lower in key_lower:
                # Check tags if provided
                if tags:
                    if not any(tag in item.tags for tag in tags):
                        continue

                results.append(item)

            if len(results) >= limit:
                break

        return results

    async def delete(self, key: str) -> None:
        """Delete a memory item."""
        if key in self._storage:
            del self._storage[key]

    async def list_all(self, limit: Optional[int] = None) -> List[MemoryItem]:
        """List all memory items."""
        items = [item for item in self._storage.values() if not item.is_expired()]

        if limit:
            items = items[:limit]

        return items

    async def cleanup_expired(self) -> int:
        """Clean up expired memory items."""
        expired_keys = [key for key, item in self._storage.items() if item.is_expired()]

        for key in expired_keys:
            del self._storage[key]

        return len(expired_keys)


class SQLiteBackend(MemoryBackend):
    """SQLite backend for production use."""

    def __init__(self, database_path: str = "memory.db"):
        """
        Initialize SQLite backend.

        Args:
            database_path: Path to SQLite database file
        """
        import sqlite3
        import json

        self.database_path = database_path
        self.conn = sqlite3.connect(database_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                tags TEXT NOT NULL,
                memory_type TEXT NOT NULL
            )
            """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)
            """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)
            """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expires_at ON memories(expires_at)
            """)
        self.conn.commit()

    async def store(self, item: MemoryItem) -> None:
        """Store a memory item."""
        import json

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO memories 
            (key, value, metadata, created_at, expires_at, tags, memory_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.key,
                json.dumps(item.value),
                json.dumps(item.metadata),
                item.created_at.isoformat(),
                item.expires_at.isoformat() if item.expires_at else None,
                json.dumps(item.tags),
                item.memory_type,
            ),
        )
        self.conn.commit()

    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """Retrieve a memory item by key."""
        import json

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM memories WHERE key = ? AND (expires_at IS NULL OR expires_at > datetime('now'))",
            (key,),
        )
        row = cursor.fetchone()

        if not row:
            return None

        return MemoryItem(
            key=row["key"],
            value=json.loads(row["value"]),
            metadata=json.loads(row["metadata"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
            tags=json.loads(row["tags"]),
            memory_type=row["memory_type"],
        )

    async def search(
        self, query: str, tags: Optional[List[str]] = None, limit: int = 10
    ) -> List[MemoryItem]:
        """Search memory items."""
        import json

        cursor = self.conn.cursor()

        # Simple LIKE search
        query_pattern = f"%{query}%"

        if tags:
            # Search with tags
            tags_json = json.dumps(tags)
            cursor.execute(
                """
                SELECT * FROM memories 
                WHERE (value LIKE ? OR key LIKE ?)
                AND (expires_at IS NULL OR expires_at > datetime('now'))
                AND tags LIKE ?
                LIMIT ?
                """,
                (query_pattern, query_pattern, f"%{tags_json[1:-1]}%", limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM memories 
                WHERE (value LIKE ? OR key LIKE ?)
                AND (expires_at IS NULL OR expires_at > datetime('now'))
                LIMIT ?
                """,
                (query_pattern, query_pattern, limit),
            )

        rows = cursor.fetchall()
        items = []

        for row in rows:
            items.append(
                MemoryItem(
                    key=row["key"],
                    value=json.loads(row["value"]),
                    metadata=json.loads(row["metadata"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                    expires_at=(
                        datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None
                    ),
                    tags=json.loads(row["tags"]),
                    memory_type=row["memory_type"],
                )
            )

        return items

    async def delete(self, key: str) -> None:
        """Delete a memory item."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories WHERE key = ?", (key,))
        self.conn.commit()

    async def list_all(self, limit: Optional[int] = None) -> List[MemoryItem]:
        """List all memory items."""
        import json

        cursor = self.conn.cursor()

        if limit:
            cursor.execute(
                """
                SELECT * FROM memories 
                WHERE expires_at IS NULL OR expires_at > datetime('now')
                LIMIT ?
                """,
                (limit,),
            )
        else:
            cursor.execute("""
                SELECT * FROM memories 
                WHERE expires_at IS NULL OR expires_at > datetime('now')
                """)

        rows = cursor.fetchall()
        items = []

        for row in rows:
            items.append(
                MemoryItem(
                    key=row["key"],
                    value=json.loads(row["value"]),
                    metadata=json.loads(row["metadata"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                    expires_at=(
                        datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None
                    ),
                    tags=json.loads(row["tags"]),
                    memory_type=row["memory_type"],
                )
            )

        return items

    async def cleanup_expired(self) -> int:
        """Clean up expired memory items."""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at <= datetime('now')"
        )
        deleted = cursor.rowcount
        self.conn.commit()
        return deleted

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
