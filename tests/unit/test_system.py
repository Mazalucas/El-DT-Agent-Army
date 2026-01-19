"""Unit tests for AgentSystem."""

import asyncio

import pytest

from agents_army.core.agent import Agent, AgentConfig
from agents_army.core.system import AgentSystem
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class SimpleTestAgent(Agent):
    """Test agent implementation."""

    async def _process_message(self, message):
        return None


class TestAgentSystem:
    """Test AgentSystem class."""

    def test_get_instance(self):
        """Test getting singleton instance."""
        system1 = AgentSystem.get_instance()
        system2 = AgentSystem.get_instance()

        assert system1 is system2
        assert isinstance(system1, AgentSystem)

    def test_register_agent(self):
        """Test registering an agent."""
        system = AgentSystem()
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        system.register_agent(agent)

        assert system.get_agent(AgentRole.RESEARCHER) == agent
        assert system.agents_loaded() is True

    def test_get_agents(self):
        """Test getting agents by role."""
        system = AgentSystem()

        agent1 = SimpleTestAgent(
            AgentConfig(
                name="Agent 1",
                role=AgentRole.RESEARCHER,
                goal="Goal 1",
                backstory="Backstory 1",
            )
        )
        agent2 = SimpleTestAgent(
            AgentConfig(
                name="Agent 2",
                role=AgentRole.RESEARCHER,
                goal="Goal 2",
                backstory="Backstory 2",
            )
        )

        system.register_agent(agent1)
        system.register_agent(agent2)

        agents = system.get_agents(AgentRole.RESEARCHER)
        assert len(agents) == 2
        assert agent1 in agents
        assert agent2 in agents

    def test_get_all_agents(self):
        """Test getting all agents."""
        system = AgentSystem()

        agent1 = SimpleTestAgent(
            AgentConfig(
                name="Agent 1",
                role=AgentRole.RESEARCHER,
                goal="Goal 1",
                backstory="Backstory 1",
            )
        )
        agent2 = SimpleTestAgent(
            AgentConfig(
                name="Agent 2",
                role=AgentRole.WRITER,
                goal="Goal 2",
                backstory="Backstory 2",
            )
        )

        system.register_agent(agent1)
        system.register_agent(agent2)

        all_agents = system.get_all_agents()
        assert len(all_agents) == 2

    @pytest.mark.asyncio
    async def test_send_message(self):
        """Test sending a message."""
        system = AgentSystem()
        received_messages = []

        class MessageHandlerAgent(Agent):
            async def _process_message(self, message):
                received_messages.append(message)
                return None

        agent = MessageHandlerAgent(
            AgentConfig(
                name="Handler",
                role=AgentRole.RESEARCHER,
                goal="Handle messages",
                backstory="Test",
            )
        )

        system.register_agent(agent)
        await system.start()

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": "task_001"},
        )

        await system.send_message(message)
        await asyncio.sleep(0.1)  # Wait for processing

        await system.stop()

        assert len(received_messages) == 1

    def test_get_registered_roles(self):
        """Test getting registered roles."""
        system = AgentSystem()

        agent1 = SimpleTestAgent(
            AgentConfig(
                name="Agent 1",
                role=AgentRole.RESEARCHER,
                goal="Goal 1",
                backstory="Backstory 1",
            )
        )
        agent2 = SimpleTestAgent(
            AgentConfig(
                name="Agent 2",
                role=AgentRole.WRITER,
                goal="Goal 2",
                backstory="Backstory 2",
            )
        )

        system.register_agent(agent1)
        system.register_agent(agent2)

        roles = system.get_registered_roles()
        assert AgentRole.RESEARCHER in roles
        assert AgentRole.WRITER in roles

    def test_health_checks(self):
        """Test health check methods."""
        system = AgentSystem()

        # Initially no agents
        assert system.agents_loaded() is False
        assert system.memory_connected() is False
        assert system.tools_registered() is False

        # Add memory agent
        memory_agent = SimpleTestAgent(
            AgentConfig(
                name="Memory",
                role=AgentRole.MEMORY,
                goal="Store memories",
                backstory="Test",
            )
        )
        system.register_agent(memory_agent)
        assert system.memory_connected() is True

        # Add tool agent
        tool_agent = SimpleTestAgent(
            AgentConfig(
                name="Tool",
                role=AgentRole.TOOL,
                goal="Provide tools",
                backstory="Test",
            )
        )
        system.register_agent(tool_agent)
        assert system.tools_registered() is True
