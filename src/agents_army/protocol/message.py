"""AgentMessage class with schema validation."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from agents_army.protocol.types import (
    AgentRole,
    Encryption,
    MessageType,
    Priority,
)


class MessageMetadata(BaseModel):
    """Metadata for agent messages."""

    priority: Priority = Priority.NORMAL
    retry_count: int = Field(default=0, ge=0)
    deadline: Optional[str] = None  # ISO 8601 timestamp
    tags: List[str] = Field(default_factory=list)

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v: Optional[str]) -> Optional[str]:
        """Validate deadline is ISO 8601 format."""
        if v is not None:
            try:
                datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("deadline must be ISO 8601 format")
        return v


class AgentMessage(BaseModel):
    """
    Standard message format for agent communication.

    This class implements the protocol specification from PROTOCOL.md
    with full schema validation using Pydantic.
    """

    # Identification
    id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    correlation_id: Optional[str] = None

    # Routing
    from_role: AgentRole = Field(..., alias="from")
    to_role: Union[AgentRole, List[AgentRole]] = Field(..., alias="to")
    reply_to: Optional[str] = None

    # Content
    type: MessageType
    payload: Dict[str, Any] = Field(default_factory=dict)

    # Metadata
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)

    # Security
    signature: Optional[str] = None
    encryption: Encryption = Encryption.NONE

    model_config = {
        "populate_by_name": True,  # Allow both field name and alias
        "json_schema_extra": {
            "example": {
                "id": "msg_001",
                "timestamp": "2024-01-01T12:00:00Z",
                "from": "dt",
                "to": "researcher",
                "type": "task_request",
                "payload": {
                    "task_id": "task_001",
                    "description": "Research topic X",
                },
                "metadata": {
                    "priority": "high",
                    "retry_count": 0,
                },
            }
        },
    }

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        """Validate timestamp is ISO 8601 format."""
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be ISO 8601 format")
        return v

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, v: Dict[str, Any], info) -> Dict[str, Any]:
        """Validate payload is not empty for non-heartbeat messages."""
        message_type = info.data.get("type")
        if message_type != MessageType.HEARTBEAT and not v:
            raise ValueError("payload cannot be empty for non-heartbeat messages")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_json(self) -> str:
        """Convert message to JSON string."""
        return self.model_dump_json(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create message from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "AgentMessage":
        """Create message from JSON string."""
        return cls.model_validate_json(json_str)

    def is_reply_to(self, other: "AgentMessage") -> bool:
        """Check if this message is a reply to another message."""
        return self.reply_to == other.id

    def is_high_priority(self) -> bool:
        """Check if message has high or critical priority."""
        return self.metadata.priority in (Priority.HIGH, Priority.CRITICAL)

    def has_deadline(self) -> bool:
        """Check if message has a deadline."""
        return self.metadata.deadline is not None

    def is_past_deadline(self) -> bool:
        """Check if message deadline has passed."""
        if not self.has_deadline():
            return False
        deadline = datetime.fromisoformat(
            self.metadata.deadline.replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)
        return now > deadline

    def get_to_roles(self) -> List[AgentRole]:
        """Get list of recipient roles."""
        if isinstance(self.to_role, list):
            return self.to_role
        return [self.to_role]
