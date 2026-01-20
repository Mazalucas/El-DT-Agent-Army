"""Type definitions for the agent communication protocol."""

from enum import Enum
from typing import Literal, Union


class MessageType(str, Enum):
    """Types of messages in the protocol."""

    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    TASK_UPDATE = "task_update"
    ERROR = "error"
    STATUS_QUERY = "status_query"
    STATUS_RESPONSE = "status_response"
    COORDINATION = "coordination"
    VALIDATION_REQUEST = "validation_request"
    VALIDATION_RESPONSE = "validation_response"
    MEMORY_STORE = "memory_store"
    MEMORY_QUERY = "memory_query"
    MEMORY_RESPONSE = "memory_response"
    HEARTBEAT = "heartbeat"
    SHUTDOWN = "shutdown"
    CONFIG_UPDATE = "config_update"


class AgentRole(str, Enum):
    """Roles of agents in the system."""

    DT = "dt"  # Director Técnico (El DT)
    COORDINATOR = "coordinator"  # Legacy name, use DT
    SPECIALIST = "specialist"
    RESEARCHER = "researcher"
    WRITER = "writer"
    ANALYST = "analyst"
    VALIDATOR = "validator"
    MEMORY = "memory"
    TOOL = "tool"
    SUPERVISOR = "supervisor"
    
    # Marketing agents
    MARKETING_STRATEGIST = "marketing_strategist"
    BRAND_GUARDIAN = "brand_guardian"
    CONTENT_CREATOR = "content_creator"
    STORYTELLING_SPECIALIST = "storytelling_specialist"
    PITCH_SPECIALIST = "pitch_specialist"
    GROWTH_HACKER = "growth_hacker"
    
    # Engineering agents
    BACKEND_ARCHITECT = "backend_architect"
    DEVOPS_AUTOMATOR = "devops_automator"
    FRONTEND_DEVELOPER = "frontend_developer"
    
    # Product agents
    PRODUCT_STRATEGIST = "product_strategist"
    FEEDBACK_SYNTHESIZER = "feedback_synthesizer"
    
    # Design agents
    UX_RESEARCHER = "ux_researcher"
    UI_DESIGNER = "ui_designer"
    
    # Testing agents
    QA_TESTER = "qa_tester"
    
    # Operations agents
    OPERATIONS_MAINTAINER = "operations_maintainer"
    
    # Planning agents
    PRD_CREATOR = "prd_creator"
    SRD_CREATOR = "srd_creator"
    DEVELOPMENT_PLANNER = "development_planner"


class Priority(str, Enum):
    """Message priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Encryption(str, Enum):
    """Encryption types for messages."""

    NONE = "none"
    TLS = "tls"
    END_TO_END = "end-to-end"


# Type aliases for convenience
MessageTypeLiteral = Literal[
    "task_request",
    "task_response",
    "task_update",
    "error",
    "status_query",
    "status_response",
    "coordination",
    "validation_request",
    "validation_response",
    "memory_store",
    "memory_query",
    "memory_response",
    "heartbeat",
    "shutdown",
    "config_update",
]

PriorityLiteral = Literal["low", "normal", "high", "critical"]

EncryptionLiteral = Literal["none", "tls", "end-to-end"]
