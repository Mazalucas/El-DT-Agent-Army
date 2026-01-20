# Propuesta de Integración: Loops Autónomos (Inspirado en Ralph Wiggum)

## 📊 Arquitectura Actual vs Propuesta

### Flujo Actual (Sin Loops)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO ACTUAL                              │
│                                                              │
│  1. DT.parse_prd()                                           │
│     └─> Crea Task objects                                    │
│                                                              │
│  2. DT.assign_task(task, agent_role)                         │
│     └─> Task.status = "in-progress"                         │
│                                                              │
│  3. Agent.handle_message(task_message)                       │
│     └─> Ejecuta tarea UNA VEZ                               │
│     └─> Retorna TaskResult                                   │
│                                                              │
│  4. DT.update_task_status(task_id, "done")                  │
│     └─> Task.status = "done"                                │
│     └─> FIN                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Problema**: Si la tarea falla o está incompleta, se marca como "done" igual.

---

### Flujo Propuesto (Con Loops Autónomos)

```
┌─────────────────────────────────────────────────────────────┐
│              FLUJO CON LOOPS AUTÓNOMOS                      │
│                                                              │
│  1. DT.parse_prd()                                           │
│     └─> Crea Task objects                                    │
│                                                              │
│  2. DT.assign_task(task, agent_role)                         │
│     └─> Task.status = "in-progress"                         │
│                                                              │
│  3. [NUEVO] AutonomousTaskExecutor.execute_until_complete() │
│     │                                                         │
│     │  ┌─────────────────────────────────────┐             │
│     │  │  LOOP ITERATIVO (hasta completitud) │             │
│     │  │                                       │             │
│     │  │  Iteración N:                        │             │
│     │  │  1. Agent.handle_message(task)        │             │
│     │  │  2. TaskProgressTracker.record()      │             │
│     │  │  3. CompletionCriteria.check()        │             │
│     │  │     ├─> Tests pasan?                  │             │
│     │  │     ├─> Linter pasa?                  │             │
│     │  │     ├─> Agent dice EXIT_SIGNAL?       │             │
│     │  │     └─> Hay progreso?                 │             │
│     │  │                                       │             │
│     │  │  4. Si NO completo:                   │             │
│     │  │     ├─> CircuitBreaker.check()       │             │
│     │  │     │   └─> ¿Está estancado?          │             │
│     │  │     │       ├─> Sí: ABRIR circuito    │             │
│     │  │     │       └─> No: CONTINUAR         │             │
│     │  │     │                                   │             │
│     │  │     ├─> TaskSessionManager.get()       │             │
│     │  │     │   └─> Recupera contexto previo  │             │
│     │  │     │                                   │             │
│     │  │     └─> REINICIAR con contexto        │             │
│     │  │                                       │             │
│     │  │  5. Si SÍ completo:                   │             │
│     │  │     └─> SALIR del loop                │             │
│     │  └─────────────────────────────────────┘             │
│     │                                                         │
│     └─> TaskResult final                                     │
│                                                              │
│  4. DT.update_task_status(task_id, "done")                  │
│     └─> Task.status = "done"                                │
│     └─> FIN                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Componentes: Nuevos vs Existentes

### ✅ Componentes Existentes (NO se modifican)

1. **`DT` (agents/dt.py)**
   - ✅ Se mantiene igual
   - ✅ Sigue creando tareas, asignando, etc.
   - ✅ Solo se agrega un método nuevo opcional

2. **`Agent` (core/agent.py)**
   - ✅ Se mantiene igual
   - ✅ Los agentes siguen ejecutando igual
   - ✅ No necesitan saber que están en un loop

3. **`TaskStorage` (core/task_storage.py)**
   - ✅ Se mantiene igual
   - ✅ Sigue guardando tareas igual

4. **`TaskScheduler` (core/task_scheduler.py)**
   - ✅ Se mantiene igual
   - ✅ Sigue programando tareas igual

5. **`DTAutonomyEngine` (core/autonomy.py)**
   - ✅ Se mantiene igual
   - ✅ Sigue decidiendo autonomía igual
   - ⚠️ Podría usarse DENTRO del loop para decisiones

6. **`Task` (core/models.py)**
   - ✅ Se mantiene igual
   - ✅ Mismo modelo de datos
   - ⚠️ Podría agregarse metadata opcional para loops

### 🆕 Componentes Nuevos (Se agregan)

1. **`AutonomousTaskExecutor`** (NUEVO)
   - **Ubicación**: `src/agents_army/core/autonomous_executor.py`
   - **Responsabilidad**: Orquestar el loop iterativo
   - **Depende de**: DT, AgentSystem, TaskProgressTracker, CompletionCriteria, CircuitBreaker, TaskSessionManager

2. **`CompletionCriteria`** (NUEVO)
   - **Ubicación**: `src/agents_army/core/completion.py`
   - **Responsabilidad**: Verificar si una tarea está completa
   - **Depende de**: Task, TaskResult, sistema de tests/linters

3. **`TaskProgressTracker`** (NUEVO)
   - **Ubicación**: `src/agents_army/core/progress_tracker.py`
   - **Responsabilidad**: Rastrear progreso entre iteraciones
   - **Depende de**: TaskStorage

4. **`TaskCircuitBreaker`** (NUEVO)
   - **Ubicación**: `src/agents_army/core/circuit_breaker.py`
   - **Responsabilidad**: Detectar loops sin progreso
   - **Depende de**: TaskProgressTracker

5. **`TaskSessionManager`** (NUEVO)
   - **Ubicación**: `src/agents_army/core/session_manager.py`
   - **Responsabilidad**: Gestionar sesiones persistentes
   - **Depende de**: TaskStorage, MemorySystem

---

## 🔗 Integración: Cómo se Conecta Todo

### Opción 1: Modo Opcional (Recomendado para empezar)

```python
# En DT (agents/dt.py) - AGREGAR método nuevo, NO modificar existentes

