# Agents_Army 🎯

> Un framework modular y escalable para construir sistemas multi-agente de IA

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-109%20passing-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 Estado del Proyecto

**Versión**: 0.1.0 (MVP)  
**Estado**: ✅ **Ready to Use** | ✅ **Ready to Share**

El MVP está **completo y funcional**. El framework está listo para uso en proyectos básicos y puede extenderse según necesidad.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Quick Start](#-quick-start)
- [Arquitectura](#-arquitectura)
- [Documentación](#-documentación)
- [Skills](#-skills)
- [Ejemplos](#-ejemplos)
- [Estado de Implementación](#-estado-de-implementación)
- [Contribuir](#-contribuir)

## ✨ Características

### 🎯 Core Features

- **Protocolo de Comunicación Estándar**: Mensajes estructurados con validación Pydantic
- **El DT (Director Técnico)**: Coordinador (Orchestrator) inteligente basado en LLM
- **18 Agentes Especializados**: Desde investigación hasta marketing, desarrollo, diseño y operaciones
- **Skills System**: Workflows especializados reutilizables (ej: github-save)
- **Sistema de Memoria**: Persistencia con múltiples backends (InMemory, SQLite)
- **Sistema de Herramientas**: 6 herramientas básicas + extensible
- **Configuración Declarativa**: YAML/JSON para configuración de agentes

### 🏗️ Arquitectura

- **Modular**: Componentes independientes y reutilizables
- **Escalable**: Fácil agregar nuevos agentes y herramientas
- **Type-Safe**: 100% type hints con Pydantic
- **Testeable**: 109 tests pasando (>80% cobertura)

## 📦 Instalación

### Requisitos

- Python 3.10+
- pip

### Instalación desde Código

```bash
# Clonar repositorio
git clone <repo-url>
cd Agents_Army

# Instalar en modo desarrollo
pip install -e .

# O instalar dependencias directamente
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desarrollo
```

### ⚠️ Configuración de API Keys

**Importante**: Para usar LLMs reales, necesitas configurar API keys.

Ver **[docs/API_KEYS_CONFIG.md](docs/API_KEYS_CONFIG.md)** para instrucciones detalladas.

```bash
# Configurar variable de entorno (recomendado)
export OPENAI_API_KEY="tu-api-key"  # Linux/macOS
# O
$env:OPENAI_API_KEY="tu-api-key"    # Windows PowerShell
```

### Verificar Instalación

```bash
python -c "from agents_army import AgentSystem, DT; print('✅ Agents_Army instalado correctamente')"
```

**Ver más detalles en**: [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | [docs/QUICK_START.md](docs/QUICK_START.md)

## 🚀 Quick Start

**¿Nuevo en Agents_Army?** Empieza con **[docs/QUICK_START.md](docs/QUICK_START.md)** (5 minutos)

### ⚡ Forma Más Rápida: Usar `/dt-start`

**Recomendamos empezar usando el comando `/dt-start` directamente en tu IDE.**

El DT te guiará a través de una conversación adaptativa para inicializar tu proyecto de forma estructurada, sin necesidad de escribir código.

#### 📝 Configurar el Workflow en tu IDE

**En Cursor:**
1. Abre el chat en Cursor
2. Escribe solo `/` (barra diagonal)
3. Se desplegará un menú con opciones
4. Selecciona o crea el workflow `dt-start`
5. ¡Listo! Ahora puedes usar `/dt-start` cuando quieras inicializar un proyecto

**En Antigravity:**
1. En el chat, arriba a la derecha, haz clic en los **tres puntitos** (⋯)
2. Se desplegará un menú → Selecciona **"Customizations"**
3. Ve a la pestaña **"Workflows"**
4. Crea un workflow **global** llamado `dt-start`
5. Configúralo para usar el archivo `.cursor/commands/dt-start.md`
6. ¡Listo! Ahora puedes usar `/dt-start` desde cualquier proyecto

#### 🎯 Usar `/dt-start`

Una vez configurado el workflow:

1. **Escribe `/dt-start`** en el chat de tu IDE
2. **El DT comenzará una conversación guiada** contigo:
   - Te preguntará qué tipo de proyecto quieres crear
   - Adaptará las preguntas según el tipo (desarrollo, marketing, contenido, diseño, etc.)
   - Creará un plan estructurado antes de ejecutar
   - Esperará tu aprobación explícita antes de crear directorios o archivos
3. **El DT inicializará tu proyecto** con la estructura apropiada

**Tipos de proyectos soportados:**
- Desarrollo de Software (apps web, móviles, APIs)
- Marketing (campañas, estrategias)
- Contenido (blog, copywriting, redes sociales)
- Diseño (UI/UX, branding)
- Investigación (market research, user research)
- Estrategia de Negocio (product strategy, go-to-market)
- Técnico/DevOps (infraestructura, CI/CD)
- Y más...

**Ver el workflow completo**: [`skills/dt-start.md`](skills/dt-start.md) | [`.cursor/commands/dt-start.md`](.cursor/commands/dt-start.md)

---

### Dos Caminos Alternativos para Empezar

#### 1️⃣ Ya Tienes un Proyecto
Clona el repo e integra El DT en tu proyecto existente.

```bash
git clone https://github.com/Mazalucas/El-DT-Agent-Army.git
cd El-DT-Agent-Army
pip install -e .
```

Luego usa El DT en tu código (ver [docs/QUICK_START.md](docs/QUICK_START.md) para ejemplo completo).

#### 2️⃣ Conversar con El DT para Planear (Código Python)
Si prefieres usar código Python directamente, El DT te ayuda a planearlo desde cero.

```bash
git clone https://github.com/Mazalucas/El-DT-Agent-Army.git
cd El-DT-Agent-Army
pip install -e .
python examples/dt_example.py
```

**Ver detalles completos en**: [docs/QUICK_START.md](docs/QUICK_START.md)

### Ejemplo Básico (Referencia)

```python
import asyncio
from agents_army import DT
from agents_army.core.agent import LLMProvider

# 1. Crear tu LLM Provider (ejemplo con mock)
class MyLLMProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs):
        # Integrar con OpenAI, Anthropic, etc.
        return "Mock response"

# 2. Crear El DT
dt = DT(
    project_path=".my_project",
    llm_provider=MyLLMProvider()
)

# 3. Inicializar proyecto
async def main():
    project = await dt.initialize_project(
        project_name="Mi Proyecto",
        description="Descripción del proyecto"
    )
    
    # 4. Crear PRD y parsear
    # ... (ver ejemplos/dt_example.py)

asyncio.run(main())
```

### Ejemplo: Sistema Multi-Agente Completo

```python
from agents_army import (
    DT, Researcher, BackendArchitect, FrontendDeveloper,
    ProductStrategist, UIDesigner, ContentCreator,
    AgentSystem, MemoryAgent, InMemoryBackend
)

# Crear sistema
system = AgentSystem()

# Crear agentes
dt = DT(llm_provider=your_llm)
researcher = Researcher(llm_provider=your_llm)
architect = BackendArchitect(llm_provider=your_llm)
frontend_dev = FrontendDeveloper(llm_provider=your_llm)
product_strategist = ProductStrategist(llm_provider=your_llm)
ui_designer = UIDesigner(llm_provider=your_llm)
content_creator = ContentCreator(llm_provider=your_llm)
memory = MemoryAgent(backend=InMemoryBackend())

# Registrar agentes
system.register_agent(dt)
system.register_agent(researcher)
system.register_agent(architect)
system.register_agent(frontend_dev)
system.register_agent(product_strategist)
system.register_agent(ui_designer)
system.register_agent(content_creator)
system.register_agent(memory)

# Usar...
# (ver examples/complete_app_example.py)
```

**Nota**: Hay 18 agentes especializados disponibles. Ver la lista completa en [Agentes Implementados](#agentes-implementados).

## 🏛️ Arquitectura

```
┌─────────────────────────────────────────┐
│         AgentSystem                     │
│      (Punto de Entrada)                 │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ El DT  │ │Message │ │Agent   │
│(Coord.)│ │Router  │ │Registry│
└────────┘ └────────┘ └────────┘
    │
    ▼
┌──────────────────────────────┐
│  Agentes Especializados      │
│  (18 agentes disponibles)    │
│  Research │ Development      │
│  Design │ Marketing          │
│  Product │ Operations        │
└──────────────────────────────┘
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Memory  │ │Tools  │ │Protocol│
│System  │ │Registry│ │Layer   │
└────────┘ └────────┘ └────────┘
```

## 📚 Documentación

### Para Empezar
- **[QUICK_START.md](docs/QUICK_START.md)** - ⚡ Inicio rápido (5 minutos)
- **[REQUIREMENTS.md](docs/REQUIREMENTS.md)** - Requisitos del sistema
- **[API_KEYS_CONFIG.md](docs/API_KEYS_CONFIG.md)** - ⚠️ **Configuración de API Keys** (LLMs y MCP)
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Guía de usuario completa
- **[FAQ.md](docs/FAQ.md)** - Preguntas frecuentes

### Documentación Técnica
- **[INDEX.md](docs/INDEX.md)** - Índice completo de documentación
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura del sistema
- **[PROTOCOL.md](docs/PROTOCOL.md)** - Protocolo de comunicación
- **[SPECIFICATIONS_V2.md](docs/SPECIFICATIONS_V2.md)** - Especificaciones técnicas
- **[INTEGRATION.md](docs/INTEGRATION.md)** - Guía de integración
- **[ROLES.md](docs/ROLES.md)** - Roles y responsabilidades

### Operaciones
- **[TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md)** - Estrategia de testing
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deployment
- **[SECURITY.md](docs/SECURITY.md)** - Seguridad
- **[MONITORING.md](docs/MONITORING.md)** - Observabilidad
- **[COST_MANAGEMENT.md](docs/COST_MANAGEMENT.md)** - Gestión de costos
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solución de problemas


## 🎯 Skills

Las Skills son workflows y comandos especializados que pueden ser ejecutados por los agentes para realizar tareas específicas. Estas skills están documentadas en formato markdown y pueden ser utilizadas por cualquier agente del sistema.

### Skills Disponibles

1. **`dt-start`** ⭐ **NUEVO** - Workflow conversacional para inicializar proyectos con El DT
   - Guía adaptativa según tipo de proyecto (desarrollo, marketing, contenido, diseño, etc.)
   - Preguntas progresivas y adaptativas
   - Crea plan estructurado antes de ejecutar
   - Espera aprobación explícita antes de crear directorios
   - Ubicación: `skills/dt-start.md` | `.cursor/commands/dt-start.md`
   - **Recomendado para empezar**: Ver sección [Quick Start](#-quick-start)

2. **`github-save`** - Workflow completo de Git para guardar cambios, crear tags de versión y hacer push al repositorio remoto
   - Verifica repositorio Git inicializado
   - Valida autenticación y conexión remota
   - Crea commits con mensajes descriptivos
   - Genera tags de versión semántica
   - Hace push de commits y tags
   - Ubicación: `skills/github-save.md`

### Uso de Skills

Las skills pueden ser referenciadas por los agentes para ejecutar workflows complejos. Cada skill incluye:
- Objetivo claro
- Pre-requisitos y validaciones
- Pasos detallados del workflow
- Manejo de errores y advertencias
- Mejores prácticas

**Ver más**: `skills/` directory

## 💡 Ejemplos

El proyecto incluye 7 ejemplos funcionales:

1. **`basic_message_example.py`** - Mensajería básica entre agentes
2. **`basic_agent_example.py`** - Creación y uso de agentes básicos
3. **`dt_example.py`** - El DT y gestión de proyectos
4. **`specialized_agents_example.py`** - Agentes especializados
5. **`memory_example.py`** - Sistema de memoria
6. **`tools_example.py`** - Sistema de herramientas
7. **`complete_app_example.py`** - Aplicación completa

Ejecutar ejemplos:

```bash
python examples/complete_app_example.py
```

## ✅ Estado de Implementación

### Fases Completadas ✅

- [x] **Fase 0: Preparación y Setup** ✅
- [x] **Fase 1: Protocolo y Mensajería** ✅ (22 tests)
- [x] **Fase 2: Sistema Base de Agentes** ✅ (30 tests)
- [x] **Fase 3: El DT (Director Técnico)** ✅ (7 tests)
- [x] **Fase 4: Agentes Especializados** ✅ (14 tests)
- [x] **Fase 5: Sistema de Memoria** ✅ (17 tests)
- [x] **Fase 6: Sistema de Herramientas** ✅ (16 tests)
- [x] **Fase 7: Integración y Testing E2E** ✅ (3 tests)

**Total: 109 tests pasando** ✅

### Componentes Implementados

| Componente | Estado | Tests |
|------------|--------|-------|
| Protocolo de Mensajería | ✅ Completo | 22 |
| Sistema Base de Agentes | ✅ Completo | 30 |
| El DT | ✅ Completo | 7 |
| Agentes Especializados | ✅ 17/17 | 14 |
| Sistema de Memoria | ✅ Completo | 17 |
| Sistema de Herramientas | ✅ 6 herramientas | 16 |
| Tests E2E | ✅ Completo | 3 |

### Agentes Implementados

#### 🎯 Agentes Core
1. ✅ **El DT** - Coordinador principal y Director Técnico
2. ✅ **MemoryAgent** - Gestión de memoria y persistencia

#### 🔍 Agentes de Investigación y Análisis
3. ✅ **Researcher** - Investigación y análisis de información
4. ✅ **UXResearcher** - Investigación de experiencia de usuario
5. ✅ **FeedbackSynthesizer** - Síntesis y análisis de feedback

#### 🏗️ Agentes de Desarrollo
6. ✅ **BackendArchitect** - Arquitectura y diseño backend
7. ✅ **FrontendDeveloper** - Desarrollo frontend
8. ✅ **DevOpsAutomator** - Automatización DevOps y CI/CD
9. ✅ **QATester** - Testing y control de calidad

#### 📊 Agentes de Producto y Estrategia
10. ✅ **ProductStrategist** - Estrategia de producto
11. ✅ **OperationsMaintainer** - Mantenimiento y operaciones

#### 🎨 Agentes de Diseño y Contenido
12. ✅ **UIDesigner** - Diseño de interfaces de usuario
13. ✅ **ContentCreator** - Creación de contenido
14. ✅ **StorytellingSpecialist** - Especialista en narrativa

#### 📈 Agentes de Marketing y Crecimiento
15. ✅ **MarketingStrategist** - Estrategia de marketing
16. ✅ **GrowthHacker** - Crecimiento y adquisición
17. ✅ **BrandGuardian** - Gestión y protección de marca
18. ✅ **PitchSpecialist** - Creación de pitches y presentaciones

**Total: 18 agentes especializados** ✅

### Herramientas Implementadas

1. ✅ `web_search` - Búsqueda web (mock)
2. ✅ `document_parser` - Parser de documentos
3. ✅ `text_extractor` - Extracción de texto
4. ✅ `text_formatter` - Formateo de texto
5. ✅ `text_analyzer` - Análisis de texto
6. ✅ `text_generator` - Generación con LLM

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src/agents_army --cov-report=html

# Tests específicos
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

**Resultado**: 109 tests pasando ✅

## 🛠️ Desarrollo

### Setup de Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install

# Ejecutar linting
black src/ tests/
ruff check src/ tests/
mypy src/
```

### Estructura del Proyecto

```
Agents_Army/
├── src/agents_army/      # Código fuente
│   ├── protocol/        # Protocolo de mensajería
│   ├── core/            # Componentes core
│   ├── agents/          # Implementaciones de agentes
│   ├── memory/          # Sistema de memoria
│   └── tools/           # Sistema de herramientas
├── tests/               # Tests (109 tests)
├── examples/            # Ejemplos (7 ejemplos)
└── docs/                # Documentación (20+ docs)
```

## 📊 Métricas del Proyecto

- **Líneas de código**: ~5,000+
- **Archivos Python**: 25+
- **Tests**: 109 pasando
- **Cobertura**: >80%
- **Documentación**: 20+ documentos
- **Ejemplos**: 7 funcionales

## 🎯 Casos de Uso

### ✅ Lo que SÍ puedes hacer

- Crear sistemas multi-agente básicos
- Coordinar agentes especializados
- Gestionar proyectos con El DT
- Almacenar y recuperar contexto
- Usar herramientas básicas
- Integrar en nuevos proyectos

### ⚠️ Limitaciones del MVP

- LLM Integration: Necesitas integrar tu propio provider
- Web Search: Mock implementation (necesita API real)
- Agentes: 18 agentes especializados implementados ✅
- MCP Avanzado: Pendiente para v2.0

## 🔮 Roadmap

### v2.0 (Futuro)

- [ ] DTAutonomyEngine completo
- [ ] Búsqueda semántica en memoria
- [ ] Vector DB backends
- [ ] MCP avanzado
- [ ] Más agentes especializados según necesidades
- [ ] Dashboard visual
- [ ] Herramientas avanzadas

## 🤝 Contribuir

El proyecto está listo para contribuciones:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Guías de Contribución

- Seguir estructura de código existente
- Agregar tests para nuevas funcionalidades
- Actualizar documentación
- Mantener >80% cobertura

## 📄 Licencia

[Especificar licencia aquí - MIT recomendado]

## 🙏 Inspiración y Créditos

Este proyecto está inspirado en:

- [claude-task-master](https://github.com/eyaltoledano/claude-task-master) - Para El DT
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) - Para patrones de agentes
- [CrewAI](https://github.com/joaomdmoura/crewAI) - Para estructura de agentes
- [Anthropic Cookbook](https://github.com/anthropics/claude-cookbooks) - Para patrones de agentes

## 📞 Soporte

- **Documentación**: Ver `docs/`
- **Ejemplos**: Ver `examples/`
- **Issues**: [Crear issue en GitHub]
- **Troubleshooting**: Ver `docs/TROUBLESHOOTING.md`

---

**Versión**: 0.1.0 (MVP)  
**Estado**: ✅ Production Ready (con integración LLM)  
**Última actualización**: Enero 2025
