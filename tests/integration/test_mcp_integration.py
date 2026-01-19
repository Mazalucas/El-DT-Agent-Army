"""Integration tests for MCP with DT."""

import pytest

from agents_army.agents.dt import DT
from agents_army.core.agent import LLMProvider
from agents_army.mcp.models import MCPServerConfig, MCPTool
from agents_army.protocol.types import AgentRole


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    async def generate(self, prompt: str, **kwargs):
        """Generate mock response."""
        return "Mock response"


class MockMCPTool(MCPTool):
    """Mock MCP tool for testing."""

    async def execute(self, params: dict) -> dict:
        """Execute mock tool."""
        return {"result": f"Executed {self.name} with {params}"}


class TestDTMCPIntegration:
    """Test MCP integration with DT."""

    @pytest.mark.asyncio
    async def test_setup_mcp_server(self):
        """Test setting up MCP server."""
        dt = DT(llm_provider=MockLLMProvider())

        config = MCPServerConfig(name="test_server", server_type="local")
        server = await dt.setup_mcp_server(config)

        assert server.config.name == "test_server"
        assert "test_server" in dt.mcp_servers

    @pytest.mark.asyncio
    async def test_register_mcp_tool(self):
        """Test registering MCP tool."""
        dt = DT(llm_provider=MockLLMProvider())

        tool = MockMCPTool(
            name="test_tool",
            description="Test tool",
        )

        await dt.register_mcp_tool(tool)

        # Should create default server
        assert "default" in dt.mcp_servers

        # Get tools for DT
        tools = await dt.get_mcp_tools(AgentRole.DT)
        assert len(tools) == 1
        assert tools[0].name == "test_tool"

    @pytest.mark.asyncio
    async def test_register_mcp_tool_with_access(self):
        """Test registering MCP tool with access restrictions."""
        dt = DT(llm_provider=MockLLMProvider())

        tool = MockMCPTool(
            name="restricted_tool",
            description="Restricted tool",
        )

        await dt.register_mcp_tool(
            tool, accessible_by=[AgentRole.BACKEND_ARCHITECT]
        )

        # DT should not have access
        dt_tools = await dt.get_mcp_tools(AgentRole.DT)
        assert len(dt_tools) == 0

        # Backend Architect should have access
        backend_tools = await dt.get_mcp_tools(AgentRole.BACKEND_ARCHITECT)
        assert len(backend_tools) == 1

    @pytest.mark.asyncio
    async def test_get_mcp_tools_multiple_servers(self):
        """Test getting tools from multiple servers."""
        dt = DT(llm_provider=MockLLMProvider())

        # Setup two servers
        config1 = MCPServerConfig(name="server1")
        await dt.setup_mcp_server(config1)

        config2 = MCPServerConfig(name="server2")
        await dt.setup_mcp_server(config2)

        # Register tools in different servers
        tool1 = MockMCPTool(name="tool1", description="Tool 1")
        await dt.register_mcp_tool(tool1, server_name="server1")

        tool2 = MockMCPTool(name="tool2", description="Tool 2")
        await dt.register_mcp_tool(tool2, server_name="server2")

        # Get all tools
        all_tools = await dt.get_mcp_tools(AgentRole.DT)
        assert len(all_tools) == 2

        # Get tools from specific server
        server1_tools = await dt.get_mcp_tools(AgentRole.DT, server_name="server1")
        assert len(server1_tools) == 1
        assert server1_tools[0].name == "tool1"
