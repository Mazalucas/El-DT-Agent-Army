"""Unit tests for AgentMessage."""

import pytest
from datetime import datetime, timezone

from agents_army.protocol.message import AgentMessage, MessageMetadata
from agents_army.protocol.types import (
    AgentRole,
    Encryption,
    MessageType,
    Priority,
)


class TestAgentMessage:
    """Test AgentMessage class."""

    def test_create_message(self):
        """Test creating a basic message."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001", "description": "Test task"},
        )

        assert message.from_role == AgentRole.DT
        assert message.to_role == AgentRole.RESEARCHER
        assert message.type == MessageType.TASK_REQUEST
        assert message.payload["task_id"] == "task_001"
        assert message.id.startswith("msg_")
        assert message.timestamp is not None

    def test_message_with_metadata(self):
        """Test message with custom metadata."""
        metadata = MessageMetadata(
            priority=Priority.HIGH,
            retry_count=2,
            tags=["urgent", "research"],
        )

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
            metadata=metadata,
        )

        assert message.metadata.priority == Priority.HIGH
        assert message.metadata.retry_count == 2
        assert "urgent" in message.metadata.tags

    def test_message_with_multiple_recipients(self):
        """Test message with multiple recipients."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=[AgentRole.RESEARCHER, AgentRole.WRITER],
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        to_roles = message.get_to_roles()
        assert len(to_roles) == 2
        assert AgentRole.RESEARCHER in to_roles
        assert AgentRole.WRITER in to_roles

    def test_message_reply(self):
        """Test message reply relationship."""
        original = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        reply = AgentMessage(
            from_role=AgentRole.RESEARCHER,
            to_role=AgentRole.DT,
            type=MessageType.TASK_RESPONSE,
            payload={"task_id": "task_001", "status": "completed"},
            reply_to=original.id,
        )

        assert reply.is_reply_to(original)
        assert not original.is_reply_to(reply)

    def test_message_priority(self):
        """Test message priority checks."""
        high_priority = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
            metadata=MessageMetadata(priority=Priority.HIGH),
        )

        normal_priority = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_002"},
            metadata=MessageMetadata(priority=Priority.NORMAL),
        )

        assert high_priority.is_high_priority()
        assert not normal_priority.is_high_priority()

    def test_message_deadline(self):
        """Test message deadline functionality."""
        future_deadline = datetime.now(timezone.utc).replace(year=2030).isoformat()

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
            metadata=MessageMetadata(deadline=future_deadline),
        )

        assert message.has_deadline()
        assert not message.is_past_deadline()

    def test_message_serialization(self):
        """Test message serialization to dict and JSON."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001", "description": "Test"},
        )

        # Test dict serialization
        message_dict = message.to_dict()
        assert message_dict["from"] == "dt"
        assert message_dict["to"] == "researcher"
        assert message_dict["type"] == "task_request"

        # Test JSON serialization
        json_str = message.to_json()
        assert "task_001" in json_str
        assert "task_request" in json_str

        # Test deserialization
        deserialized = AgentMessage.from_json(json_str)
        assert deserialized.id == message.id
        assert deserialized.from_role == message.from_role
        assert deserialized.to_role == message.to_role

    def test_message_validation_empty_payload(self):
        """Test that non-heartbeat messages require payload."""
        # Non-heartbeat with empty payload should fail
        with pytest.raises(ValueError, match="payload cannot be empty"):
            AgentMessage(
                from_role=AgentRole.DT,
                to_role=AgentRole.RESEARCHER,
                type=MessageType.TASK_REQUEST,
                payload={},
            )

        # Heartbeat can have empty payload
        heartbeat = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.HEARTBEAT,
            payload={},
        )
        assert heartbeat.type == MessageType.HEARTBEAT

    def test_message_validation_timestamp(self):
        """Test timestamp validation."""
        with pytest.raises(ValueError, match="timestamp must be ISO 8601"):
            AgentMessage(
                from_role=AgentRole.DT,
                to_role=AgentRole.RESEARCHER,
                type=MessageType.TASK_REQUEST,
                payload={"task_id": "task_001"},
                timestamp="invalid-timestamp",
            )

    def test_message_encryption(self):
        """Test message encryption field."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
            encryption=Encryption.TLS,
        )

        assert message.encryption == Encryption.TLS
