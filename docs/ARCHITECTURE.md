# Arquitectura del Sistema: Agents_Army

## Visión General

Este documento describe la arquitectura de alto nivel del framework **Agents_Army**, mostrando cómo se organizan los componentes, sus responsabilidades y cómo interactúan entre sí.

## Principios Arquitectónicos

1. **Modularidad**: Componentes independientes y reutilizables
2. **Separación de Responsabilidades**: Cada componente tiene un propósito claro
3. **Extensibilidad**: Fácil agregar nuevos agentes, herramientas y protocolos
4. **Observabilidad**: Logging y métricas integradas
5. **Testabilidad**: Componentes fácilmente testeables en aislamiento

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  (Tu aplicación que usa Agents_Army)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Agent System                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Coordinator                              │  │
│  │  - Task Management                                   │  │
│  │  - Agent Orchestration                               │  │
│  │  - Result Synthesis                                  │  │
│  └───────────────┬──────────────────────────────────────┘  │
│                  │                                           │
│  ┌───────────────┴───────────────┐                         │
│  │                               │                           │
│  ▼                               ▼                           │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │  Specialist  │      │  Specialist  │                    │
│  │  (Researcher)│      │   (Writer)   │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                              │
│         └──────────┬──────────┘                              │
│                    │                                         │
│                    ▼                                         │
│         ┌──────────────────────┐                           │
│         │     Validator         │                           │
│         └──────────┬────────────┘                           │
└────────────────────┼────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Protocol Layer                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Message Router / Bus                         │  │
│  │  - Message Routing                                    │  │
│  │  - Serialization / Deserialization                    │  │
│  │  - Validation                                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Infrastructure Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │    Memory    │  │    Tools     │  │   Logging    │    │
│  │   System     │  │   Registry   │  │   System     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. Agent System (Sistema de Agentes)

**Responsabilidad**: Punto de entrada principal, gestiona el ciclo de vida de todos los agentes.

**Componentes**:
- **Agent Registry**: Registro de agentes disponibles
- **Lifecycle Manager**: Gestión del ciclo de vida (start, stop, restart)
- **Configuration Manager**: Gestión de configuración

**Interfaces**:
```python
class AgentSystem:
    def register_agent(self, agent: Agent) -> None
    def get_agent(self, role: AgentRole) -> Agent
    def execute_task(self, task: Task) -> TaskResult
    def shutdown(self) -> None
```

### 2. Coordinator (Coordinador)

**Responsabilidad**: Orquestación de tareas y coordinación entre agentes.

**Componentes**:
- **Task Decomposer**: Divide tareas complejas en subtareas
- **Task Scheduler**: Programa y asigna tareas
- **Result Synthesizer**: Combina resultados de múltiples agentes

**Interfaces**:
```python
class Coordinator(Agent):
    async def execute_task(self, task: Task) -> TaskResult
    async def decompose_task(self, task: Task) -> List[SubTask]
    async def assign_task(self, subtask: SubTask, agent: Agent) -> None
    async def synthesize_results(self, results: List[TaskResult]) -> TaskResult
```

### 3. Specialist (Especialista)

**Responsabilidad**: Ejecución de tareas especializadas.

**Componentes**:
- **Task Executor**: Ejecuta tareas de su dominio
- **Tool Manager**: Gestiona herramientas disponibles
- **Context Manager**: Gestiona contexto de ejecución

**Interfaces**:
```python
class Specialist(Agent):
    async def execute(self, task: Task) -> TaskResult
    def get_available_tools(self) -> List[Tool]
    async def use_tool(self, tool: Tool, params: dict) -> dict
```

### 4. Validator (Validador)

**Responsabilidad**: Validación de outputs y cumplimiento de políticas.

**Componentes**:
- **Quality Checker**: Verifica calidad del output
- **Policy Enforcer**: Aplica políticas y guardrails
- **Issue Detector**: Detecta problemas y errores

