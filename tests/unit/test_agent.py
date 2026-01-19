"""Unit tests for Agent base class."""

from typing import Any, Optional

import pytest

from agents_army.core.agent import Agent, AgentConfig, LLMProvider
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    def __init__(self):
        self.responses = {}
        self.call_count = 0

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate mock response."""
        self.call_count += 1
        return self.responses.get(prompt, f"Mock response to: {prompt[:50]}...")

    def set_response(self, prompt: str, response: str):
        """Set response for a prompt."""
        self.responses[prompt] = response


class SimpleTestAgent(Agent):
    """Test agent implementation."""

    async def _process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process message for testing."""
        return AgentMessage(
            from_role=self.role,
            to_role=message.from_role,
            type=MessageType.TASK_RESPONSE,
            payload={"status": "processed"},
            reply_to=message.id,
        )


class TestAgentBase:
    """Test Agent base class."""

    def test_create_agent(self):
        """Test creating an agent."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )

        agent = SimpleTestAgent(config)

        assert agent.name == "Test Agent"
        assert agent.role == AgentRole.RESEARCHER
        assert agent.goal == "Test goal"
        assert agent.backstory == "Test backstory"
        assert agent.status == "idle"
        assert agent.is_available is True

    def test_agent_tools(self):
        """Test agent tool management."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        # Register tool
        tool = lambda x: x * 2
        agent.register_tool("multiply", tool)

        # Get tool
        retrieved_tool = agent.get_tool("multiply")
        assert retrieved_tool is not None
        assert retrieved_tool(5) == 10

        # Get available tools
        tools = agent.get_available_tools()
        assert "multiply" in tools

        # Get non-existent tool
        assert agent.get_tool("nonexistent") is None

    def test_agent_context(self):
        """Test agent context management."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        # Set context
        agent.set_context("key1", "value1")
        agent.set_context("key2", 42)

        # Get context
        assert agent.get_context("key1") == "value1"
        assert agent.get_context("key2") == 42
        assert agent.get_context("nonexistent", "default") == "default"

        # Clear context
        agent.clear_context()
        assert agent.get_context("key1") is None

    def test_agent_instructions(self):
        """Test agent instructions generation."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Research topics",
            backstory="You are a researcher",
            instructions="Always cite sources",
        )
        agent = SimpleTestAgent(config)

        instructions = agent.get_instructions()
        assert "Role: researcher" in instructions
        assert "Goal: Research topics" in instructions
        assert "Backstory: You are a researcher" in instructions
        assert "Instructions: Always cite sources" in instructions

    @pytest.mark.asyncio
    async def test_agent_llm_generation(self):
        """Test LLM response generation."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        llm = MockLLMProvider()
        llm.set_response("Test prompt", "Test response")
        agent = SimpleTestAgent(config, llm_provider=llm)

        response = await agent.generate_response("Test prompt")
        assert response == "Test response"
        assert llm.call_count == 1

    @pytest.mark.asyncio
    async def test_agent_llm_no_provider(self):
        """Test LLM generation without provider."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        with pytest.raises(ValueError, match="No LLM provider"):
            await agent.generate_response("Test prompt")

    @pytest.mark.asyncio
    async def test_agent_handle_message(self):
        """Test message handling."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        response = await agent.handle_message(message)

        assert response is not None
        assert response.type == MessageType.TASK_RESPONSE
        assert response.is_reply_to(message)
        assert agent.status == "idle"  # Should be idle after processing
        assert len(agent.get_message_history()) == 1

    @pytest.mark.asyncio
    async def test_agent_handle_message_error(self):
        """Test message handling with error."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )

        class FailingAgent(Agent):
            async def _process_message(self, message: AgentMessage):
                raise ValueError("Test error")

        agent = FailingAgent(config)

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        response = await agent.handle_message(message)

        # Should return error message
        assert response is not None
        assert "error" in response.payload
        assert agent.status == "error"

    def test_agent_lifecycle(self):
        """Test agent lifecycle methods."""
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        # Start
        agent.start()
        assert agent.status == "idle"

        # Stop
        agent.stop()
        assert agent.status == "stopped"
        assert len(agent.get_all_context()) == 0
