"""Data models for memory system."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class MemoryItem:
    """Represents a memory item."""

    key: str
    value: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    memory_type: str = "general"  # session, task, user, system, general

    def is_expired(self) -> bool:
        """Check if memory item has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "tags": self.tags,
            "memory_type": self.memory_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        """Create from dictionary."""
        item = cls(
            key=data["key"],
            value=data["value"],
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            memory_type=data.get("memory_type", "general"),
        )

        if "created_at" in data:
            item.created_at = datetime.fromisoformat(data["created_at"])
        if "expires_at" in data and data["expires_at"]:
            item.expires_at = datetime.fromisoformat(data["expires_at"])

        return item


@dataclass
class RetentionPolicy:
    """Retention policy for memory items."""

    session: timedelta = timedelta(hours=1)
    task: timedelta = timedelta(days=7)
    user: timedelta = timedelta(days=30)
    system: timedelta = timedelta(days=90)
    general: timedelta = timedelta(days=30)  # Default

    def get_ttl(self, memory_type: str) -> timedelta:
        """
        Get TTL for a memory type.

        Args:
            memory_type: Type of memory

        Returns:
            TTL timedelta
        """
        return getattr(self, memory_type, self.general)

    @classmethod
    def from_config(cls, config: Dict[str, str]) -> "RetentionPolicy":
        """
        Create from configuration dictionary.

        Args:
            config: Configuration with keys like "session": "1h", "task": "7d"

        Returns:
            RetentionPolicy instance
        """

        def parse_duration(duration_str: str) -> timedelta:
            """Parse duration string like '1h', '7d', '30d'."""
            if duration_str.endswith("h"):
                hours = int(duration_str[:-1])
                return timedelta(hours=hours)
            elif duration_str.endswith("d"):
                days = int(duration_str[:-1])
                return timedelta(days=days)
            elif duration_str.endswith("m"):
                minutes = int(duration_str[:-1])
                return timedelta(minutes=minutes)
            else:
                return timedelta(days=30)  # Default

        return cls(
            session=parse_duration(config.get("session", "1h")),
            task=parse_duration(config.get("task", "7d")),
            user=parse_duration(config.get("user", "30d")),
            system=parse_duration(config.get("system", "90d")),
            general=parse_duration(config.get("general", "30d")),
        )