class DT(Agent):
    # ... código existente sin cambios ...
    
    def __init__(self, ...):
        # ... código existente ...
        
        # [NUEVO] Inicializar executor autónomo (opcional)
        self.autonomous_executor: Optional[AutonomousTaskExecutor] = None
    
    def enable_autonomous_loops(
        self,
        max_iterations: int = 50,
        enable_circuit_breaker: bool = True,
        enable_sessions: bool = True
    ) -> None:
        """
        Habilita loops autónomos para tareas.
        
        Esto es OPCIONAL - el sistema funciona igual sin esto.
        """
        from agents_army.core.autonomous_executor import AutonomousTaskExecutor
        
        self.autonomous_executor = AutonomousTaskExecutor(
            dt=self,
            max_iterations=max_iterations,
            enable_circuit_breaker=enable_circuit_breaker,
            enable_sessions=enable_sessions
        )
    
    async def execute_task_with_loop(
        self,
        task: Task,
        agent_role: AgentRole,
        completion_criteria: Optional[CompletionCriteria] = None
    ) -> TaskResult:
        """
        [NUEVO] Ejecuta una tarea en loop hasta completitud.
        
        Si autonomous_executor no está habilitado, ejecuta normal (una vez).
        """
        if not self.autonomous_executor:
            # Fallback al comportamiento normal
            return await self._execute_task_once(task, agent_role)
        
        return await self.autonomous_executor.execute_until_complete(
            task=task,
            agent_role=agent_role,
            completion_criteria=completion_criteria
        )
    
    async def _execute_task_once(
        self,
        task: Task,
        agent_role: AgentRole
    ) -> TaskResult:
        """
        [NUEVO] Método helper para ejecución normal (sin loop).
        Esto es básicamente lo que ya hacen los ejemplos actuales.
        """
        # Asignar tarea
        await self.assign_task(task, agent_role)
        
        # Enviar mensaje al agente
        message = AgentMessage(
            from_role=self.role,
            to_role=agent_role,
            type=MessageType.TASK_REQUEST,
            payload={"task_id": task.id, "description": task.description}
        )
        
        if self.system:
            agent = self.system.get_agent(agent_role)
            if agent:
                response = await agent.handle_message(message)
                # ... procesar respuesta ...
        
        return TaskResult(task_id=task.id, status="completed")
