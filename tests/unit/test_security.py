"""Unit tests for security components."""

from datetime import timedelta

import pytest

from agents_army.security.auth import AuthenticationManager
from agents_army.security.rate_limiter import RateLimiter
from agents_army.protocol.types import AgentRole


class TestAuthenticationManager:
    """Test AuthenticationManager functionality."""

    def test_register_agent(self):
        """Test registering an agent."""
        auth = AuthenticationManager()

        token = auth.register_agent("agent_001", AgentRole.DT)

        assert token is not None
        assert len(token) > 0
        assert "agent_001" in auth.agent_tokens

    def test_authenticate(self):
        """Test authentication."""
        auth = AuthenticationManager()

        token = auth.register_agent("agent_001", AgentRole.BACKEND_ARCHITECT)

        role = auth.authenticate(token)
        assert role == AgentRole.BACKEND_ARCHITECT

        # Invalid token
        assert auth.authenticate("invalid_token") is None

    def test_authorize(self):
        """Test authorization."""
        auth = AuthenticationManager()

        # DT has full access
        assert auth.authorize(AgentRole.DT, "any_action") is True

        # Set permissions for other role
        auth.set_role_permissions(
            AgentRole.BACKEND_ARCHITECT, ["design_architecture", "design_api"]
        )

        assert auth.authorize(AgentRole.BACKEND_ARCHITECT, "design_architecture") is True
        assert auth.authorize(AgentRole.BACKEND_ARCHITECT, "unauthorized_action") is False

    def test_revoke_token(self):
        """Test revoking token."""
        auth = AuthenticationManager()

        token = auth.register_agent("agent_001", AgentRole.DT)

        assert auth.revoke_token(token) is True
        assert auth.authenticate(token) is None

        assert auth.revoke_token("invalid_token") is False


class TestRateLimiter:
    """Test RateLimiter functionality."""

    def test_is_allowed(self):
        """Test rate limiting."""
        limiter = RateLimiter(default_limit=2, default_window=timedelta(seconds=60))

        assert limiter.is_allowed("agent_001") is True
        assert limiter.is_allowed("agent_001") is True
        assert limiter.is_allowed("agent_001") is False  # Exceeded limit

    def test_get_remaining(self):
        """Test getting remaining requests."""
        limiter = RateLimiter(default_limit=5)

        assert limiter.get_remaining("agent_001") == 5

        limiter.is_allowed("agent_001")
        assert limiter.get_remaining("agent_001") == 4

    def test_set_limit(self):
        """Test setting custom limit."""
        limiter = RateLimiter(default_limit=10)

        limiter.set_limit("agent_001", limit=2)

        assert limiter.is_allowed("agent_001") is True
        assert limiter.is_allowed("agent_001") is True
        assert limiter.is_allowed("agent_001") is False

    def test_reset(self):
        """Test resetting rate limit."""
        limiter = RateLimiter(default_limit=2)

        limiter.is_allowed("agent_001")
        limiter.is_allowed("agent_001")

        assert limiter.is_allowed("agent_001") is False

        limiter.reset("agent_001")

        assert limiter.is_allowed("agent_001") is True
