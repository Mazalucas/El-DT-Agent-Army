"""MCP models and data structures."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from agents_army.protocol.types import AgentRole


@dataclass
class MCPTool:
    """Represents an MCP tool."""

    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    accessible_by: List[AgentRole] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    async def execute(self, params: Dict[str, Any]) -> Any:
        """
        Execute the tool with given parameters.

        Args:
            params: Tool parameters

        Returns:
            Tool execution result
        """
        raise NotImplementedError("Subclasses must implement execute()")


@dataclass
class MCPResource:
    """Represents an MCP resource."""

    uri: str
    name: str
    description: str
    mime_type: Optional[str] = None
    accessible_by: List[AgentRole] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    async def read(self) -> Any:
        """
        Read the resource.

        Returns:
            Resource content
        """
        raise NotImplementedError("Subclasses must implement read()")


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    server_type: str = "local"  # local | remote | external
    endpoint: Optional[str] = None
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None
    accessible_by: List[AgentRole] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
