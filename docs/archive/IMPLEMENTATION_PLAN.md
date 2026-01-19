# Plan de Implementación: Agents_Army

## Visión General

Este documento define el plan de implementación para construir el framework **Agents_Army**, integrando las mejores prácticas identificadas en el [OpenAI Cookbook](https://cookbook.openai.com/topic/agents), [Anthropic Claude Agent SDK](https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk) y otros frameworks de referencia.

**⚠️ IMPORTANTE**: Antes de implementar, revisa **[SPECIFICATIONS.md](SPECIFICATIONS.md)** que define exactamente qué vamos a construir: cuántos agentes, cuáles, qué funcionalidad específica, y todas las definiciones técnicas.

## Principios de Implementación

1. **Iterativo e Incremental**: Construir en fases, validando cada paso
2. **Basado en Estándares**: Usar protocolos existentes cuando sea posible (MCP, etc.)
3. **Modular y Extensible**: Componentes independientes y reutilizables
4. **Bien Documentado**: Código autodocumentado y ejemplos claros
5. **Testeable**: Tests desde el inicio, cobertura alta

## Fases de Implementación

### Fase 0: Preparación y Setup (Semana 1)

**Objetivo**: Preparar el entorno de desarrollo y estructura base del proyecto.

**Tareas**:
- [ ] Configurar estructura de proyecto (Python/TypeScript)
- [ ] Setup de herramientas de desarrollo (linting, formatting, testing)
- [ ] Configurar CI/CD básico
- [ ] Crear estructura de directorios según [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Setup de documentación (Sphinx/MkDocs)
- [ ] Definir versionado (Semantic Versioning)

**Entregables**:
- Estructura de proyecto lista
- Herramientas de desarrollo configuradas
- CI/CD funcionando

**Criterios de Éxito**:
- Proyecto se puede clonar y configurar en < 5 minutos
- Tests básicos pasan
- Documentación se genera correctamente

---

### Fase 1: Core - Protocolo y Mensajería (Semanas 2-3)

**Objetivo**: Implementar el protocolo de comunicación base.

**Tareas**:
- [ ] Implementar `AgentMessage` class con validación de esquemas
- [ ] Implementar `MessageSerializer` (JSON, con soporte para otros formatos)
- [ ] Implementar `MessageRouter` básico
- [ ] Implementar tipos de mensajes según [PROTOCOL.md](PROTOCOL.md)
- [ ] Tests unitarios para protocolo
- [ ] Tests de integración para flujos de mensajes

**Entregables**:
- Sistema de mensajería funcional
- Validación de esquemas
- Routing básico

**Criterios de Éxito**:
- Mensajes se serializan/deserializan correctamente
- Validación rechaza mensajes inválidos
- Router enruta mensajes correctamente

**Referencias**:
- [PROTOCOL.md](PROTOCOL.md) - Especificación del protocolo
- [INSPIRATION.md](INSPIRATION.md) - Patrones del OpenAI Cookbook

---

### Fase 2: Core - Sistema Base de Agentes (Semanas 4-5)

**Objetivo**: Implementar la clase base `Agent` y sistema de registro.

**Tareas**:
- [ ] Implementar clase base `Agent` con:
  - Instrucciones configurables
  - Modelo LLM configurable
  - Sistema de herramientas
  - Manejo de contexto
- [ ] Implementar `AgentRegistry` para registro de agentes
- [ ] Implementar `AgentSystem` como punto de entrada
- [ ] Sistema de configuración (YAML/JSON)
- [ ] Tests para agentes base

**Entregables**:
- Clase `Agent` funcional
- Sistema de registro de agentes
- Configuración declarativa

**Criterios de Éxito**:
- Se pueden crear agentes con configuración
- Agentes se registran correctamente
- Sistema puede inicializar agentes desde configuración

**Referencias**:
- [ROLES.md](ROLES.md) - Definición de roles
- [ARCHITECTURE.md](ARCHITECTURE.md) - Diseño de componentes

---

### Fase 3: El DT (Semanas 6-8)

**Objetivo**: Implementar El DT con funcionalidad de taskmaster + autonomía.

**Tareas**:
- [ ] Implementar `DT` extendiendo `Agent`
- [ ] Implementar funcionalidad core de taskmaster:
  - [ ] `initialize_project()`
  - [ ] `parse_prd()`
  - [ ] `get_tasks()`, `get_next_task()`
  - [ ] `expand_task()`
  - [ ] `research()`
- [ ] Implementar `TaskDecomposer` para dividir tareas complejas
- [ ] Implementar `TaskScheduler` para asignar tareas
- [ ] Implementar `ResultSynthesizer` para combinar resultados
- [ ] **Implementar `DTAutonomyEngine`** (NUEVO):
  - [ ] `decide_and_act()`
  - [ ] `calculate_confidence()`
  - [ ] `assess_risk()`
  - [ ] `make_decision()`
  - [ ] `execute_autonomously()`
- [ ] **Implementar `LearningEngine`** (NUEVO):
  - [ ] Aprendizaje de decisiones
  - [ ] Ajuste de umbrales adaptativos
- [ ] Sistema de handoffs entre agentes
- [ ] Sistema de reglas (carga y aplicación)
- [ ] Tests para El DT

**Entregables**:
- El DT funcional con taskmaster
- Sistema de autonomía completo
- Sistema de aprendizaje básico
- Descomposición de tareas
- Handoffs entre agentes

**Criterios de Éxito**:
- El DT puede parsear PRD y generar tareas
- Puede decidir y actuar autónomamente según reglas
- Puede descomponer tareas complejas
- Puede asignar tareas a agentes especializados
- Puede sintetizar resultados de múltiples agentes
- Sistema de aprendizaje ajusta umbrales

**Referencias**:
- [SPECIFICATIONS_V2.md](SPECIFICATIONS_V2.md#1-el-dt-director-técnico) - Especificación de El DT
- [TASKMASTER_RULES_INTEGRATION.md](TASKMASTER_RULES_INTEGRATION.md) - Sistema de reglas
- [DT_AUTONOMY.md](DT_AUTONOMY.md) - Autonomía detallada

---

### Fase 4: Specialist Agents (Semanas 8-9)

**Objetivo**: Implementar agentes especialistas según [SPECIFICATIONS.md](SPECIFICATIONS.md).

**Agentes a Implementar**:
- ✅ Researcher (investigación)
- ✅ Writer (escritura)
- ❌ Analyst (para v2.0)

**Tareas**:
- [ ] Implementar `Specialist` base class
- [ ] Implementar `Researcher` con:
  - [ ] Método `execute()` completo
  - [ ] Método `search_web()` con validación
  - [ ] Método `analyze_document()` básico
  - [ ] Integración con herramientas: web_search, document_parser, text_extractor
- [ ] Implementar `Writer` con:
  - [ ] Método `execute()` completo
  - [ ] Método `generate_content()`
  - [ ] Método `edit_content()`
  - [ ] Método `format_content()` (markdown, plain)
  - [ ] Integración con herramientas: text_generator, text_formatter, text_analyzer
- [ ] Tests unitarios para cada método
- [ ] Tests de integración end-to-end

**Entregables**:
- Researcher funcional con todas las capacidades especificadas
- Writer funcional con todas las capacidades especificadas
- Herramientas integradas y funcionando

**Criterios de Éxito**:
- Researcher puede buscar web y analizar documentos según especificación
- Writer puede generar y formatear contenido según especificación
- Todas las herramientas funcionan correctamente
- Tests pasan con cobertura > 80%

**Referencias**:
- [SPECIFICATIONS.md](SPECIFICATIONS.md#2-researcher-investigador) - Especificación detallada de Researcher
- [SPECIFICATIONS.md](SPECIFICATIONS.md#3-writer-escritor) - Especificación detallada de Writer
- [ROLES.md](ROLES.md#2-specialist-especialista) - Rol de especialista

---

### Fase 5: Validator (Semana 10)

**Objetivo**: Implementar sistema de validación según [SPECIFICATIONS.md](SPECIFICATIONS.md).

**Tareas**:
- [ ] Implementar `Validator` agent con:
  - [ ] Método `validate()` completo
  - [ ] Método `check_format()` con validación de esquemas
  - [ ] Método `check_quality()` con score 0-1
  - [ ] Método `check_policies()` básico (contenido ofensivo)
  - [ ] Generación de feedback constructivo
- [ ] Implementar 4 reglas de validación:
  - [ ] format_check
  - [ ] quality_check (score mínimo 0.7)
  - [ ] policy_check
  - [ ] completeness_check
- [ ] Tests para cada regla de validación
- [ ] Tests de integración

**Entregables**:
- Validator funcional con todas las reglas especificadas
- Sistema de guardrails básico funcionando

**Criterios de Éxito**:
- Validator valida formato, calidad, políticas y completitud
- Score de calidad funciona correctamente (0-1)
- Políticas básicas se detectan
- Feedback es útil y accionable

**Referencias**:
- [SPECIFICATIONS.md](SPECIFICATIONS.md#4-validator-validador) - Especificación detallada de Validator
- [ROLES.md](ROLES.md#3-validator-validador--observador) - Rol de validador

---

### Fase 6: Memory System (Semanas 11-12)

**Objetivo**: Implementar sistema de memoria según [SPECIFICATIONS.md](SPECIFICATIONS.md).

**Backends a Implementar**:
- ✅ InMemoryBackend (desarrollo/testing)
- ✅ SQLiteBackend (producción simple)
- ❌ VectorDBBackend (para v2.0)
- ❌ RedisBackend (para v2.0)

**Tareas**:
- [ ] Implementar interfaz `MemoryBackend`
- [ ] Implementar `InMemoryBackend`:
  - [ ] Almacenamiento en memoria
  - [ ] Búsqueda de texto simple
  - [ ] Políticas de retención básicas
- [ ] Implementar `SQLiteBackend`:
  - [ ] Schema de base de datos
  - [ ] Operaciones CRUD
  - [ ] Búsqueda de texto simple (LIKE queries)
  - [ ] Políticas de retención con TTL
- [ ] Implementar `MemorySystem` con:
  - [ ] Método `store()` completo
  - [ ] Método `retrieve()` por clave
  - [ ] Método `search()` básico (texto simple, no semántico)
  - [ ] Método `delete()` con validación de TTL
- [ ] Implementar políticas de retención:
  - [ ] session: 1h
  - [ ] task: 7d
  - [ ] user: 30d
  - [ ] system: 90d
- [ ] Tests para cada backend
- [ ] Tests de políticas de retención

**Entregables**:
- MemorySystem funcional con 2 backends
- Búsqueda básica funcionando
- Políticas de retención implementadas

**Criterios de Éxito**:
- Memoria puede almacenar y recuperar información
- Backends intercambiables funcionan correctamente
- Búsqueda de texto simple funciona
- Políticas de retención se aplican automáticamente
- Tests pasan con cobertura > 80%

**Referencias**:
- [SPECIFICATIONS.md](SPECIFICATIONS.md#5-memorysystem-sistema-de-memoria) - Especificación detallada de MemorySystem
- [ROLES.md](ROLES.md#4-memory-sistema-de-memoria) - Rol de memoria

---

### Fase 7: Tools Registry (Semana 13)

**Objetivo**: Implementar sistema de herramientas según [SPECIFICATIONS.md](SPECIFICATIONS.md).

**Herramientas a Implementar** (6 herramientas):
1. ✅ web_search
2. ✅ document_parser
3. ✅ text_extractor
4. ✅ text_generator
5. ✅ text_formatter
6. ✅ text_analyzer

**Tareas**:
- [ ] Implementar clase base `Tool` con:
  - [ ] Validación de parámetros con Pydantic
  - [ ] Manejo de errores
  - [ ] Logging de ejecución
- [ ] Implementar `ToolRegistry` con:
  - [ ] Método `register()`
  - [ ] Método `get_tool()`
  - [ ] Método `list_tools()`
  - [ ] Método `execute_tool()` con validación
- [ ] Implementar las 6 herramientas especificadas:
  - [ ] web_search: Integración con SerpAPI o similar
  - [ ] document_parser: Parser de texto plano y markdown
  - [ ] text_extractor: Extracción básica de texto
  - [ ] text_generator: Wrapper de LLM para generación
  - [ ] text_formatter: Formateo markdown y plain
  - [ ] text_analyzer: Análisis básico (word count, sentences, etc.)
- [ ] Tests unitarios para cada herramienta
- [ ] Tests de integración con agentes

**Entregables**:
- ToolRegistry funcional
- 6 herramientas implementadas y funcionando
- Validación de parámetros funcionando

**Criterios de Éxito**:
- Todas las herramientas se registran correctamente
- Validación de parámetros funciona para todas
- Herramientas se ejecutan sin errores
- Agentes pueden usar herramientas correctamente
- Tests pasan con cobertura > 80%

**Referencias**:
- [SPECIFICATIONS.md](SPECIFICATIONS.md#6-tool-registry-infraestructura) - Especificación detallada de herramientas
- [ROLES.md](ROLES.md#5-tool-herramienta-externa) - Rol de herramienta

---

### Fase 8: Observabilidad y Logging (Semana 14)

**Objetivo**: Implementar sistema de logging, métricas y tracing.

**Tareas**:
- [ ] Sistema de logging estructurado
- [ ] Métricas (tiempo, tokens, éxito/fallo)
- [ ] Tracing de decisiones y flujos
- [ ] Dashboard básico (opcional)
- [ ] Tests para observabilidad

**Entregables**:
- Sistema de logging completo
- Métricas básicas
- Tracing funcional

**Criterios de Éxito**:
- Todos los eventos se registran
- Métricas se recopilan correctamente
- Traces permiten debugging

**Referencias**:
- [ARCHITECTURE.md](ARCHITECTURE.md#observabilidad) - Observabilidad
- [INSPIRATION.md](INSPIRATION.md#1-agents-sdk-de-openai) - Tracing del Agents SDK

---

### Fase 9: Despliegue y DevOps (Semanas 15-16)

**Objetivo**: Implementar estrategia de despliegue completa.

**Tareas**:
- [ ] Crear Dockerfile optimizado
- [ ] Crear docker-compose para desarrollo
- [ ] Configurar CI/CD pipeline (GitHub Actions)
- [ ] Implementar health checks (`/health`, `/ready`, `/live`)
- [ ] Configurar auto-scaling básico
- [ ] Implementar sistema de versionado
- [ ] Configurar secret management
- [ ] Documentación de despliegue
- [ ] Tests de despliegue

**Entregables**:
- Dockerfile funcional
- CI/CD pipeline completo
- Health checks implementados
- Documentación de despliegue

**Criterios de Éxito**:
- Imagen Docker se construye correctamente
- CI/CD pipeline pasa todos los checks
- Health checks funcionan
- Despliegue a staging exitoso
- Documentación completa

**Referencias**:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Estrategia de despliegue

---

### Fase 10: Integración y Ejemplos (Semanas 17-18)

**Objetivo**: Crear ejemplos prácticos y adaptadores para frameworks comunes.

**Tareas**:
- [ ] Ejemplo básico de uso
- [ ] Ejemplo multi-agente complejo
- [ ] Ejemplo de autonomía del DT
- [ ] Adaptador para FastAPI
- [ ] Adaptador para Flask (opcional)
- [ ] Adaptador para Django (opcional)
- [ ] Tutorial paso a paso
- [ ] Tests de integración end-to-end

**Entregables**:
- Múltiples ejemplos funcionales
- Adaptadores para frameworks comunes
- Tutorial completo

**Criterios de Éxito**:
- Ejemplos funcionan correctamente
- Adaptadores facilitan integración
- Tutorial es claro y completo

**Referencias**:
- [INTEGRATION.md](INTEGRATION.md) - Guía de integración
- [INSPIRATION.md](INSPIRATION.md) - Ejemplos del Cookbook

---

### Fase 11: Features Avanzadas (Semanas 19-22)

**Objetivo**: Implementar features avanzadas identificadas en el análisis.

**Tareas**:
- [ ] Sistema de evaluación (Evals)
- [ ] Context summarization
- [ ] Self-evolution mechanisms (opcional)
- [ ] Soporte MCP completo
- [ ] Ejecución paralela de agentes
- [ ] Distributed execution (opcional)

**Entregables**:
- Features avanzadas funcionales
- Mejora continua integrada

**Criterios de Éxito**:
- Features avanzadas funcionan
- Sistema puede evolucionar
- Rendimiento mejorado

**Referencias**:
- [INSPIRATION.md](INSPIRATION.md#3-self-evolving-agents) - Self-evolving agents
- [INSPIRATION.md](INSPIRATION.md#5-context-engineering) - Context summarization

---

## Stack Tecnológico Propuesto

### Lenguaje Principal
- **Python 3.10+**: Amplia adopción, ecosistema rico, fácil integración con LLMs

### Dependencias Core
- **pydantic**: Validación de datos y esquemas
- **pyyaml**: Configuración YAML
- **asyncio**: Programación asíncrona
- **typing**: Type hints

### LLM Integration
- **openai**: SDK de OpenAI
- **anthropic**: SDK de Anthropic (opcional)
- **langchain**: Para abstracciones comunes (opcional)

### Testing
- **pytest**: Framework de testing
- **pytest-asyncio**: Tests asíncronos
- **pytest-cov**: Cobertura de código

### Documentación
- **mkdocs** o **sphinx**: Generación de documentación
- **mkdocs-material**: Tema para MkDocs

### CI/CD
- **GitHub Actions**: CI/CD
- **pre-commit**: Hooks de pre-commit
- **black**: Formateo de código
- **ruff**: Linting rápido

### Opcionales
- **redis**: Para memoria distribuida
- **postgresql**: Backend de base de datos
- **vector databases**: Para búsqueda semántica (opcional)

## Estructura de Código Propuesta

```
agents_army/
├── src/
│   ├── agents_army/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── agent.py          # Clase base Agent
│   │   │   ├── message.py        # AgentMessage
│   │   │   ├── protocol.py       # Protocolo de comunicación
│   │   │   └── system.py         # AgentSystem
│   │   ├── agents/
│   │   │   ├── coordinator.py    # Coordinator
│   │   │   ├── specialist.py     # Specialist base
│   │   │   ├── researcher.py     # Researcher
│   │   │   ├── writer.py          # Writer
│   │   │   ├── analyst.py         # Analyst
│   │   │   └── validator.py       # Validator
│   │   ├── memory/
│   │   │   ├── backend.py         # MemoryBackend interface
│   │   │   ├── in_memory.py       # InMemoryBackend
│   │   │   ├── database.py        # DatabaseBackend
│   │   │   └── system.py          # MemorySystem
│   │   ├── tools/
│   │   │   ├── base.py            # Tool base class
│   │   │   ├── registry.py        # ToolRegistry
│   │   │   └── builtin.py         # Herramientas built-in
│   │   ├── protocol/
│   │   │   ├── router.py           # MessageRouter
│   │   │   ├── serializer.py       # MessageSerializer
│   │   │   └── validator.py        # MessageValidator
│   │   ├── observability/
│   │   │   ├── logging.py          # Logging system
│   │   │   ├── metrics.py          # Métricas
│   │   │   └── tracing.py          # Tracing
│   │   └── config/
│   │       ├── loader.py           # Config loader
│   │       └── schema.py           # Config schemas
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── examples/
│   ├── basic/
│   ├── multi_agent/
│   └── integration/
├── docs/
│   └── (documentación existente)
├── pyproject.toml
├── README.md
└── .gitignore
```

## Métricas de Éxito

### Técnicas
- **Cobertura de tests**: > 80%
- **Tiempo de build**: < 5 minutos
- **Documentación**: 100% de APIs documentadas
- **Type hints**: 100% de código con type hints

### Funcionales
- **Protocolo**: Mensajes se comunican correctamente
- **Agentes**: Todos los roles implementados funcionan
- **Integración**: Ejemplos funcionan end-to-end
- **Performance**: Latencia aceptable (< 1s para mensajes simples)

## Riesgos y Mitigación

### Riesgo 1: Complejidad del Protocolo
- **Mitigación**: Implementar en fases, validar cada paso

### Riesgo 2: Integración con LLMs
- **Mitigación**: Abstraer interfaz de LLM, soportar múltiples proveedores

### Riesgo 3: Performance
- **Mitigación**: Profiling temprano, optimización iterativa

### Riesgo 4: Cambios en APIs externas
- **Mitigación**: Versionado de dependencias, tests de integración

## Documentos de Referencia Adicionales

- **[PLAN_REVIEW.md](PLAN_REVIEW.md)**: Revisión completa del plan, gaps y mejoras
- **[DT_AUTONOMY.md](DT_AUTONOMY.md)**: Autonomía detallada de El DT
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Estrategia de despliegue completa

## Próximos Pasos Inmediatos

1. **Revisar [PLAN_REVIEW.md](PLAN_REVIEW.md)**: Identificar gaps críticos
2. **Crear documentos faltantes**: DT_AUTONOMY.md, DEPLOYMENT.md, etc.
3. **Decidir stack tecnológico**: Confirmar Python vs TypeScript
4. **Setup inicial**: Crear estructura de proyecto
5. **Fase 0**: Completar preparación y setup
6. **Fase 1**: Empezar con protocolo de mensajería

## Referencias

- [ARCHITECTURE.md](ARCHITECTURE.md) - Diseño arquitectónico
- [PROTOCOL.md](PROTOCOL.md) - Especificación del protocolo
- [ROLES.md](ROLES.md) - Definición de roles
- [INSPIRATION.md](INSPIRATION.md) - Fuentes de inspiración
- [INTEGRATION.md](INTEGRATION.md) - Guía de integración

---

**Última actualización**: Enero 2025  
**Estado**: Planificación - Listo para implementación