**Interfaces**:
```python
class Validator(Agent):
    async def validate(self, content: Any, rules: List[ValidationRule]) -> ValidationResult
    def check_quality(self, content: Any) -> QualityScore
    def check_policies(self, content: Any) -> PolicyCheckResult
```

### 5. Memory System (Sistema de Memoria)

**Responsabilidad**: Gestión de contexto persistente.

**Componentes**:
- **Storage Backend**: Backend de almacenamiento (local, DB, vector DB)
- **Retrieval Engine**: Motor de búsqueda y recuperación
- **Retention Manager**: Gestión de políticas de retención

**Interfaces**:
```python
class MemorySystem:
    async def store(self, key: str, value: Any, metadata: dict) -> None
    async def retrieve(self, query: MemoryQuery) -> List[MemoryItem]
    async def delete(self, key: str) -> None
    def get_retention_policy(self, key: str) -> RetentionPolicy
```

### 6. Protocol Layer (Capa de Protocolo)

**Responsabilidad**: Comunicación estandarizada entre componentes.

**Componentes**:
- **Message Router**: Enrutamiento de mensajes
- **Message Serializer**: Serialización/deserialización
- **Message Validator**: Validación de esquemas

**Interfaces**:
```python
class MessageRouter:
    async def send(self, message: AgentMessage) -> None
    async def receive(self, role: AgentRole) -> AgentMessage
    def register_handler(self, message_type: MessageType, handler: Callable) -> None

class MessageSerializer:
    def serialize(self, message: AgentMessage) -> bytes
    def deserialize(self, data: bytes) -> AgentMessage
```

### 7. Tools Registry (Registro de Herramientas)

**Responsabilidad**: Gestión de herramientas disponibles.

**Componentes**:
- **Tool Registry**: Registro de herramientas
- **Tool Executor**: Ejecutor de herramientas
- **Tool Validator**: Validador de parámetros

**Interfaces**:
```python
class ToolRegistry:
    def register(self, tool: Tool) -> None
    def get_tool(self, name: str) -> Tool
    def list_tools(self, category: str = None) -> List[Tool]

class Tool:
    name: str
    description: str
    parameters: dict
    
    async def execute(self, params: dict) -> dict
```

## Flujo de Datos

### Flujo 1: Ejecución de Tarea Simple

```
User Request
    │
    ▼
AgentSystem.execute_task()
    │
    ▼
Coordinator.receive_task()
    │
    ▼
Coordinator.decompose_task()
    │
    ▼
Coordinator.assign_task() ──► MessageRouter.send()
    │                              │
    │                              ▼
    │                    Specialist.receive()
    │                              │
    │                              ▼
    │                    Specialist.execute()
    │                              │
    │                              ▼
    │                    ToolRegistry.get_tool()
    │                              │
    │                              ▼
    │                    Tool.execute()
    │                              │
    │                              ▼
    │                    Specialist.send_response()
    │                              │
    │                              ▼
    │                    MessageRouter.send()
    │                              │
    ▼                              │
Coordinator.receive_response()     │
    │                              │
    ▼                              │
Coordinator.validate() ──► Validator.validate()
    │                              │
    ▼                              │
Coordinator.synthesize()           │
    │                              │
    ▼                              │
MemorySystem.store()               │
    │                              │
    ▼                              │
User Response                      │
```

### Flujo 2: Consulta de Memoria

```
Specialist needs context
    │
    ▼
MemorySystem.retrieve()
    │
    ▼
StorageBackend.query()
    │
    ▼
RetrievalEngine.search()
    │
    ▼
RetrievalEngine.rank()
    │
    ▼
MemorySystem.return_results()
    │
    ▼
Specialist receives context
```

## Capas de la Arquitectura

### Capa de Aplicación
- **Responsabilidad**: Lógica de negocio específica del proyecto
- **Dependencias**: Usa Agents_Army, no es parte del framework

