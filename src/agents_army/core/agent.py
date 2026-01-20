"""Base Agent class for all agents in the system."""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate a response from the LLM."""
        pass


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    name: str
    role: AgentRole
    goal: str
    backstory: str
    instructions: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    verbose: bool = True
    allow_delegation: bool = False
    max_iterations: int = 3
    department: Optional[str] = None


class Agent(ABC):
    """
    Base class for all agents in the system.

    This class provides the foundation for all agents, including:
    - Configuration (role, goal, backstory)
    - LLM integration
    - Tool management
    - Context management
    - Message handling
    """

    def __init__(
        self,
        config: AgentConfig,
        llm_provider: Optional[LLMProvider] = None,
    ):
        """
        Initialize an agent.

        Args:
            config: Agent configuration
            llm_provider: Optional LLM provider (for testing/mocking)
        """
        self.config = config
        self.id = f"agent_{uuid.uuid4().hex[:8]}"
        self.llm_provider = llm_provider
        self._tools: Dict[str, Any] = {}
        self._context: Dict[str, Any] = {}
        self._status = "idle"  # idle, busy, error, stopped
        self._message_history: List[AgentMessage] = []

    @property
    def name(self) -> str:
        """Get agent name."""
        return self.config.name

    @property
    def role(self) -> AgentRole:
        """Get agent role."""
        return self.config.role

    @property
    def goal(self) -> str:
        """Get agent goal."""
        return self.config.goal

    @property
    def backstory(self) -> str:
        """Get agent backstory."""
        return self.config.backstory

    @property
    def status(self) -> str:
        """Get agent status."""
        return self._status

    @property
    def is_available(self) -> bool:
        """Check if agent is available for new tasks."""
        return self._status == "idle"

    def register_tool(self, name: str, tool: Any) -> None:
        """
        Register a tool for this agent.

        Args:
            name: Tool name
            tool: Tool object (must be callable or have execute method)
        """
        self._tools[name] = tool

    def get_tool(self, name: str) -> Optional[Any]:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool object or None if not found
        """
        return self._tools.get(name)

    def get_available_tools(self) -> List[str]:
        """
        Get list of available tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def set_context(self, key: str, value: Any) -> None:
        """
        Set context value.

        Args:
            key: Context key
            value: Context value
        """
        self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Get context value.

        Args:
            key: Context key
            default: Default value if key not found

        Returns:
            Context value or default
        """
        return self._context.get(key, default)

    def clear_context(self) -> None:
        """Clear all context."""
        self._context.clear()

    def get_all_context(self) -> Dict[str, Any]:
        """
        Get all context.

        Returns:
            Dictionary with all context
        """
        return self._context.copy()

    async def handle_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """
        Handle an incoming message.

        This is the main entry point for agent communication.
        Subclasses should override this to implement specific behavior.

        Args:
            message: Incoming message

        Returns:
            Optional response message
        """
        self._message_history.append(message)
        self._status = "busy"

        try:
            response = await self._process_message(message)
            return response
        except Exception as e:
            self._status = "error"
            # Create error message
            error_message = AgentMessage(
                from_role=self.role,
                to_role=message.from_role,
                type=message.type,  # Use same type for error response
                payload={
                    "error": str(e),
                    "original_message_id": message.id,
                },
                reply_to=message.id,
            )
            return error_message
        finally:
            if self._status == "busy":
                self._status = "idle"

    @abstractmethod
    async def _process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """
        Process a message (to be implemented by subclasses).

        Args:
            message: Message to process

        Returns:
            Optional response message
        """
        pass

    async def generate_response(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate a response using the LLM.

        Args:
            prompt: Input prompt
            **kwargs: Additional arguments for LLM

        Returns:
            Generated response

        Raises:
            ValueError: If no LLM provider is configured
        """
        if self.llm_provider is None:
            raise ValueError("No LLM provider configured")

        return await self.llm_provider.generate(prompt, **kwargs)

    def get_instructions(self) -> str:
        """
        Get full instructions for this agent.

        Combines role, goal, backstory, and custom instructions.

        Returns:
            Complete instruction string
        """
        parts = [
            f"Role: {self.role.value}",
            f"Goal: {self.goal}",
            f"Backstory: {self.backstory}",
        ]

        if self.config.instructions:
            parts.append(f"Instructions: {self.config.instructions}")

        return "\n".join(parts)

    def get_message_history(self, limit: Optional[int] = None) -> List[AgentMessage]:
        """
        Get message history.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        if limit is None:
            return self._message_history.copy()
        return self._message_history[-limit:]

    def start(self) -> None:
        """Start the agent."""
        self._status = "idle"

    def stop(self) -> None:
        """Stop the agent."""
        self._status = "stopped"
        self.clear_context()

    def __repr__(self) -> str:
        """String representation of agent."""
        return f"Agent(name={self.name}, role={self.role.value}, status={self.status})"
