"""Structured logging for Agents_Army."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredLogger:
    """
    Structured logger that outputs JSON-formatted logs.

    Provides consistent logging format for all agents and system components.
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize StructuredLogger.

        Args:
            name: Logger name
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers
        self.logger.handlers = []

        # Create console handler with JSON formatter
        handler = logging.StreamHandler()
        handler.setLevel(level)

        # Use JSON formatter
        formatter = JSONFormatter()
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_agent_action(
        self,
        agent_id: str,
        action: str,
        metadata: Optional[Dict[str, Any]] = None,
        level: str = "info",
    ) -> None:
        """
        Log an agent action.

        Args:
            agent_id: Agent ID
            action: Action performed
            metadata: Optional metadata
            level: Log level (info, warning, error)
        """
        log_data = {
            "event": "agent_action",
            "agent_id": agent_id,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }

        self._log(log_data, level)

    def log_llm_call(
        self,
        agent_id: str,
        model: str,
        prompt_length: int,
        response_length: int,
        duration: float,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """
        Log an LLM call.

        Args:
            agent_id: Agent ID
            model: LLM model used
            prompt_length: Prompt length in tokens/chars
            response_length: Response length in tokens/chars
            duration: Call duration in seconds
            success: Whether call succeeded
            error: Optional error message
        """
        log_data = {
            "event": "llm_call",
            "agent_id": agent_id,
            "model": model,
            "prompt_length": prompt_length,
            "response_length": response_length,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now().isoformat(),
        }

        if error:
            log_data["error"] = error

        level = "error" if not success else "info"
        self._log(log_data, level)

    def log_task_event(
        self,
        task_id: str,
        event: str,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a task-related event.

        Args:
            task_id: Task ID
            event: Event type (created, assigned, completed, failed)
            agent_id: Optional agent ID
            metadata: Optional metadata
        """
        log_data = {
            "event": "task_event",
            "task_id": task_id,
            "event_type": event,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }

        if agent_id:
            log_data["agent_id"] = agent_id

        self._log(log_data, "info")

    def log_system_event(
        self,
        event: str,
        metadata: Optional[Dict[str, Any]] = None,
        level: str = "info",
    ) -> None:
        """
        Log a system event.

        Args:
            event: Event description
            metadata: Optional metadata
            level: Log level
        """
        log_data = {
            "event": "system_event",
            "description": event,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }

        self._log(log_data, level)

    def _log(self, data: Dict[str, Any], level: str) -> None:
        """
        Internal logging method.

        Args:
            data: Log data dictionary
            level: Log level
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(json.dumps(data, default=str))


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record

        Returns:
            JSON-formatted log string
        """
        # If record.msg is already JSON, return it
        if isinstance(record.msg, str) and record.msg.startswith("{"):
            return record.msg

        # Otherwise, create JSON from record
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data, default=str)
