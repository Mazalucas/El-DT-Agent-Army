"""Built-in tools for Agents_Army."""

import re
from typing import Any, Dict, List, Optional

from agents_army.tools.registry import ToolRegistry
from agents_army.tools.tool import Tool, ToolExecutionError


class WebSearchTool(Tool):
    """Tool for web search (mock implementation for MVP)."""

    def __init__(self):
        """Initialize web search tool."""
        super().__init__(
            name="web_search",
            description="Search the web for information",
            category="web",
            parameters_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "default": 5,
                        "description": "Maximum number of results",
                    },
                },
                "required": ["query"],
            },
        )

    async def execute(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Execute web search (mock).

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        # Mock implementation - in production would use actual search API
        return [
            {
                "title": f"Result {i} for: {query}",
                "url": f"https://example.com/result{i}",
                "snippet": f"This is a mock result for the query: {query}",
            }
            for i in range(min(max_results, 5))
        ]


class DocumentParserTool(Tool):
    """Tool for parsing documents."""

    def __init__(self):
        """Initialize document parser tool."""
        super().__init__(
            name="document_parser",
            description="Parse documents in various formats",
            category="text",
            parameters_schema={
                "type": "object",
                "properties": {
                    "document": {"type": "string", "description": "Document content"},
                    "format": {
                        "type": "string",
                        "default": "plain",
                        "enum": ["plain", "markdown"],
                        "description": "Document format",
                    },
                },
                "required": ["document"],
            },
        )

    async def execute(self, document: str, format: str = "plain") -> Dict[str, Any]:
        """
        Parse a document.

        Args:
            document: Document content
            format: Document format (plain, markdown)

        Returns:
            Parsed document structure
        """
        if format == "markdown":
            # Simple markdown parsing
            lines = document.split("\n")
            sections = []
            current_section = None

            for line in lines:
                if line.startswith("#"):
                    if current_section:
                        sections.append(current_section)
                    current_section = {"title": line.strip("# "), "content": []}
                elif current_section:
                    current_section["content"].append(line)
                else:
                    if not sections:
                        sections.append({"title": "Content", "content": []})
                    sections[-1]["content"].append(line)

            if current_section:
                sections.append(current_section)

            return {
                "format": "markdown",
                "sections": sections,
                "total_lines": len(lines),
            }
        else:
            # Plain text
            lines = document.split("\n")
            return {
                "format": "plain",
                "content": document,
                "total_lines": len(lines),
                "word_count": len(document.split()),
            }


class TextExtractorTool(Tool):
    """Tool for extracting text from content."""

    def __init__(self):
        """Initialize text extractor tool."""
        super().__init__(
            name="text_extractor",
            description="Extract text from content",
            category="text",
            parameters_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to extract text from"}
                },
                "required": ["content"],
            },
        )

    async def execute(self, content: str) -> str:
        """
        Extract text from content.

        Args:
            content: Content to extract text from

        Returns:
            Extracted text
        """
        # Remove HTML tags if present
        text = re.sub(r"<[^>]+>", "", content)
        # Remove extra whitespace
        text = " ".join(text.split())
        return text


class TextGeneratorTool(Tool):
    """Tool for generating text (wrapper for LLM)."""

    def __init__(self, llm_provider=None):
        """
        Initialize text generator tool.

        Args:
            llm_provider: Optional LLM provider
        """
        super().__init__(
            name="text_generator",
            description="Generate text using LLM",
            category="text",
            parameters_schema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Generation prompt"},
                    "max_tokens": {
                        "type": "integer",
                        "default": 1000,
                        "description": "Maximum tokens to generate",
                    },
                },
                "required": ["prompt"],
            },
        )
        self.llm_provider = llm_provider

    async def execute(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate text.

        Args:
            prompt: Generation prompt
            max_tokens: Maximum tokens

        Returns:
            Generated text
        """
        if not self.llm_provider:
            raise ToolExecutionError("LLM provider not configured")

        return await self.llm_provider.generate(prompt, max_tokens=max_tokens)


class TextFormatterTool(Tool):
    """Tool for formatting text."""

    def __init__(self):
        """Initialize text formatter tool."""
        super().__init__(
            name="text_formatter",
            description="Format text in various styles",
            category="text",
            parameters_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to format"},
                    "format": {
                        "type": "string",
                        "enum": ["markdown", "plain", "html"],
                        "description": "Output format",
                    },
                },
                "required": ["content", "format"],
            },
        )

    async def execute(self, content: str, format: str) -> str:
        """
        Format text.

        Args:
            content: Content to format
            format: Output format (markdown, plain, html)

        Returns:
            Formatted text
        """
        if format == "markdown":
            # Convert plain text to markdown
            lines = content.split("\n")
            formatted = []
            for line in lines:
                line = line.strip()
                if line:
                    formatted.append(line)
                else:
                    formatted.append("")
            return "\n".join(formatted)

        elif format == "html":
            # Convert to HTML
            lines = content.split("\n")
            html_lines = []
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    text = line.lstrip("# ").strip()
                    html_lines.append(f"<h{level}>{text}</h{level}>")
                elif line:
                    html_lines.append(f"<p>{line}</p>")
                else:
                    html_lines.append("<br>")
            return "\n".join(html_lines)

        else:  # plain
            # Just return as-is
            return content


class TextAnalyzerTool(Tool):
    """Tool for analyzing text."""

    def __init__(self):
        """Initialize text analyzer tool."""
        super().__init__(
            name="text_analyzer",
            description="Analyze text and extract statistics",
            category="analysis",
            parameters_schema={
                "type": "object",
                "properties": {"content": {"type": "string", "description": "Content to analyze"}},
                "required": ["content"],
            },
        )

    async def execute(self, content: str) -> Dict[str, Any]:
        """
        Analyze text.

        Args:
            content: Content to analyze

        Returns:
            Analysis results
        """
        words = content.split()
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        return {
            "word_count": len(words),
            "character_count": len(content),
            "character_count_no_spaces": len(content.replace(" ", "")),
            "sentence_count": len(sentences),
            "paragraph_count": len([p for p in content.split("\n\n") if p.strip()]),
            "average_words_per_sentence": len(words) / len(sentences) if sentences else 0,
        }


def create_default_tools(llm_provider=None) -> ToolRegistry:
    """
    Create a ToolRegistry with default tools.

    Args:
        llm_provider: Optional LLM provider for text_generator

    Returns:
        ToolRegistry with default tools registered
    """
    registry = ToolRegistry()

    # Register all default tools
    registry.register(WebSearchTool())
    registry.register(DocumentParserTool())
    registry.register(TextExtractorTool())
    registry.register(TextGeneratorTool(llm_provider=llm_provider))
    registry.register(TextFormatterTool())
    registry.register(TextAnalyzerTool())

    return registry
