"""Tool Registry for managing and executing tools."""

from typing import Any, Dict, List, Optional

from agents_army.tools.tool import (
    InvalidParametersError,
    Tool,
    ToolExecutionError,
    ToolNotFoundError,
)


class ToolRegistry:
    """
    Registry for managing and executing tools.

    Provides centralized registration, validation, and execution of tools.
    """

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool.

        Args:
            tool: Tool to register

        Raises:
            ValueError: If tool name is already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool

    def unregister(self, tool_name: str) -> None:
        """
        Unregister a tool.

        Args:
            tool_name: Name of tool to unregister
        """
        if tool_name in self._tools:
            del self._tools[tool_name]

    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Tool]:
        """
        List available tools.

        Args:
            category: Optional category filter

        Returns:
            List of tools
        """
        tools = list(self._tools.values())

        if category:
            tools = [tool for tool in tools if tool.category == category]

        return tools

    def has_tool(self, name: str) -> bool:
        """
        Check if a tool is registered.

        Args:
            name: Tool name

        Returns:
            True if tool is registered
        """
        return name in self._tools

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute a tool with validation.

        Args:
            tool_name: Name of tool to execute
            params: Tool parameters

        Returns:
            Tool execution result

        Raises:
            ToolNotFoundError: If tool is not found
            InvalidParametersError: If parameters are invalid
            ToolExecutionError: If execution fails
        """
        tool = self.get_tool(tool_name)

        if not tool:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found")

        # Validate parameters
        try:
            tool.validate_parameters(params)
        except InvalidParametersError as e:
            raise InvalidParametersError(
                f"Invalid parameters for tool '{tool_name}': {str(e)}"
            ) from e

        # Execute tool
        try:
            result = await tool.execute(**params)
            return result
        except Exception as e:
            if isinstance(e, (ToolExecutionError, InvalidParametersError)):
                raise
            raise ToolExecutionError(f"Tool '{tool_name}' execution failed: {str(e)}") from e

    def get_all_tools(self) -> List[Tool]:
        """
        Get all registered tools.

        Returns:
            List of all tools
        """
        return list(self._tools.values())

    def count_tools(self, category: Optional[str] = None) -> int:
        """
        Count registered tools.

        Args:
            category: Optional category filter

        Returns:
            Number of tools
        """
        if category:
            return len([t for t in self._tools.values() if t.category == category])
        return len(self._tools)
