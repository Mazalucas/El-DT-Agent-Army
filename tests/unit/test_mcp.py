"""Unit tests for MCP Server."""

import pytest

from agents_army.mcp.models import MCPServerConfig, MCPResource, MCPTool
from agents_army.mcp.server import MCPServer
from agents_army.protocol.types import AgentRole


class MockMCPTool(MCPTool):
    """Mock MCP tool for testing."""

    async def execute(self, params: dict) -> dict:
        """Execute mock tool."""
        return {"result": f"Executed {self.name} with {params}"}


class MockMCPResource(MCPResource):
    """Mock MCP resource for testing."""

    async def read(self) -> dict:
        """Read mock resource."""
        return {"content": f"Content from {self.uri}"}


class TestMCPServer:
    """Test MCP Server functionality."""

    def test_create_server(self):
        """Test creating MCP server."""
        config = MCPServerConfig(name="test_server", server_type="local")
        server = MCPServer(config)

        assert server.config.name == "test_server"
        assert len(server.tools) == 0
        assert len(server.resources) == 0

    @pytest.mark.asyncio
    async def test_register_tool(self):
        """Test registering a tool."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool = MockMCPTool(
            name="test_tool",
            description="Test tool",
            parameters={"param1": "string"},
        )

        await server.register_tool(tool)

        assert "test_tool" in server.tools
        assert server.tools["test_tool"] == tool

    @pytest.mark.asyncio
    async def test_register_tool_with_access(self):
        """Test registering tool with access restrictions."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool = MockMCPTool(
            name="restricted_tool",
            description="Restricted tool",
        )

        await server.register_tool(
            tool, accessible_by=[AgentRole.BACKEND_ARCHITECT]
        )

        assert tool.accessible_by == [AgentRole.BACKEND_ARCHITECT]

    @pytest.mark.asyncio
    async def test_execute_tool(self):
        """Test executing a tool."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool = MockMCPTool(
            name="test_tool",
            description="Test tool",
        )
        await server.register_tool(tool)

        result = await server.execute_tool(
            "test_tool", {"param": "value"}, AgentRole.DT
        )

        assert "result" in result
        assert "test_tool" in result["result"]

    @pytest.mark.asyncio
    async def test_execute_tool_access_denied(self):
        """Test executing tool with access denied."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool = MockMCPTool(
            name="restricted_tool",
            description="Restricted tool",
        )
        await server.register_tool(
            tool, accessible_by=[AgentRole.BACKEND_ARCHITECT]
        )

        with pytest.raises(ValueError, match="does not have access"):
            await server.execute_tool(
                "restricted_tool", {}, AgentRole.FRONTEND_DEVELOPER
            )

    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self):
        """Test executing non-existent tool."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        with pytest.raises(ValueError, match="Tool not found"):
            await server.execute_tool("nonexistent", {}, AgentRole.DT)

    @pytest.mark.asyncio
    async def test_register_resource(self):
        """Test registering a resource."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        resource = MockMCPResource(
            uri="resource://test",
            name="Test Resource",
            description="Test resource",
        )

        await server.register_resource(resource)

        assert "resource://test" in server.resources

    @pytest.mark.asyncio
    async def test_read_resource(self):
        """Test reading a resource."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        resource = MockMCPResource(
            uri="resource://test",
            name="Test Resource",
            description="Test resource",
        )
        await server.register_resource(resource)

        content = await server.read_resource("resource://test", AgentRole.DT)

        assert "content" in content

    def test_get_tools(self):
        """Test getting tools for an agent."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool1 = MockMCPTool(name="tool1", description="Tool 1")
        tool2 = MockMCPTool(
            name="tool2",
            description="Tool 2",
            accessible_by=[AgentRole.BACKEND_ARCHITECT],
        )

        # Register tools synchronously for this test
        import asyncio

        async def register():
            await server.register_tool(tool1)
            await server.register_tool(tool2)

        asyncio.run(register())

        # Get tools for DT (should get tool1 only, tool2 is restricted)
        dt_tools = server.get_tools(AgentRole.DT)
        assert len(dt_tools) == 1
        assert dt_tools[0].name == "tool1"

        # Get tools for Backend Architect (should get both)
        backend_tools = server.get_tools(AgentRole.BACKEND_ARCHITECT)
        assert len(backend_tools) == 2

    def test_list_tools(self):
        """Test listing tools."""
        config = MCPServerConfig(name="test_server")
        server = MCPServer(config)

        tool1 = MockMCPTool(name="tool1", description="Tool 1")
        tool2 = MockMCPTool(name="tool2", description="Tool 2")

        import asyncio

        async def register():
            await server.register_tool(tool1)
            await server.register_tool(tool2)

        asyncio.run(register())

        tool_names = server.list_tools()
        assert "tool1" in tool_names
        assert "tool2" in tool_names
        assert len(tool_names) == 2
