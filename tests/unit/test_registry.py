"""Unit tests for AgentRegistry."""

import pytest
from agents_army.core.agent import Agent, AgentConfig
from agents_army.core.registry import AgentRegistry
from agents_army.protocol.types import AgentRole


class SimpleTestAgent(Agent):
    """Test agent implementation."""

    async def _process_message(self, message):
        return None


class TestAgentRegistry:
    """Test AgentRegistry class."""

    def test_register_agent(self):
        """Test registering an agent."""
        registry = AgentRegistry()
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        registry.register(agent)

        assert registry.has_agent(AgentRole.RESEARCHER)
        assert registry.count_agents() == 1
        assert registry.get_agent(AgentRole.RESEARCHER) == agent

    def test_register_multiple_agents_same_role(self):
        """Test registering multiple agents with same role."""
        registry = AgentRegistry()

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

        registry.register(agent1)
        registry.register(agent2)

        agents = registry.get_agents(AgentRole.RESEARCHER)
        assert len(agents) == 2
        assert agent1 in agents
        assert agent2 in agents

    def test_unregister_agent(self):
        """Test unregistering an agent."""
        registry = AgentRegistry()
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        registry.register(agent)
        assert registry.has_agent(AgentRole.RESEARCHER)

        registry.unregister(agent)
        assert not registry.has_agent(AgentRole.RESEARCHER)
        assert registry.count_agents() == 0

    def test_get_agent_by_id(self):
        """Test getting agent by ID."""
        registry = AgentRegistry()
        config = AgentConfig(
            name="Test Agent",
            role=AgentRole.RESEARCHER,
            goal="Test goal",
            backstory="Test backstory",
        )
        agent = SimpleTestAgent(config)

        registry.register(agent)

        retrieved = registry.get_agent_by_id(agent.id)
        assert retrieved == agent

    def test_get_all_agents(self):
        """Test getting all agents."""
        registry = AgentRegistry()

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

        registry.register(agent1)
        registry.register(agent2)

        all_agents = registry.get_all_agents()
        assert len(all_agents) == 2
        assert agent1 in all_agents
        assert agent2 in all_agents

    def test_get_registered_roles(self):
        """Test getting registered roles."""
        registry = AgentRegistry()

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

        registry.register(agent1)
        registry.register(agent2)

        roles = registry.get_registered_roles()
        assert AgentRole.RESEARCHER in roles
        assert AgentRole.WRITER in roles

    def test_clear_registry(self):
        """Test clearing the registry."""
        registry = AgentRegistry()

        agent = SimpleTestAgent(
            AgentConfig(
                name="Test Agent",
                role=AgentRole.RESEARCHER,
                goal="Test goal",
                backstory="Test backstory",
            )
        )

        registry.register(agent)
        assert registry.count_agents() == 1

        registry.clear()
        assert registry.count_agents() == 0
        assert not registry.has_agent(AgentRole.RESEARCHER)

    def test_register_none(self):
        """Test registering None raises error."""
        registry = AgentRegistry()

        with pytest.raises(ValueError, match="Agent cannot be None"):
            registry.register(None)
