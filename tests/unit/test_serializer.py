"""Unit tests for MessageSerializer."""

import pytest

from agents_army.protocol.message import AgentMessage
from agents_army.protocol.serializer import MessageSerializer
from agents_army.protocol.types import AgentRole, MessageType


class TestMessageSerializer:
    """Test MessageSerializer class."""

    def test_serialize_json(self):
        """Test JSON serialization."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        json_str = MessageSerializer.serialize(message, format="json")
        assert isinstance(json_str, str)
        assert "task_001" in json_str
        assert "task_request" in json_str

    def test_deserialize_json(self):
        """Test JSON deserialization."""
        json_str = '{"id":"msg_123","timestamp":"2024-01-01T12:00:00Z","from":"dt","to":"researcher","type":"task_request","payload":{"task_id":"task_001"}}'

        message = MessageSerializer.deserialize(json_str, format="json")

        assert message.from_role == AgentRole.DT
        assert message.to_role == AgentRole.RESEARCHER
        assert message.type == MessageType.TASK_REQUEST
        assert message.payload["task_id"] == "task_001"

    def test_serialize_dict(self):
        """Test dictionary serialization."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        message_dict = MessageSerializer.serialize_dict(message)
        assert isinstance(message_dict, dict)
        assert message_dict["from"] == "dt"
        assert message_dict["to"] == "researcher"

    def test_deserialize_dict(self):
        """Test dictionary deserialization."""
        message_dict = {
            "id": "msg_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "from": "dt",
            "to": "researcher",
            "type": "task_request",
            "payload": {"task_id": "task_001"},
        }

        message = MessageSerializer.deserialize_dict(message_dict)

        assert message.from_role == AgentRole.DT
        assert message.to_role == AgentRole.RESEARCHER
        assert message.type == MessageType.TASK_REQUEST

    def test_validate_json(self):
        """Test JSON validation."""
        valid_json = '{"id":"msg_123","timestamp":"2024-01-01T12:00:00Z","from":"dt","to":"researcher","type":"task_request","payload":{"task_id":"task_001"}}'
        invalid_json = '{"invalid": "json"}'

        assert MessageSerializer.validate_json(valid_json) is True
        assert MessageSerializer.validate_json(invalid_json) is False

    def test_unsupported_format(self):
        """Test error on unsupported format."""
        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        with pytest.raises(ValueError, match="Unsupported format"):
            MessageSerializer.serialize(message, format="xml")

        with pytest.raises(ValueError, match="Unsupported format"):
            MessageSerializer.deserialize("data", format="xml")
