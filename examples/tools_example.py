"""
Example of using the Tools System.

This example demonstrates:
- Creating and registering tools
- Executing tools through registry
- Using built-in tools
- Tool parameter validation
"""

import asyncio
from agents_army.tools import (
    DocumentParserTool,
    TextAnalyzerTool,
    TextExtractorTool,
    TextFormatterTool,
    ToolRegistry,
    WebSearchTool,
    create_default_tools,
)


async def main():
    """Main example function."""
    print("Tools System Example\n")

    # 1. Create tool registry with default tools
    print("1. Creating tool registry with default tools...")
    registry = create_default_tools()
    print(f"   Registered {registry.count_tools()} tools\n")

    # 2. List all tools
    print("2. Listing all tools...")
    tools = registry.list_tools()
    for tool in tools:
        print(f"   - {tool.name} ({tool.category}): {tool.description}")
    print()

    # 3. Execute web search tool
    print("3. Executing web search tool...")
    search_results = await registry.execute_tool(
        "web_search", {"query": "AI agents", "max_results": 3}
    )
    print(f"   Found {len(search_results)} results:")
    for i, result in enumerate(search_results, 1):
        print(f"     {i}. {result['title']}")
    print()

    # 4. Execute text analyzer tool
    print("4. Executing text analyzer tool...")
    text = "This is a sample text. It has multiple sentences. Let's analyze it!"
    analysis = await registry.execute_tool("text_analyzer", {"content": text})
    print(f"   Analysis results:")
    print(f"     - Word count: {analysis['word_count']}")
    print(f"     - Sentence count: {analysis['sentence_count']}")
    print(f"     - Character count: {analysis['character_count']}")
    print(f"     - Average words per sentence: {analysis['average_words_per_sentence']:.2f}")
    print()

    # 5. Execute document parser tool
    print("5. Executing document parser tool...")
    markdown_doc = """# Introduction

This is the introduction section.

## Features

- Feature 1
- Feature 2

## Conclusion

This is the conclusion.
"""
    parsed = await registry.execute_tool(
        "document_parser", {"document": markdown_doc, "format": "markdown"}
    )
    print(f"   Parsed document:")
    print(f"     - Format: {parsed['format']}")
    print(f"     - Sections: {len(parsed['sections'])}")
    for section in parsed["sections"]:
        print(f"       * {section['title']}")
    print()

    # 6. Execute text formatter tool
    print("6. Executing text formatter tool...")
    plain_text = "Title\n\nThis is content.\n\nMore content here."
    formatted = await registry.execute_tool(
        "text_formatter", {"content": plain_text, "format": "html"}
    )
    print(f"   Formatted text (HTML):")
    print(f"     {formatted[:100]}...")
    print()

    # 7. Execute text extractor tool
    print("7. Executing text extractor tool...")
    html_content = "<div><p>This is <strong>important</strong> content.</p></div>"
    extracted = await registry.execute_tool("text_extractor", {"content": html_content})
    print(f"   Extracted text: {extracted}")
    print()

    # 8. Test tool categories
    print("8. Listing tools by category...")
    web_tools = registry.list_tools(category="web")
    text_tools = registry.list_tools(category="text")
    analysis_tools = registry.list_tools(category="analysis")

    print(f"   Web tools: {len(web_tools)}")
    print(f"   Text tools: {len(text_tools)}")
    print(f"   Analysis tools: {len(analysis_tools)}")
    print()

    # 9. Test error handling
    print("9. Testing error handling...")
    try:
        await registry.execute_tool("nonexistent_tool", {})
    except Exception as e:
        print(f"   Caught expected error: {type(e).__name__}")

    try:
        await registry.execute_tool("web_search", {})  # Missing required parameter
    except Exception as e:
        print(f"   Caught expected error: {type(e).__name__}")
    print()

    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
