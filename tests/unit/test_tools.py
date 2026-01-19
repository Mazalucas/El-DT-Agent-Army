"""Unit tests for tools system."""

import pytest

from agents_army.tools.registry import ToolRegistry
from agents_army.tools.tool import (
    InvalidParametersError,
    Tool,
    ToolExecutionError,
    ToolNotFoundError,
)
from agents_army.tools.tools import (
    DocumentParserTool,
    TextAnalyzerTool,
    TextExtractorTool,
    TextFormatterTool,
    TextGeneratorTool,
    WebSearchTool,
    create_default_tools,
)


class TestTool:
    """Test base Tool class."""

    class SimpleTool(Tool):
        """Simple test tool."""

        def __init__(self):
            super().__init__(
                name="simple_tool",
                description="A simple test tool",
                parameters_schema={"required": ["param1"]},
            )

        async def execute(self, param1: str) -> str:
            """Execute tool."""
            return f"Result: {param1}"

    def test_create_tool(self):
        """Test creating a tool."""
        tool = self.SimpleTool()

        assert tool.name == "simple_tool"
        assert tool.description == "A simple test tool"

    @pytest.mark.asyncio
    async def test_execute_tool(self):
        """Test executing a tool."""
        tool = self.SimpleTool()

        result = await tool.execute(param1="test")
        assert result == "Result: test"

    def test_validate_parameters(self):
        """Test parameter validation."""
        tool = self.SimpleTool()

        # Valid parameters
        tool.validate_parameters({"param1": "value"})

        # Missing required parameter
        with pytest.raises(InvalidParametersError):
            tool.validate_parameters({})


class TestToolRegistry:
    """Test ToolRegistry."""

    def test_register_tool(self):
        """Test registering a tool."""
        registry = ToolRegistry()
        tool = WebSearchTool()

        registry.register(tool)

        assert registry.has_tool("web_search")
        assert registry.get_tool("web_search") == tool

    def test_register_duplicate_tool(self):
        """Test registering duplicate tool raises error."""
        registry = ToolRegistry()
        tool1 = WebSearchTool()
        tool2 = WebSearchTool()

        registry.register(tool1)

        with pytest.raises(ValueError, match="already registered"):
            registry.register(tool2)

    def test_get_tool(self):
        """Test getting a tool."""
        registry = ToolRegistry()
        tool = WebSearchTool()

        registry.register(tool)

        retrieved = registry.get_tool("web_search")
        assert retrieved == tool

        assert registry.get_tool("nonexistent") is None

    def test_list_tools(self):
        """Test listing tools."""
        registry = ToolRegistry()

        registry.register(WebSearchTool())
        registry.register(TextAnalyzerTool())

        tools = registry.list_tools()
        assert len(tools) == 2

        web_tools = registry.list_tools(category="web")
        assert len(web_tools) == 1
        assert web_tools[0].name == "web_search"

    @pytest.mark.asyncio
    async def test_execute_tool(self):
        """Test executing a tool through registry."""
        registry = ToolRegistry()
        registry.register(WebSearchTool())

        result = await registry.execute_tool("web_search", {"query": "test", "max_results": 3})

        assert isinstance(result, list)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_execute_nonexistent_tool(self):
        """Test executing nonexistent tool raises error."""
        registry = ToolRegistry()

        with pytest.raises(ToolNotFoundError):
            await registry.execute_tool("nonexistent", {})

    @pytest.mark.asyncio
    async def test_execute_tool_invalid_params(self):
        """Test executing tool with invalid parameters."""
        registry = ToolRegistry()
        registry.register(WebSearchTool())

        with pytest.raises(InvalidParametersError):
            await registry.execute_tool("web_search", {})


class TestBuiltInTools:
    """Test built-in tools."""

    @pytest.mark.asyncio
    async def test_web_search_tool(self):
        """Test web search tool."""
        tool = WebSearchTool()

        results = await tool.execute(query="AI agents", max_results=3)

        assert isinstance(results, list)
        assert len(results) == 3
        assert "title" in results[0]
        assert "url" in results[0]

    @pytest.mark.asyncio
    async def test_document_parser_tool(self):
        """Test document parser tool."""
        tool = DocumentParserTool()

        result = await tool.execute(document="# Title\n\nContent here", format="markdown")

        assert result["format"] == "markdown"
        assert "sections" in result

    @pytest.mark.asyncio
    async def test_text_extractor_tool(self):
        """Test text extractor tool."""
        tool = TextExtractorTool()

        result = await tool.execute(content="<p>Test content</p>")

        assert result == "Test content"

    @pytest.mark.asyncio
    async def test_text_formatter_tool(self):
        """Test text formatter tool."""
        tool = TextFormatterTool()

        result = await tool.execute(content="Test content", format="markdown")

        assert isinstance(result, str)
        assert "Test content" in result

    @pytest.mark.asyncio
    async def test_text_analyzer_tool(self):
        """Test text analyzer tool."""
        tool = TextAnalyzerTool()

        result = await tool.execute(content="This is a test. It has two sentences.")

        assert result["word_count"] == 8
        assert result["sentence_count"] == 2
        assert "character_count" in result

    def test_create_default_tools(self):
        """Test creating default tools registry."""
        registry = create_default_tools()

        assert registry.count_tools() == 6
        assert registry.has_tool("web_search")
        assert registry.has_tool("text_analyzer")
        assert registry.has_tool("document_parser")