```

**Uso**:

```python
# Modo tradicional (sin cambios)
task = await dt.get_next_task()
await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)
# ... ejecuta una vez ...

# Modo con loops (nuevo, opcional)
dt.enable_autonomous_loops(max_iterations=50)
task = await dt.get_next_task()
result = await dt.execute_task_with_loop(
    task=task,
    agent_role=AgentRole.BACKEND_ARCHITECT,
    completion_criteria=CompletionCriteria(
        tests_must_pass=True,
        linter_must_pass=True
    )
)
# ... ejecuta hasta completitud ...
```

### Opción 2: Integración Transparente (Más avanzado)

Modificar `assign_task()` para que automáticamente use loops si están habilitados:

```python
class DT(Agent):
    async def assign_task(
        self,
        task: Task,
        agent_role: AgentRole,
        use_autonomous_loop: bool = False  # [NUEVO] Flag opcional
    ) -> TaskAssignment:
        """
        Assign a task to an agent.
        
        Si use_autonomous_loop=True y autonomous_executor está habilitado,
        ejecuta en loop hasta completitud.
        """
        assignment = TaskAssignment(
            task_id=task.id,
            agent_role=agent_role
        )
        
        task.assigned_agent = agent_role
        task.update_status("in-progress")
        self.task_storage.save_task(task)
        
        # [NUEVO] Si está habilitado, ejecutar en loop
        if use_autonomous_loop and self.autonomous_executor:
            await self.autonomous_executor.execute_until_complete(
                task=task,
                agent_role=agent_role
            )
        # Si no, comportamiento normal (el agente ejecuta cuando recibe mensaje)
        
        return assignment
```

---

## 📐 Diagrama de Dependencias

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                       │
│  (Tu código que usa Agents_Army)                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ usa
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    DT (agents/dt.py)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Métodos Existentes (sin cambios):                   │  │
│  │  - parse_prd()                                        │  │
│  │  - assign_task()                                     │  │
│  │  - update_task_status()                              │  │
│  │  - get_next_task()                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Métodos Nuevos (opcionales):                        │  │
│  │  - enable_autonomous_loops()                        │  │
│  │  - execute_task_with_loop()                          │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ usa (si está habilitado)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         AutonomousTaskExecutor (NUEVO)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - execute_until_complete()                          │  │
│  │  - _execute_iteration()                              │  │
│  │  - _check_completion()                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────┬───────┬───────┬───────┬───────┬───────────────────────┘
      │       │       │       │       │
      │       │       │       │       │ usa
      ▼       ▼       ▼       ▼       ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│TaskProg│ │Complet│ │Circuit │ │Session │ │ AgentSystem  │
│Tracker │ │Criteria│ │Breaker │ │Manager │ │ (existente)  │
│(NUEVO) │ │(NUEVO) │ │(NUEVO) │ │(NUEVO) │ │              │
└────┬───┘ └───┬────┘ └───┬────┘ └───┬────┘ └───────┬────────┘
     │        │          │          │             │
     │        │          │          │             │ usa
     │        │          │          │             ▼
     │        │          │          │    ┌─────────────────┐
     │        │          │          │    │ Agent (existente)│
     │        │          │          │    │ - handle_message │
     │        │          │          │    └─────────────────┘
     │        │          │          │
     │        │          │          │ usa
     │        │          │          ▼
     │        │          │    ┌─────────────────┐
     │        │          │    │ MemorySystem     │
     │        │          │    │ (existente)      │
     │        │          │    └─────────────────┘
     │        │          │
     │        │          │ usa
     │        │          ▼
     │        │    ┌─────────────────┐
     │        │    │ TaskProgress     │
     │        │    │ Tracker         │
     │        │    └─────────────────┘
     │        │
     │        │ usa
     │        ▼
     │   ┌─────────────────┐
     │   │ TaskStorage      │
     │   │ (existente)     │
     │   └─────────────────┘
     │
     │ usa
     ▼
┌─────────────────┐
│ Task (model)    │
│ (existente)     │
└─────────────────┘
```

---

## 🎯 Resumen: Qué se Agrega, Qué se Modifica, Qué se Reemplaza

### ✅ Se AGREGA (Nuevos componentes)

