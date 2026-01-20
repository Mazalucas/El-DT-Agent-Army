"""Data models for tasks, projects, and related entities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents_army.protocol.types import AgentRole


@dataclass
class Task:
    """Represents a task in the system."""

    id: str
    title: str
    description: str
    status: str = "pending"  # pending | in-progress | done | blocked
    priority: int = 3  # 1-5, 5 is highest
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Task IDs
    assigned_agent: Optional[AgentRole] = None
    subtasks: List["Task"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_ready(self) -> bool:
        """Check if task is ready to be executed (dependencies met)."""
        return len(self.dependencies) == 0

    def add_dependency(self, task_id: str) -> None:
        """Add a dependency."""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)

    def remove_dependency(self, task_id: str) -> None:
        """Remove a dependency."""
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)

    def update_status(self, new_status: str) -> None:
        """Update task status."""
        self.status = new_status
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "assigned_agent": self.assigned_agent.value if self.assigned_agent else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        assigned_agent = None
        if data.get("assigned_agent"):
            assigned_agent = AgentRole(data["assigned_agent"])

        task = cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=data.get("status", "pending"),
            priority=data.get("priority", 3),
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            assigned_agent=assigned_agent,
            metadata=data.get("metadata", {}),
        )

        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            task.updated_at = datetime.fromisoformat(data["updated_at"])

        return task


@dataclass
class Project:
    """Represents a project managed by El DT."""

    name: str
    description: str
    path: str  # .dt directory
    prd_path: str
    rules: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "path": self.path,
            "prd_path": self.prd_path,
            "rules": self.rules,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create project from dictionary."""
        project = cls(
            name=data["name"],
            description=data["description"],
            path=data["path"],
            prd_path=data["prd_path"],
            rules=data.get("rules", []),
        )

        if "created_at" in data:
            project.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            project.updated_at = datetime.fromisoformat(data["updated_at"])

        return project


@dataclass
class TaskResult:
    """Result of task execution."""

    task_id: str
    status: str  # completed | failed | partial
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    agent_id: Optional[str] = None
    quality_score: Optional[float] = None  # 0.0 - 1.0
    tokens_used: Optional[int] = None
    duration: Optional[float] = None  # seconds
    created_at: datetime = field(default_factory=datetime.now)

    def is_successful(self) -> bool:
        """Check if result is successful."""
        return self.status == "completed" and self.error is None


@dataclass
class TaskAssignment:
    """Represents assignment of a task to an agent."""

    task_id: str
    agent_role: AgentRole
    assigned_at: datetime = field(default_factory=datetime.now)
    status: str = "assigned"  # assigned | in-progress | completed | failed


# Autonomy Engine Models


@dataclass
class Situation:
    """Represents a situation requiring autonomous decision."""

    task: Task
    context: Dict[str, Any] = field(default_factory=dict)
    available_agents: List[AgentRole] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SituationAnalysis:
    """Analysis of a situation."""

    task_type: str
    complexity: str  # low | medium | high
    agents_available: List[AgentRole] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    resources_required: Dict[str, Any] = field(default_factory=dict)
    time_available: Optional[float] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfidenceScore:
    """Confidence score for autonomous action."""

    score: float  # 0.0 - 1.0
    factors: Dict[str, float] = field(default_factory=dict)
    explanation: str = ""


@dataclass
class RiskAssessment:
    """Risk assessment for autonomous action."""

    total_risk: float  # 0.0 - 1.0
    risk_factors: Dict[str, float] = field(default_factory=dict)
    level: str = "low"  # low | medium | high | critical
    explanation: str = ""


@dataclass
class Decision:
    """Decision made by autonomy engine."""

    autonomous: bool
    confidence: float
    risk: float
    action: str
    reasoning: str = ""
    escalation_reason: Optional[str] = None
    level: int = 4  # 1-4, 4 = fully autonomous


@dataclass
class ActionResult:
    """Result of autonomous action."""

    success: bool
    action_taken: str
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    escalated: bool = False
    escalation_reason: Optional[str] = None


# Conflict Resolution Models


@dataclass
class AgentConflict:
    """Represents a conflict between agents."""

    conflict_id: str
    task_id: str
    conflicting_agents: List[AgentRole]
    conflict_type: str  # opinion | resource | priority | approach
    description: str
    agent_opinions: Dict[AgentRole, Dict[str, Any]] = field(default_factory=dict)
    severity: str = "medium"  # low | medium | high | critical
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ConflictResolution:
    """Resolution for an agent conflict."""

    conflict_id: str
    resolution_type: str  # merge | choose_one | compromise | escalate
    chosen_approach: Dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""
    resolved_by: AgentRole = AgentRole.DT
    resolved_at: datetime = field(default_factory=datetime.now)
    success: bool = True
