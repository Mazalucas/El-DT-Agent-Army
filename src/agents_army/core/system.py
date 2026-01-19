"""AgentSystem - Main entry point for the agent framework."""

from typing import Dict, List, Optional

from agents_army.core.agent import Agent, AgentConfig
from agents_army.core.registry import AgentRegistry
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.router import MessageRouter
from agents_army.protocol.types import AgentRole


class AgentSystem:
    """
    Main system for managing agents.

    This is the primary entry point for the Agents_Army framework.
    It manages agent lifecycle, registration, and message routing.
    """

    _instance: Optional["AgentSystem"] = None

    def __init__(self):
        """Initialize the agent system."""
        self.registry = AgentRegistry()
        self.router = MessageRouter()
        self._initialized = False

    @classmethod
    def get_instance(cls) -> "AgentSystem":
        """
        Get the singleton instance of AgentSystem.

        Returns:
            AgentSystem instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        """Initialize the system (start router, etc.)."""
        if self._initialized:
            return

        # Setup router handlers for all registered agents
        for agent in self.registry.get_all_agents():
            self._setup_agent_routing(agent)

        self._initialized = True

    async def start(self) -> None:
        """Start the system (start router, etc.)."""
        await self.router.start()
        self._initialized = True

    async def stop(self) -> None:
        """Stop the system."""
        await self.router.stop()
        self._initialized = False

    def register_agent(self, agent: Agent) -> None:
        """
        Register an agent with the system.

        Args:
            agent: Agent to register
        """
        self.registry.register(agent)
        self._setup_agent_routing(agent)

    def unregister_agent(self, agent: Agent) -> None:
        """
        Unregister an agent from the system.

        Args:
            agent: Agent to unregister
        """
        self.registry.unregister(agent)
        # Note: Router handlers are not automatically removed
        # This could be improved in the future

    def get_agent(self, role: AgentRole) -> Optional[Agent]:
        """
        Get an agent by role.

        Args:
            role: Agent role

        Returns:
            Agent instance or None
        """
        return self.registry.get_agent(role)

    def get_agents(self, role: AgentRole) -> List[Agent]:
        """
        Get all agents with a specific role.

        Args:
            role: Agent role

        Returns:
            List of agent instances
        """
        return self.registry.get_agents(role)

    async def send_message(self, message: AgentMessage) -> None:
        """
        Send a message through the router.

        Args:
            message: Message to send
        """
        await self.router.send(message)

    async def route_message(self, message: AgentMessage) -> None:
        """
        Route a message immediately (bypass queue).

        Args:
            message: Message to route
        """
        await self.router.route(message)

    def _setup_agent_routing(self, agent: Agent) -> None:
        """
        Setup routing for an agent.

        Args:
            agent: Agent to setup routing for
        """
        async def agent_handler(message: AgentMessage):
            """Handler that routes messages to agent."""
            if message.get_to_roles() and agent.role in message.get_to_roles():
                await agent.handle_message(message)

        self.router.register_handler(agent.role, agent_handler)

    def get_registered_roles(self) -> List[AgentRole]:
        """
        Get list of registered agent roles.

        Returns:
            List of agent roles
        """
        return self.registry.get_registered_roles()

    def get_all_agents(self) -> List[Agent]:
        """
        Get all registered agents.

        Returns:
            List of all agents
        """
        return self.registry.get_all_agents()

    def agents_loaded(self) -> bool:
        """
        Check if agents are loaded.

        Returns:
            True if at least one agent is registered
        """
        return len(self.registry.get_all_agents()) > 0

    def memory_connected(self) -> bool:
        """
        Check if memory system is connected.

        Returns:
            True if memory agent is registered
        """
        return self.registry.has_agent(AgentRole.MEMORY)

    def tools_registered(self) -> bool:
        """
        Check if tools are registered.

        Returns:
            True if tool agent is registered
        """
        return self.registry.has_agent(AgentRole.TOOL)
