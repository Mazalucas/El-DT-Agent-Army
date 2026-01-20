# Changelog

All notable changes to Agents_Army will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added

#### Fase 0: Preparación y Setup
- ✅ Estructura completa del proyecto
- ✅ Configuración de `pyproject.toml` con metadata del proyecto
- ✅ `requirements.txt` y `requirements-dev.txt` con dependencias
- ✅ Configuración de herramientas de desarrollo:
  - Black para formateo
  - Ruff para linting
  - MyPy para type checking
  - Pre-commit hooks
- ✅ CI/CD básico con GitHub Actions
- ✅ Estructura de directorios:
  - `src/agents_army/` - Código fuente principal
  - `src/agents_army/core/` - Componentes core
  - `src/agents_army/agents/` - Implementaciones de agentes
  - `src/agents_army/memory/` - Sistema de memoria
  - `src/agents_army/tools/` - Herramientas
  - `src/agents_army/protocol/` - Protocolos de comunicación
  - `tests/` - Tests organizados por tipo
- ✅ Tests básicos configurados y funcionando
- ✅ Makefile con comandos útiles
- ✅ README_DEVELOPMENT.md con guía de desarrollo
- ✅ `.gitignore` configurado

### Documentation
- ✅ Documentación completa (15+ documentos)
- ✅ README actualizado con estructura del proyecto

## [Unreleased]

### Changed
- ✅ **Reorganización completa de documentación**
  - Documentación esencial separada de referencia
  - Documentación histórica eliminada (solo esencial)
  - Nuevo `docs/INDEX.md` simplificado
  - Nuevo `docs/QUICK_START.md` para inicio rápido
- ✅ **Mejoras en documentación**
  - Nuevo `docs/API_KEYS_CONFIG.md` con guía completa de API keys
  - Nuevo `docs/REQUIREMENTS.md` con requisitos detallados
  - Nuevo `docs/FAQ.md` con preguntas frecuentes
  - Actualizado `README.md` con referencias a configuración de API keys
- ✅ **Seguridad**
  - Actualizado `.gitignore` para proteger archivos `.env` y API keys
  - Documentación de mejores prácticas de seguridad

### Added

#### Fase 7: Integración y Testing E2E ✅
- ✅ Tests E2E completos (3 tests pasando)
  - Flujo completo de proyecto (inicialización → PRD → tareas → ejecución)
  - Coordinación multi-agente
  - Integración con sistema de memoria
- ✅ Aplicación de ejemplo completa (`complete_app_example.py`)
  - Demuestra uso completo del framework
  - Integración de todos los componentes
  - Flujo de trabajo real
- ✅ Tests de integración avanzados

#### Fase 6: Sistema de Herramientas ✅
- ✅ `Tool` - Clase base para todas las herramientas
- ✅ `ToolRegistry` - Registro y ejecución de herramientas
- ✅ Herramientas básicas implementadas:
  - `WebSearchTool` - Búsqueda web (mock para MVP)
  - `DocumentParserTool` - Parser de documentos (plain, markdown)
  - `TextExtractorTool` - Extracción de texto
  - `TextFormatterTool` - Formateo de texto (markdown, plain, html)
  - `TextAnalyzerTool` - Análisis de texto (estadísticas)
  - `TextGeneratorTool` - Generación de texto con LLM
- ✅ Validación de parámetros
- ✅ Manejo de errores (ToolNotFoundError, InvalidParametersError, ToolExecutionError)
- ✅ `create_default_tools()` - Factory para crear registry con herramientas por defecto
- ✅ Tests completos (16 tests pasando)
- ✅ Ejemplo funcional

#### Fase 5: Sistema de Memoria ✅
- ✅ `MemorySystem` - Sistema principal de memoria
- ✅ `MemoryBackend` - Interfaz abstracta para backends
- ✅ `InMemoryBackend` - Backend en memoria para desarrollo/testing
- ✅ `SQLiteBackend` - Backend SQLite para producción
- ✅ `MemoryAgent` - Agente wrapper para operaciones de memoria
- ✅ `RetentionPolicy` - Políticas de retención configurables
- ✅ Tipos de memoria: session, task, user, system, general
- ✅ Búsqueda de texto simple
- ✅ Limpieza automática de items expirados
- ✅ Tests completos (17 tests pasando)
- ✅ Ejemplo funcional

#### Fase 4: Agentes Especializados ✅
- ✅ `Researcher` - Agente de investigación genérico
- ✅ `BackendArchitect` - Especialista en arquitectura backend
- ✅ `MarketingStrategist` - Estratega de marketing
- ✅ `QATester` - Especialista en testing y QA
- ✅ Todos los agentes implementan métodos especializados
- ✅ Integración con sistema de mensajería
- ✅ Tests completos (14 tests pasando)
- ✅ Ejemplo funcional de coordinación multi-agente

#### Fase 3: El DT (Director Técnico) ✅
- ✅ Clase `DT` extendiendo `Agent`
- ✅ Funcionalidad core de taskmaster:
  - `initialize_project()` - Inicialización de proyectos
  - `parse_prd()` - Parseo de PRD y generación de tareas
  - `get_tasks()` - Listado de tareas con filtros
  - `get_next_task()` - Obtención de siguiente tarea
  - `assign_task()` - Asignación de tareas a agentes
  - `update_task_status()` - Actualización de estado
  - `expand_task()` - Expansión de tareas
  - `research()` - Investigación (con delegación a Researcher)
- ✅ Modelos de datos: `Task`, `Project`, `TaskResult`, `TaskAssignment`
- ✅ `TaskStorage` para persistencia de tareas
- ✅ Sistema de reglas básico (`RulesLoader`, `RulesChecker`)
- ✅ Tests completos (7 tests pasando)
- ✅ Ejemplo funcional

#### Fase 2: Sistema Base de Agentes ✅
- ✅ Clase base `Agent` con:
  - Instrucciones configurables (role, goal, backstory)
  - Modelo LLM configurable
  - Sistema de herramientas
  - Manejo de contexto
  - Message handling
  - Lifecycle management
- ✅ `AgentRegistry` para registro y búsqueda de agentes
- ✅ `AgentSystem` como punto de entrada principal
- ✅ `ConfigLoader` para carga de configuración desde YAML/JSON
- ✅ Sistema de configuración declarativa
- ✅ Tests completos (30 tests pasando)
- ✅ Ejemplo funcional de uso

#### Fase 1: Protocolo y Mensajería ✅
- ✅ `AgentMessage` class con validación completa de esquemas (Pydantic)
- ✅ `MessageSerializer` para serialización/deserialización JSON
- ✅ `MessageRouter` básico para enrutamiento de mensajes
- ✅ Tipos de mensajes según PROTOCOL.md (15 tipos)
- ✅ Roles de agentes (incluyendo todos los agentes especializados)
- ✅ Sistema de prioridades (low, normal, high, critical)
- ✅ Soporte para múltiples destinatarios
- ✅ Sistema de reply/reply_to para mensajes relacionados
- ✅ Validación de deadlines y timestamps
- ✅ Tests unitarios completos (16 tests)
- ✅ Tests de integración para flujos de mensajes (5 tests)

### Planned
- [ ] Fase 2: Sistema Base de Agentes
- [ ] Fase 3: El DT (Director Técnico)
- [ ] Fase 4: Agentes Especialistas
- [ ] Fase 5: Sistema de Memoria
- [ ] Fase 6: Herramientas y Registry
- [ ] Fase 7: Validación y Políticas
- [ ] Fase 8: Observabilidad
- [ ] Fase 9: Despliegue y DevOps
- [ ] Fase 10: Integración y Ejemplos
