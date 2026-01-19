"""Message serialization and deserialization."""

import json
from typing import Any, Dict

from agents_army.protocol.message import AgentMessage


class MessageSerializer:
    """
    Serializer for AgentMessage objects.

    Currently supports JSON format, with extensibility for other formats.
    """

    @staticmethod
    def serialize(message: AgentMessage, format: str = "json") -> str:
        """
        Serialize a message to string format.

        Args:
            message: The message to serialize
            format: Serialization format (currently only "json" supported)

        Returns:
            Serialized message as string

        Raises:
            ValueError: If format is not supported
        """
        if format == "json":
            return message.to_json()
        else:
            raise ValueError(f"Unsupported format: {format}")

    @staticmethod
    def deserialize(data: str, format: str = "json") -> AgentMessage:
        """
        Deserialize a message from string format.

        Args:
            data: Serialized message string
            format: Serialization format (currently only "json" supported)

        Returns:
            Deserialized AgentMessage

        Raises:
            ValueError: If format is not supported or data is invalid
        """
        if format == "json":
            try:
                return AgentMessage.from_json(data)
            except Exception as e:
                raise ValueError(f"Failed to deserialize JSON message: {e}")
        else:
            raise ValueError(f"Unsupported format: {format}")

    @staticmethod
    def serialize_dict(message: AgentMessage) -> Dict[str, Any]:
        """
        Serialize a message to dictionary.

        Args:
            message: The message to serialize

        Returns:
            Message as dictionary
        """
        return message.to_dict()

    @staticmethod
    def deserialize_dict(data: Dict[str, Any]) -> AgentMessage:
        """
        Deserialize a message from dictionary.

        Args:
            data: Message dictionary

        Returns:
            Deserialized AgentMessage

        Raises:
            ValueError: If data is invalid
        """
        try:
            return AgentMessage.from_dict(data)
        except Exception as e:
            raise ValueError(f"Failed to deserialize message from dict: {e}")

    @staticmethod
    def validate_json(json_str: str) -> bool:
        """
        Validate that a JSON string is a valid message.

        Args:
            json_str: JSON string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            AgentMessage.from_json(json_str)
            return True
        except Exception:
            return False
