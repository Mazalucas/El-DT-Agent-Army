# Estructura del Proyecto: Agents_Army

## 📁 Organización del Proyecto

```
Agents_Army/
├── src/
│   └── agents_army/              # Código fuente principal
│       ├── __init__.py           # Exports principales
│       ├── py.typed               # Marker para type checkers
│       ├── protocol/             # Protocolo de comunicación
│       │   ├── __init__.py
│       │   ├── message.py        # AgentMessage
│       │   ├── router.py         # MessageRouter
│       │   ├── serializer.py     # MessageSerializer
│       │   └── types.py          # Tipos y enums
│       ├── core/                 # Componentes core
│       │   ├── __init__.py
│       │   ├── agent.py          # Clase base Agent
│       │   ├── system.py        # AgentSystem
│       │   ├── registry.py       # AgentRegistry
│       │   ├── config.py         # ConfigLoader
│       │   ├── models.py         # Task, Project, etc.
│       │   ├── task_storage.py   # TaskStorage
│       │   └── rules.py          # Sistema de reglas
│       ├── agents/               # Implementaciones de agentes
│       │   ├── __init__.py
│       │   ├── dt.py             # El DT (Director Técnico)
│       │   ├── researcher.py     # Researcher
│       │   ├── backend_architect.py
│       │   ├── marketing_strategist.py
│       │   └── qa_tester.py
│       ├── memory/               # Sistema de memoria
│       │   ├── __init__.py
│       │   ├── system.py         # MemorySystem
│       │   ├── backend.py        # Backends (InMemory, SQLite)
│       │   ├── models.py         # MemoryItem, RetentionPolicy
│       │   └── memory_agent.py   # MemoryAgent
│       └── tools/                # Sistema de herramientas
│           ├── __init__.py
│           ├── tool.py           # Clase base Tool
│           ├── registry.py        # ToolRegistry
│           └── tools.py           # Herramientas built-in
│
├── tests/                         # Tests (109 tests pasando)
│   ├── __init__.py
│   ├── conftest.py               # Configuración pytest
│   ├── unit/                     # Unit tests (90+ tests)
│   │   ├── test_agent.py
│   │   ├── test_config.py
│   │   ├── test_dt.py
│   │   ├── test_memory.py
│   │   ├── test_message.py
│   │   ├── test_registry.py
│   │   ├── test_serializer.py
│   │   ├── test_specialized_agents.py
│   │   ├── test_system.py
│   │   ├── test_tools.py
│   │   └── test_version.py
│   ├── integration/              # Integration tests (5 tests)
│   │   └── test_message_flow.py
│   └── e2e/                      # E2E tests (3 tests)
│       └── test_complete_workflow.py
│
├── examples/                      # Ejemplos funcionales (7 ejemplos)
│   ├── agents_config.yaml        # Configuración de ejemplo
│   ├── basic_agent_example.py
│   ├── basic_message_example.py
│   ├── complete_app_example.py   # Aplicación completa
│   ├── dt_example.py
│   ├── memory_example.py
│   ├── specialized_agents_example.py
│   └── tools_example.py
│
├── docs/                          # Documentación
│   ├── INDEX.md                   # Índice de documentación
│   ├── REQUIREMENTS.md            # Requisitos
│   ├── INSTALLATION.md            # Instalación (movido desde raíz)
│   ├── PROJECT_STATUS.md          # Estado del proyecto (movido desde raíz)
│   ├── PROJECT_STRUCTURE.md       # Estructura del proyecto (movido desde raíz)
│   ├── RESUMEN_EJECUTIVO.md       # Resumen ejecutivo (movido desde raíz)
│   ├── README_DEVELOPMENT.md      # Guía de desarrollo (movido desde raíz)
│   ├── CHANGELOG.md               # Historial de cambios (movido desde raíz)
│   ├── API_KEYS_CONFIG.md        # ⚠️ Configuración API Keys
│   ├── USER_GUIDE.md             # Guía de usuario
│   ├── FAQ.md                    # Preguntas frecuentes
│   ├── ARCHITECTURE.md            # Arquitectura
│   ├── PROTOCOL.md                # Protocolo
│   ├── ROLES.md                   # Roles
│   ├── INTEGRATION.md             # Integración
│   ├── TROUBLESHOOTING.md         # Troubleshooting
│   ├── SPECIFICATIONS_V2.md       # Especificaciones actuales
│   ├── TESTING_STRATEGY.md       # Testing
│   ├── DEPLOYMENT.md              # Deployment
│   ├── SECURITY.md                # Seguridad
│   ├── MONITORING.md              # Observabilidad
│   ├── COST_MANAGEMENT.md         # Costos
│       ├── README.md
│       ├── INSPIRATION.md
│       ├── RESEARCH.md
│       ├── SPECIFICATIONS.md      # v1 deprecated
│       ├── PLAN_REVIEW.md
│       ├── CREWAI_LEARNINGS.md
│       ├── TASKMASTER_RULES_INTEGRATION.md
│       ├── DT_AUTONOMY.md
│       ├── IMPLEMENTATION_PLAN.md
│       ├── PROJECT_SUMMARY.md
│       ├── INDEX.md
│       └── REORGANIZATION_PLAN.md
│
├── .github/                        # GitHub Actions
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
│
├── README.md                       # Documentación principal
├── LICENSE                         # Licencia (si existe)
├── pyproject.toml                 # Configuración del proyecto
├── setup.py                       # Setup script
├── requirements.txt               # Dependencias core
├── requirements-dev.txt           # Dependencias de desarrollo
├── Makefile                       # Comandos útiles
├── .gitignore                     # Archivos a ignorar
└── .pre-commit-config.yaml        # Pre-commit hooks
```

## 📊 Estadísticas

- **Archivos Python**: 25+
- **Tests**: 109 pasando
- **Ejemplos**: 7 funcionales
- **Documentación**: 15+ documentos esenciales + 11 de referencia

## 🎯 Principios de Organización

### 1. Separación de Concerns
- **src/**: Código fuente
- **tests/**: Tests organizados por tipo
- **examples/**: Ejemplos funcionales
- **docs/**: Documentación esencial

### 2. Modularidad
- Cada módulo tiene su propio `__init__.py`
- Exports claros y organizados
- Dependencias mínimas entre módulos

### 3. Escalabilidad
- Fácil agregar nuevos agentes en `agents/`
- Fácil agregar nuevas herramientas en `tools/`
- Fácil agregar nuevos backends en `memory/`

### 4. Claridad
- Nombres descriptivos
- Estructura lógica
- Documentación accesible

## 🔍 Navegación Rápida

### Para Usuarios
- **Empezar**: `docs/INSTALLATION.md`
- **Configurar**: `docs/API_KEYS_CONFIG.md`
- **Usar**: `docs/USER_GUIDE.md`
- **Ejemplos**: `examples/`

### Para Desarrolladores
- **Arquitectura**: `docs/ARCHITECTURE.md`
- **Protocolo**: `docs/PROTOCOL.md`
- **Integración**: `docs/INTEGRATION.md`
- **Código**: `src/agents_army/`

### Para Contribuidores
- **Tests**: `tests/`
- **Ejemplos**: `examples/`
- **Documentación**: `docs/`
- **CI/CD**: `.github/workflows/`

---

**Última actualización**: Enero 2025
