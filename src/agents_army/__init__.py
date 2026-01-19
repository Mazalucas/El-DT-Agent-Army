"""
Agents_Army: A modular and scalable framework for building multi-agent AI systems.

This package provides a framework for creating and orchestrating multi-agent systems
with clear protocols, defined roles, and governance rules.
"""

__version__ = "0.1.0"
__author__ = "Agents_Army Contributors"

# Core exports
from agents_army.core import (
    Agent,
    AgentConfig,
    AgentRegistry,
    AgentSystem,
    ConfigLoader,
    Project,
    Task,
    TaskAssignment,
    TaskResult,
)
from agents_army.protocol import (
    AgentMessage,
    AgentRole,
    MessageRouter,
    MessageSerializer,
    MessageType,
    Priority,
)

# Agent implementations
from agents_army.agents import (
    BackendArchitect,
    DT,
    MarketingStrategist,
    QATester,
    Researcher,
)

# Memory system
from agents_army.memory import (
    InMemoryBackend,
    MemoryAgent,
    MemoryBackend,
    MemorySystem,
    SQLiteBackend,
)

# Tools system
from agents_army.tools import (
    Tool,
    ToolRegistry,
    create_default_tools,
)

__all__ = [
    "__version__",
    # Core
    "Agent",
    "AgentConfig",
    "AgentRegistry",
    "AgentSystem",
    "ConfigLoader",
    "Project",
    "Task",
    "TaskAssignment",
    "TaskResult",
    # Protocol
    "AgentMessage",
    "AgentRole",
    "MessageRouter",
    "MessageSerializer",
    "MessageType",
    "Priority",
    # Agents
    "DT",
    "Researcher",
    "BackendArchitect",
    "MarketingStrategist",
    "QATester",
    # Memory
    "MemorySystem",
    "MemoryBackend",
    "InMemoryBackend",
    "SQLiteBackend",
    "MemoryAgent",
    # Tools
    "Tool",
    "ToolRegistry",
    "create_default_tools",
]
