"""Tests for TaskSessionManager."""

import tempfile
from datetime import datetime, timedelta

import pytest

from agents_army.core.session_manager import (
    SessionResetReason,
    TaskSession,
    TaskSessionManager,
)
from agents_army.core.task_storage import TaskStorage
from agents_army.protocol.types import AgentRole


class TestTaskSessionManager:
    """Tests for TaskSessionManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def session_manager(self, temp_dir):
        """Create TaskSessionManager instance."""
        storage = TaskStorage(temp_dir)
        return TaskSessionManager(storage, expiration_hours=24)

    def test_get_or_create_session_new(self, session_manager):
        """Test creating new session."""
        session = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        assert session.task_id == "test_task"
        assert session.agent_role == AgentRole.BACKEND_ARCHITECT
        assert len(session.iterations) == 0

    def test_get_or_create_session_existing(self, session_manager):
        """Test getting existing session."""
        session1 = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        session2 = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        assert session1.task_id == session2.task_id
        assert session1.agent_role == session2.agent_role

    def test_get_or_create_session_agent_changed(self, session_manager):
        """Test session reset when agent changes."""
        session1 = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        session2 = session_manager.get_or_create_session(
            "test_task", AgentRole.FRONTEND_DEVELOPER
        )
        
        # Should create new session when agent changes
        assert session2.agent_role == AgentRole.FRONTEND_DEVELOPER

    def test_should_reset_session_circuit_breaker(self, session_manager):
        """Test should_reset_session for circuit breaker."""
        session = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        should_reset = session_manager.should_reset_session(
            session, SessionResetReason.CIRCUIT_BREAKER_OPEN
        )
        
        assert should_reset is True

    def test_should_reset_session_expired(self, session_manager):
        """Test should_reset_session for expired session."""
        session = TaskSession(
            task_id="test_task",
            agent_role=AgentRole.BACKEND_ARCHITECT,
            created_at=datetime.now() - timedelta(hours=25),
            last_accessed=datetime.now() - timedelta(hours=25),
        )
        
        should_reset = session_manager.should_reset_session(
            session, SessionResetReason.SESSION_EXPIRED
        )
        
        assert should_reset is True

    def test_store_context(self, session_manager):
        """Test storing context."""
        session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        context = {"key1": "value1", "key2": "value2"}
        session_manager.store_context("test_task", context)
        
        retrieved = session_manager.get_context("test_task")
        assert retrieved["key1"] == "value1"
        assert retrieved["key2"] == "value2"

    def test_get_context_empty(self, session_manager):
        """Test getting context for non-existent session."""
        context = session_manager.get_context("non_existent")
        assert context == {}

    def test_add_iteration(self, session_manager):
        """Test adding iteration to session."""
        session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        session_manager.add_iteration(
            "test_task",
            iteration=1,
            agent_output="Output",
            file_changes=["file1.py"],
            errors=[],
        )
        
        # Session should have iteration
        session = session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        assert len(session.iterations) == 1

    def test_reset_session(self, session_manager):
        """Test resetting session."""
        session_manager.get_or_create_session(
            "test_task", AgentRole.BACKEND_ARCHITECT
        )
        
        session_manager.store_context("test_task", {"key": "value"})
        assert session_manager.get_context("test_task") != {}
        
        session_manager.reset_session("test_task", "test_reason")
        
        # Context should be cleared
        assert session_manager.get_context("test_task") == {}
