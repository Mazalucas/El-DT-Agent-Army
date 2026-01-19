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
    AgentConflict,
    AgentRegistry,
    AgentSystem,
    ConfigLoader,
    ConflictResolution,
    Project,
    Task,
    TaskAssignment,
    TaskDecomposer,
    TaskResult,
    TaskScheduler,
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
    BrandGuardian,
    ContentCreator,
    DT,
    DevOpsAutomator,
    FeedbackSynthesizer,
    FrontendDeveloper,
    GrowthHacker,
    MarketingStrategist,
    OperationsMaintainer,
    PitchSpecialist,
    ProductStrategist,
    QATester,
    Researcher,
    StorytellingSpecialist,
    UIDesigner,
    UXResearcher,
)

# Memory system
from agents_army.memory import (
    InMemoryBackend,
    InMemoryVectorBackend,
    MemoryAgent,
    MemoryBackend,
    MemorySystem,
    SQLiteBackend,
    VectorBackend,
)

# Tools system
from agents_army.tools import (
    Tool,
    ToolRegistry,
    create_default_tools,
)

# MCP system
from agents_army.mcp import (
    MCPClient,
    MCPServer,
    MCPTool,
)

# Observability
from agents_army.observability import (
    MetricsCollector,
    StructuredLogger,
)

# Security
from agents_army.security import (
    AuthenticationManager,
    RateLimiter,
)

# Cost management
from agents_army.cost import (
    BudgetAlerts,
    CostEstimator,
    CostTracker,
)

__all__ = [
    "__version__",
    # Core
    "Agent",
    "AgentConfig",
    "AgentConflict",
    "AgentRegistry",
    "AgentSystem",
    "ConfigLoader",
    "ConflictResolution",
    "Project",
    "Task",
    "TaskAssignment",
    "TaskDecomposer",
    "TaskResult",
    "TaskScheduler",
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
    "DevOpsAutomator",
    "FrontendDeveloper",
    "ProductStrategist",
    "FeedbackSynthesizer",
    "UXResearcher",
    "UIDesigner",
    "BrandGuardian",
    "ContentCreator",
    "StorytellingSpecialist",
    "PitchSpecialist",
    "GrowthHacker",
    "OperationsMaintainer",
    # Memory
    "MemorySystem",
    "MemoryBackend",
    "InMemoryBackend",
    "SQLiteBackend",
    "VectorBackend",
    "InMemoryVectorBackend",
    "MemoryAgent",
    # Tools
    "Tool",
    "ToolRegistry",
    "create_default_tools",
    # MCP
    "MCPServer",
    "MCPClient",
    "MCPTool",
    # Observability
    "StructuredLogger",
    "MetricsCollector",
    # Security
    "AuthenticationManager",
    "RateLimiter",
    # Cost Management
    "CostTracker",
    "CostEstimator",
    "BudgetAlerts",
]
