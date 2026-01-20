"""Authentication and authorization for Agents_Army."""

from typing import Dict, List, Optional

from agents_army.protocol.types import AgentRole


class AuthenticationManager:
    """
    Manages authentication and authorization for agents.

    Provides basic authentication and role-based access control.
    """

    def __init__(self):
        """Initialize AuthenticationManager."""
        self.agent_tokens: Dict[str, str] = {}  # agent_id -> token
        self.token_roles: Dict[str, AgentRole] = {}  # token -> role
        self.role_permissions: Dict[AgentRole, List[str]] = {}

    def register_agent(self, agent_id: str, role: AgentRole, token: Optional[str] = None) -> str:
        """
        Register an agent and generate authentication token.

        Args:
            agent_id: Agent ID
            role: Agent role
            token: Optional custom token (generates if None)

        Returns:
            Authentication token
        """
        import secrets

        if token is None:
            token = secrets.token_urlsafe(32)

        self.agent_tokens[agent_id] = token
        self.token_roles[token] = role

        return token

    def authenticate(self, token: str) -> Optional[AgentRole]:
        """
        Authenticate using token.

        Args:
            token: Authentication token

        Returns:
            Agent role if authenticated, None otherwise
        """
        return self.token_roles.get(token)

    def authorize(self, role: AgentRole, action: str, resource: Optional[str] = None) -> bool:
        """
        Check if role is authorized for action.

        Args:
            role: Agent role
            action: Action to perform
            resource: Optional resource

        Returns:
            True if authorized, False otherwise
        """
        # Default permissions
        if role == AgentRole.DT:
            return True  # DT has full access

        permissions = self.role_permissions.get(role, [])
        return action in permissions or "*" in permissions

    def set_role_permissions(self, role: AgentRole, permissions: List[str]) -> None:
        """
        Set permissions for a role.

        Args:
            role: Agent role
            permissions: List of allowed actions
        """
        self.role_permissions[role] = permissions

    def revoke_token(self, token: str) -> bool:
        """
        Revoke an authentication token.

        Args:
            token: Token to revoke

        Returns:
            True if revoked, False if not found
        """
        if token in self.token_roles:
            role = self.token_roles.pop(token)
            # Remove from agent_tokens
            agent_id = next((aid for aid, t in self.agent_tokens.items() if t == token), None)
            if agent_id:
                del self.agent_tokens[agent_id]
            return True
        return False
