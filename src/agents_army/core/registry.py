"""Agent registry for managing agent instances."""

from typing import Dict, List, Optional

from agents_army.core.agent import Agent
from agents_army.protocol.types import AgentRole


class AgentRegistry:
    """
    Registry for managing agent instances.

    Provides centralized registration and lookup of agents by role.
    """

    def __init__(self):
        """Initialize the registry."""
        self._agents: Dict[AgentRole, List[Agent]] = {}
        self._agents_by_id: Dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        """
        Register an agent.

        Args:
            agent: Agent to register

        Raises:
            ValueError: If agent is None or invalid
        """
        if agent is None:
            raise ValueError("Agent cannot be None")

        role = agent.role

        # Add to role-based registry
        if role not in self._agents:
            self._agents[role] = []
        self._agents[role].append(agent)

        # Add to ID-based registry
        self._agents_by_id[agent.id] = agent

    def unregister(self, agent: Agent) -> None:
        """
        Unregister an agent.

        Args:
            agent: Agent to unregister
        """
        role = agent.role

        # Remove from role-based registry
        if role in self._agents and agent in self._agents[role]:
            self._agents[role].remove(agent)
            if not self._agents[role]:
                del self._agents[role]

        # Remove from ID-based registry
        if agent.id in self._agents_by_id:
            del self._agents_by_id[agent.id]

    def get_agent(self, role: AgentRole) -> Optional[Agent]:
        """
        Get the first agent with the specified role.

        Args:
            role: Agent role

        Returns:
            Agent instance or None if not found
        """
        agents = self._agents.get(role, [])
        if agents:
            return agents[0]
        return None

    def get_agents(self, role: AgentRole) -> List[Agent]:
        """
        Get all agents with the specified role.

        Args:
            role: Agent role

        Returns:
            List of agent instances
        """
        return self._agents.get(role, []).copy()

    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """
        Get agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent instance or None if not found
        """
        return self._agents_by_id.get(agent_id)

    def get_all_agents(self) -> List[Agent]:
        """
        Get all registered agents.

        Returns:
            List of all agent instances
        """
        all_agents = []
        for agents in self._agents.values():
            all_agents.extend(agents)
        return all_agents

    def get_registered_roles(self) -> List[AgentRole]:
        """
        Get list of roles with registered agents.

        Returns:
            List of agent roles
        """
        return list(self._agents.keys())

    def has_agent(self, role: AgentRole) -> bool:
        """
        Check if any agent with the role is registered.

        Args:
            role: Agent role

        Returns:
            True if at least one agent with the role is registered
        """
        return role in self._agents and len(self._agents[role]) > 0

    def count_agents(self, role: Optional[AgentRole] = None) -> int:
        """
        Count registered agents.

        Args:
            role: Optional role to filter by

        Returns:
            Number of agents
        """
        if role is None:
            return len(self._agents_by_id)
        return len(self._agents.get(role, []))

    def clear(self) -> None:
        """Clear all registered agents."""
        self._agents.clear()
        self._agents_by_id.clear()
