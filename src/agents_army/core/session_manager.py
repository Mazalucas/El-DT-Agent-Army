"""Session management for autonomous task execution."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents_army.core.task_storage import TaskStorage
from agents_army.protocol.types import AgentRole


class SessionResetReason(str, Enum):
    """Reasons for resetting a session."""

    CIRCUIT_BREAKER_OPEN = "circuit_breaker_open"
    MANUAL_INTERRUPT = "manual_interrupt"
    PROJECT_COMPLETE = "project_complete"
    SESSION_EXPIRED = "session_expired"
    AGENT_CHANGED = "agent_changed"


@dataclass
class TaskSession:
    """Session data for a task execution."""

    task_id: str
    agent_role: AgentRole
    created_at: datetime
    last_accessed: datetime
    iterations: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "agent_role": self.agent_role.value,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "iterations": self.iterations,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskSession":
        """Create from dictionary."""
        return cls(
            task_id=data["task_id"],
            agent_role=AgentRole(data["agent_role"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            iterations=data.get("iterations", []),
            context=data.get("context", {}),
        )

    def is_expired(self, expiration_hours: int) -> bool:
        """
        Check if session is expired.

        Args:
            expiration_hours: Hours until expiration

        Returns:
            True if expired
        """
        expiration_time = self.last_accessed + timedelta(hours=expiration_hours)
        return datetime.now() > expiration_time


class TaskSessionManager:
    """Manages persistent sessions for task execution."""

    def __init__(
        self,
        task_storage: TaskStorage,
        expiration_hours: int = 24,
        memory_system: Optional[Any] = None,
    ):
        """
        Initialize session manager.

        Args:
            task_storage: TaskStorage instance
            expiration_hours: Hours until session expiration
            memory_system: Optional MemorySystem for enhanced context storage
        """
        self.task_storage = task_storage
        self.expiration_hours = expiration_hours
        self.memory_system = memory_system
        self.sessions_dir = Path(task_storage.project_path) / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_file(self, task_id: str) -> Path:
        """
        Get path to session file.

        Args:
            task_id: Task ID

        Returns:
            Path to session file
        """
        return self.sessions_dir / f"{task_id}.json"

    def get_or_create_session(
        self, task_id: str, agent_role: AgentRole
    ) -> TaskSession:
        """
        Get existing session or create new one.

        Args:
            task_id: Task ID
            agent_role: Agent role

        Returns:
            TaskSession instance
        """
        session_file = self._get_session_file(task_id)

        # Try to load existing session
        if session_file.exists():
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    session = TaskSession.from_dict(data)

                    # Check if agent changed
                    if session.agent_role != agent_role:
                        # Reset session if agent changed
                        return self._create_new_session(task_id, agent_role)

                    # Check if expired
                    if session.is_expired(self.expiration_hours):
                        # Reset expired session
                        return self._create_new_session(task_id, agent_role)

                    # Update last accessed
                    session.last_accessed = datetime.now()
                    self._save_session(session)
                    return session
            except Exception:
                # If loading fails, create new session
                pass

        # Create new session
        return self._create_new_session(task_id, agent_role)

    def _create_new_session(self, task_id: str, agent_role: AgentRole) -> TaskSession:
        """
        Create a new session.

        Args:
            task_id: Task ID
            agent_role: Agent role

        Returns:
            New TaskSession
        """
        now = datetime.now()
        session = TaskSession(
            task_id=task_id,
            agent_role=agent_role,
            created_at=now,
            last_accessed=now,
            iterations=[],
            context={},
        )
        self._save_session(session)
        return session

    def should_reset_session(
        self, session: TaskSession, reason: SessionResetReason
    ) -> bool:
        """
        Determine if session should be reset.

        Args:
            session: Current session
            reason: Reason for potential reset

        Returns:
            True if should reset
        """
        # Always reset for these reasons
        if reason in [
            SessionResetReason.CIRCUIT_BREAKER_OPEN,
            SessionResetReason.MANUAL_INTERRUPT,
            SessionResetReason.PROJECT_COMPLETE,
            SessionResetReason.AGENT_CHANGED,
        ]:
            return True

        # Check expiration
        if reason == SessionResetReason.SESSION_EXPIRED:
            return session.is_expired(self.expiration_hours)

        return False

    def store_context(self, task_id: str, context: Dict[str, Any]) -> None:
        """
        Store context for a task session.

        Args:
            task_id: Task ID
            context: Context dictionary to store
        """
        session_file = self._get_session_file(task_id)
        if not session_file.exists():
            return

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                session = TaskSession.from_dict(data)

            # Merge context
            session.context.update(context)
            session.last_accessed = datetime.now()

            self._save_session(session)

            # Also store in memory system if available
            if self.memory_system:
                try:
                    # Store context in memory system
                    self.memory_system.store(
                        key=f"session_context_{task_id}",
                        value=context,
                        memory_type="session_context",
                    )
                except Exception:
                    pass  # Fail silently if memory system unavailable
        except Exception:
            pass  # Fail silently if can't update

    def get_context(self, task_id: str) -> Dict[str, Any]:
        """
        Get context for a task session.

        Args:
            task_id: Task ID

        Returns:
            Context dictionary
        """
        session_file = self._get_session_file(task_id)
        if not session_file.exists():
            return {}

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                session = TaskSession.from_dict(data)
                return session.context.copy()
        except Exception:
            return {}

    def add_iteration(
        self,
        task_id: str,
        iteration: int,
        agent_output: str,
        file_changes: List[str],
        errors: List[str],
    ) -> None:
        """
        Add iteration record to session.

        Args:
            task_id: Task ID
            iteration: Iteration number
            agent_output: Output from agent
            file_changes: List of changed files
            errors: List of errors
        """
        session_file = self._get_session_file(task_id)
        if not session_file.exists():
            return

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                session = TaskSession.from_dict(data)

            # Add iteration record
            session.iterations.append(
                {
                    "iteration": iteration,
                    "timestamp": datetime.now().isoformat(),
                    "agent_output": agent_output[:1000],  # Limit size
                    "file_changes": file_changes,
                    "errors": errors,
                }
            )

            # Keep only last 50 iterations
            if len(session.iterations) > 50:
                session.iterations = session.iterations[-50:]

            session.last_accessed = datetime.now()
            self._save_session(session)
        except Exception:
            pass  # Fail silently if can't update

    def reset_session(self, task_id: str, reason: str) -> None:
        """
        Reset session for a task.

        Args:
            task_id: Task ID
            reason: Reason for reset
        """
        session_file = self._get_session_file(task_id)
        if session_file.exists():
            session_file.unlink()

        # Also clear from memory system if available
        if self.memory_system:
            try:
                self.memory_system.delete(f"session_context_{task_id}")
            except Exception:
                pass

    def _save_session(self, session: TaskSession) -> None:
        """
        Save session to disk.

        Args:
            session: Session to save
        """
        session_file = self._get_session_file(session.task_id)
        try:
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Fail silently if can't save
