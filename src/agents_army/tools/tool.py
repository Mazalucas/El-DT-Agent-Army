"""Base Tool class and exceptions."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ToolError(Exception):
    """Base exception for tool errors."""

    pass


class ToolNotFoundError(ToolError):
    """Raised when a tool is not found."""

    pass


class InvalidParametersError(ToolError):
    """Raised when tool parameters are invalid."""

    pass


class ToolExecutionError(ToolError):
    """Raised when tool execution fails."""

    pass


class ToolParameters(BaseModel):
    """Base class for tool parameters."""

    pass


class Tool(ABC):
    """
    Base class for all tools.

    Tools are callable functions that agents can use to perform actions.
    """

    def __init__(
        self,
        name: str,
        description: str,
        category: str = "general",
        parameters_schema: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a tool.

        Args:
            name: Tool name (must be unique)
            description: Tool description
            category: Tool category (e.g., "text", "web", "analysis")
            parameters_schema: Optional JSON schema for parameters
        """
        self.name = name
        self.description = description
        self.category = category
        self.parameters_schema = parameters_schema or {}

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """
        Execute the tool.

        Args:
            **kwargs: Tool parameters

        Returns:
            Tool result

        Raises:
            ToolExecutionError: If execution fails
            InvalidParametersError: If parameters are invalid
        """
        pass

    def validate_parameters(self, params: Dict[str, Any]) -> None:
        """
        Validate tool parameters.

        Args:
            params: Parameters to validate

        Raises:
            InvalidParametersError: If parameters are invalid
        """
        # Basic validation - can be overridden by subclasses
        if self.parameters_schema:
            # Simple validation based on schema
            required = self.parameters_schema.get("required", [])
            for param in required:
                if param not in params:
                    raise InvalidParametersError(f"Missing required parameter: {param}")

    def __call__(self, **kwargs: Any) -> Any:
        """
        Make tool callable.

        Args:
            **kwargs: Tool parameters

        Returns:
            Tool result
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If loop is running, we need to handle this differently
            # For now, raise an error
            raise RuntimeError(
                "Tool execution requires async context. Use await tool.execute() instead."
            )

        return loop.run_until_complete(self.execute(**kwargs))

    def __repr__(self) -> str:
        """String representation of tool."""
        return f"Tool(name={self.name}, category={self.category})"