### Capa de Agentes
- **Responsabilidad**: Lógica de agentes y coordinación
- **Componentes**: Coordinator, Specialist, Validator
- **Dependencias**: Protocol Layer, Infrastructure Layer

### Capa de Protocolo
- **Responsabilidad**: Comunicación y mensajería
- **Componentes**: MessageRouter, MessageSerializer, MessageValidator
- **Dependencias**: Infrastructure Layer

### Capa de Infraestructura
- **Responsabilidad**: Servicios de bajo nivel
- **Componentes**: Memory System, Tools Registry, Logging
- **Dependencias**: Ninguna (capa base)

## Patrones de Diseño Utilizados

### 1. Registry Pattern
- **Uso**: ToolRegistry, AgentRegistry
- **Propósito**: Centralizar registro y búsqueda de componentes

### 2. Strategy Pattern
- **Uso**: Diferentes backends de memoria, diferentes validadores
- **Propósito**: Intercambiar algoritmos en tiempo de ejecución

### 3. Observer Pattern
- **Uso**: Sistema de logging, métricas
- **Propósito**: Notificar eventos a múltiples observadores

### 4. Factory Pattern
- **Uso**: Creación de agentes, creación de herramientas
- **Propósito**: Encapsular lógica de creación

### 5. Mediator Pattern
- **Uso**: Coordinator como mediador entre agentes
- **Propósito**: Reducir acoplamiento directo entre agentes

## Extensibilidad

### Agregar un Nuevo Tipo de Agente

1. Crear clase que extienda `Agent`
2. Implementar interfaces requeridas
3. Registrar en `AgentRegistry`
4. Configurar en `agents_config.yaml`

### Agregar una Nueva Herramienta

1. Crear clase que extienda `Tool`
2. Implementar método `execute()`
3. Registrar en `ToolRegistry`
4. Documentar parámetros y uso

### Agregar un Nuevo Backend de Memoria

1. Implementar interfaz `MemoryBackend`
2. Implementar métodos `store()`, `retrieve()`, `delete()`
3. Registrar en `MemorySystem`
4. Configurar en `agents_config.yaml`

## Seguridad

### Autenticación y Autorización

- Autenticación mutua entre agentes
- Control de acceso basado en roles
- Validación de permisos antes de ejecutar acciones

### Cifrado

- Cifrado TLS para comunicación en red
- Cifrado de datos sensibles en memoria
- Firma digital para mensajes críticos

### Validación

- Validación de inputs contra esquemas
- Sanitización de datos
- Rate limiting por agente

## Observabilidad

### Logging

- Logs estructurados (JSON)
- Niveles de log configurables
- Contexto de ejecución en cada log

### Métricas

- Tiempo de ejecución por tarea
- Tasa de éxito/fallo
- Uso de recursos (tokens, memoria)
- Latencia de comunicación

### Trazabilidad

- IDs de correlación para rastrear flujos
- Historial completo de ejecución
- Versionado de prompts y configuraciones

## Escalabilidad

### Horizontal

- Múltiples instancias de agentes
- Balanceo de carga
- Distribución de tareas

### Vertical

- Optimización de recursos
- Caching inteligente
- Procesamiento asíncrono

## Testing

### Unit Tests
- Componentes individuales
- Mocks para dependencias
- Tests de interfaces

### Integration Tests
- Flujos completos
- Comunicación entre componentes
- Backends reales (opcional)

### E2E Tests
- Escenarios completos de usuario
- Validación de resultados
- Performance testing

## Próximos Pasos de Implementación

1. **Fase 1: Core**
   - Agent base class
   - Message protocol implementation
   - Basic coordinator

2. **Fase 2: Agents**
   - Specialist implementation
   - Validator implementation
   - Memory system

3. **Fase 3: Infrastructure**
   - Tools registry
   - Logging system
   - Configuration management

4. **Fase 4: Advanced**
   - Advanced coordination patterns
   - Distributed execution
   - Advanced memory backends