1. **`AutonomousTaskExecutor`** - Orquestador principal del loop
2. **`CompletionCriteria`** - Verificación de completitud
3. **`TaskProgressTracker`** - Tracking de progreso
4. **`TaskCircuitBreaker`** - Protección contra loops infinitos
5. **`TaskSessionManager`** - Gestión de sesiones

### 🔧 Se MODIFICA (Extensiones opcionales)

1. **`DT`** - Se agregan métodos nuevos:
   - `enable_autonomous_loops()` - Habilita la funcionalidad
   - `execute_task_with_loop()` - Ejecuta con loop (opcional)
   - Los métodos existentes NO cambian

2. **`Task` (modelo)** - Se podría agregar metadata opcional:
   - `metadata["loop_config"]` - Configuración de loop
   - `metadata["iteration_count"]` - Contador de iteraciones
   - Los campos existentes NO cambian

### ❌ NO se REEMPLAZA nada

- Todos los componentes existentes siguen funcionando igual
- El comportamiento por defecto es el mismo (sin loops)
- Los loops son una funcionalidad adicional opcional

---

## 🚀 Plan de Implementación Incremental

### Fase 1: Fundamentos (Sin romper nada)

1. Crear `CompletionCriteria` básico
2. Crear `TaskProgressTracker` básico
3. Agregar método `enable_autonomous_loops()` a DT (vacío por ahora)
4. **Test**: Verificar que el sistema sigue funcionando igual

### Fase 2: Loop básico

1. Crear `AutonomousTaskExecutor` básico
2. Implementar `execute_until_complete()` simple (sin protecciones)
3. Integrar con DT
4. **Test**: Verificar que funciona opcionalmente

### Fase 3: Protecciones

1. Crear `TaskCircuitBreaker`
2. Integrar con `AutonomousTaskExecutor`
3. **Test**: Verificar que detecta loops sin progreso

### Fase 4: Sesiones

1. Crear `TaskSessionManager`
2. Integrar con MemorySystem
3. **Test**: Verificar persistencia de contexto

### Fase 5: Validación avanzada

1. Integrar con tests (pytest, etc.)
2. Integrar con linters (flake8, black, etc.)
3. **Test**: Verificar validación automática

---

## 💡 Ejemplo de Uso Completo

```python
import asyncio
from agents_army.core.system import AgentSystem
from agents_army.agents.dt import DT
from agents_army.core.completion import CompletionCriteria
from agents_army.protocol.types import AgentRole

async def main():
    # Setup normal (sin cambios)
    system = AgentSystem()
    dt = DT()
    system.register_agent(dt)
    await system.start()
    
    # [NUEVO] Habilitar loops autónomos (opcional)
    dt.enable_autonomous_loops(
        max_iterations=50,
        enable_circuit_breaker=True,
        enable_sessions=True
    )
    
    # Parsear PRD (sin cambios)
    tasks = await dt.parse_prd("prd.txt")
    
    # Ejecutar tareas (dos opciones)
    
    # Opción 1: Modo tradicional (sin cambios)
    task1 = tasks[0]
    await dt.assign_task(task1, AgentRole.BACKEND_ARCHITECT)
    # ... agente ejecuta una vez ...
    
    # Opción 2: Modo con loop (nuevo)
    task2 = tasks[1]
    result = await dt.execute_task_with_loop(
        task=task2,
        agent_role=AgentRole.BACKEND_ARCHITECT,
        completion_criteria=CompletionCriteria(
            tests_must_pass=True,
            linter_must_pass=True,
            agent_exit_signal=True
        )
    )
    # ... agente ejecuta hasta completitud ...
    
    await system.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ✅ Conclusión

**La propuesta es una EXTENSIÓN, no un reemplazo:**

- ✅ No rompe código existente
- ✅ Es completamente opcional
- ✅ Se puede habilitar gradualmente
- ✅ Los componentes existentes no cambian
- ✅ Se agregan nuevos componentes modulares
- ✅ Se puede probar sin afectar producción

**Es como agregar un "modo turbo" a un auto: el auto funciona igual, pero ahora tiene una opción adicional para ir más rápido cuando la necesites.**
