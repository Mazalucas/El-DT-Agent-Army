"""MCP Server implementation."""

from typing import Any, Dict, List, Optional

from agents_army.mcp.models import MCPResource, MCPServerConfig, MCPTool
from agents_army.protocol.types import AgentRole


class MCPServer:
    """
    MCP Server for registering and managing MCP tools and resources.

    Allows El DT to register tools and resources that can be accessed
    by specific agents via the MCP protocol.
    """

    def __init__(self, config: MCPServerConfig):
        """
        Initialize MCP Server.

        Args:
            config: MCP server configuration
        """
        self.config = config
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}

    async def register_tool(
        self, tool: MCPTool, accessible_by: Optional[List[AgentRole]] = None
    ) -> None:
        """
        Register an MCP tool.

        Args:
            tool: Tool to register
            accessible_by: Optional list of agent roles that can access this tool
                         (None = all agents)
        """
        if accessible_by is not None:
            tool.accessible_by = accessible_by
        elif not tool.accessible_by:
            # Default: accessible by all agents
            tool.accessible_by = []

        self.tools[tool.name] = tool

    async def register_resource(
        self,
        resource: MCPResource,
        accessible_by: Optional[List[AgentRole]] = None,
    ) -> None:
        """
        Register an MCP resource.

        Args:
            resource: Resource to register
            accessible_by: Optional list of agent roles that can access this resource
                         (None = all agents)
        """
        if accessible_by is not None:
            resource.accessible_by = accessible_by
        elif not resource.accessible_by:
            # Default: accessible by all agents
            resource.accessible_by = []

        self.resources[resource.uri] = resource

    async def execute_tool(
        self, tool_name: str, params: Dict[str, Any], agent_role: AgentRole
    ) -> Any:
        """
        Execute an MCP tool.

        Args:
            tool_name: Name of the tool
            params: Tool parameters
            agent_role: Role of agent requesting execution

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found or agent doesn't have access
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        tool = self.tools[tool_name]

        # Check access permissions
        if tool.accessible_by and agent_role not in tool.accessible_by:
            raise ValueError(f"Agent {agent_role.value} does not have access to tool {tool_name}")

        return await tool.execute(params)

    async def read_resource(self, resource_uri: str, agent_role: AgentRole) -> Any:
        """
        Read an MCP resource.

        Args:
            resource_uri: URI of the resource
            agent_role: Role of agent requesting access

        Returns:
            Resource content

        Raises:
            ValueError: If resource not found or agent doesn't have access
        """
        if resource_uri not in self.resources:
            raise ValueError(f"Resource not found: {resource_uri}")

        resource = self.resources[resource_uri]

        # Check access permissions
        if resource.accessible_by and agent_role not in resource.accessible_by:
            raise ValueError(
                f"Agent {agent_role.value} does not have access to resource {resource_uri}"
            )

        return await resource.read()

    def get_tools(self, agent_role: Optional[AgentRole] = None) -> List[MCPTool]:
        """
        Get available tools for an agent.

        Args:
            agent_role: Optional agent role to filter tools

        Returns:
            List of available tools
        """
        if agent_role is None:
            return list(self.tools.values())

        return [
            tool
            for tool in self.tools.values()
            if not tool.accessible_by or agent_role in tool.accessible_by
        ]

    def get_resources(self, agent_role: Optional[AgentRole] = None) -> List[MCPResource]:
        """
        Get available resources for an agent.

        Args:
            agent_role: Optional agent role to filter resources

        Returns:
            List of available resources
        """
        if agent_role is None:
            return list(self.resources.values())

        return [
            resource
            for resource in self.resources.values()
            if not resource.accessible_by or agent_role in resource.accessible_by
        ]

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def list_resources(self) -> List[str]:
        """
        List all registered resource URIs.

        Returns:
            List of resource URIs
        """
        return list(self.resources.keys())


# Allow server.py to be executed directly as a module
# This enables: python -m agents_army.mcp.server
if __name__ == "__main__":
    # Import and run the __main__ module
    import sys
    import importlib.util
    
    # Load and execute __main__.py from the same package
    spec = importlib.util.spec_from_file_location(
        "agents_army.mcp.__main__",
        __file__.replace("server.py", "__main__.py")
    )
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        # Fallback: try importing directly
        from agents_army.mcp import __main__  # noqa: F401
