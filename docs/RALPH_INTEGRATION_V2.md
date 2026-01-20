# Propuesta de Integración V2: Loops Autónomos como Comportamiento por Defecto

## 🎯 Principio Fundamental

**Los loops autónomos NO son opcionales - son parte del comportamiento inteligente del sistema.**

El sistema decide automáticamente cuándo usar loops iterativos vs ejecución simple, basándose en:
- Nivel de autonomía calculado por `DTAutonomyEngine`
- Complejidad de la tarea
- Criterios de completitud verificables
- Historial de ejecuciones similares

---

## 🧠 Decisión Automática: ¿Cuándo usar Loops?

### Integración con DTAutonomyEngine Existente

Ya tienes `DTAutonomyEngine` que calcula niveles de autonomía (1-4). Usemos eso:

```
┌─────────────────────────────────────────────────────────────┐
│              FLUJO INTEGRADO (Automático)                   │
│                                                              │
│  1. DT.assign_task(task, agent_role)                         │
│     │                                                         │
│     └─> Crea Situation                                       │
│         │                                                     │
│         ▼                                                     │
│  2. DTAutonomyEngine.decide_and_act(situation)              │
│     │                                                         │
│     ├─> Analiza complejidad, riesgo, confianza              │
│     ├─> Calcula nivel de autonomía (1-4)                    │
│     │                                                         │
│     └─> Decision:                                            │
│         │                                                     │
│         ├─> Nivel 4 (Alta autonomía, bajo riesgo)           │
│         │   └─> [AUTOMÁTICO] Ejecutar con LOOP AUTÓNOMO     │
│         │       ├─> Hasta completitud verificable            │
│         │       ├─> Con circuit breaker                      │
│         │       └─> Con sesiones persistentes               │
│         │                                                     │
│         ├─> Nivel 3 (Buena autonomía, riesgo moderado)      │
│         │   └─> [AUTOMÁTICO] Ejecutar con LOOP VALIDADO    │
│         │       ├─> Hasta completitud verificable            │
│         │       ├─> Con validación en cada iteración         │
│         │       └─> Con circuit breaker estricto            │
│         │                                                     │
│         ├─> Nivel 2 (Autonomía baja)                        │
│         │   └─> [AUTOMÁTICO] Ejecutar SIMPLE con validación │
│         │       ├─> Una ejecución + validación               │
│         │       └─> Si falla, escalar (no loop)             │
│         │                                                     │
│         └─> Nivel 1 (Sin autonomía)                          │
│             └─> Escalar a humano                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Cambios en la Arquitectura

### 1. Modificar `DTAutonomyEngine._execute_autonomously()`

**ANTES** (actual):
```python
async def _execute_autonomously(
    self, situation: Situation, decision: Decision
) -> ActionResult:
    """Execute autonomous action."""
    # Esto solo retorna éxito simulado
    return ActionResult(
        success=True,
        action_taken=decision.action,
        result={"task_id": situation.task.id},
        escalated=False,
    )
```

**DESPUÉS** (con loops integrados):
```python
async def _execute_autonomously(
    self, situation: Situation, decision: Decision
) -> ActionResult:
    """
    Execute autonomous action.
    
    Ahora decide automáticamente el modo de ejecución:
    - Nivel 4: Loop autónomo completo
    - Nivel 3: Loop con validación
    - Nivel 2: Ejecución simple con validación
    """
    task = situation.task
    agent_role = task.assigned_agent
    
    if not agent_role:
        return ActionResult(
            success=False,
            action_taken="escalated",
            escalated=True,
            escalation_reason="No agent assigned"
        )
    
    # Decidir modo de ejecución basado en nivel de autonomía
    if decision.level == 4:
        # Alta autonomía → Loop autónomo completo
        return await self._execute_with_autonomous_loop(
            task=task,
            agent_role=agent_role,
            max_iterations=50,
            strict_validation=True
        )
    
    elif decision.level == 3:
        # Buena autonomía → Loop con validación estricta
        return await self._execute_with_validated_loop(
            task=task,
            agent_role=agent_role,
            max_iterations=30,
            validate_each_iteration=True
        )
    
    elif decision.level == 2:
        # Autonomía baja → Ejecución simple + validación
        return await self._execute_simple_with_validation(
            task=task,
            agent_role=agent_role
        )
    
    else:
        # No debería llegar aquí (nivel 1 escala)
        return ActionResult(
            success=False,
            action_taken="escalated",
            escalated=True
        )
```

### 2. Nuevos Métodos en `DTAutonomyEngine`

```python
class DTAutonomyEngine:
    # ... código existente ...
    
    async def _execute_with_autonomous_loop(
        self,
        task: Task,
        agent_role: AgentRole,
        max_iterations: int = 50,
        strict_validation: bool = True
    ) -> ActionResult:
        """
        Ejecuta tarea en loop autónomo completo.
        
        Usado para nivel 4 (alta autonomía).
        """
        executor = AutonomousTaskExecutor(
            dt=self.dt,  # Necesitamos referencia a DT
            max_iterations=max_iterations,
            enable_circuit_breaker=True,
            enable_sessions=True
        )
        
        completion_criteria = CompletionCriteria(
            tests_must_pass=strict_validation,
            linter_must_pass=strict_validation,
            agent_exit_signal=True,
            min_completion_indicators=2
        )
        
        return await executor.execute_until_complete(
            task=task,
            agent_role=agent_role,
            completion_criteria=completion_criteria
        )
    
    async def _execute_with_validated_loop(
        self,
        task: Task,
        agent_role: AgentRole,
        max_iterations: int = 30,
        validate_each_iteration: bool = True
    ) -> ActionResult:
        """
        Ejecuta tarea en loop con validación en cada iteración.
        
        Usado para nivel 3 (buena autonomía).
        """
        executor = AutonomousTaskExecutor(
            dt=self.dt,
            max_iterations=max_iterations,
            enable_circuit_breaker=True,
            enable_sessions=True,
            circuit_breaker_strict=True  # Más estricto
        )
        
        completion_criteria = CompletionCriteria(
            tests_must_pass=True,
            linter_must_pass=True,
            agent_exit_signal=True,
            min_completion_indicators=3  # Más estricto
        )
        
        return await executor.execute_until_complete(
            task=task,
            agent_role=agent_role,
            completion_criteria=completion_criteria,
            validate_each_iteration=validate_each_iteration
        )
    
    async def _execute_simple_with_validation(
        self,
        task: Task,
        agent_role: AgentRole
    ) -> ActionResult:
        """
        Ejecuta tarea una vez con validación.
        
        Usado para nivel 2 (autonomía baja).
        Si falla, escala (no intenta loop).
        """
        # Ejecutar una vez
        result = await self._execute_task_once(task, agent_role)
        
        # Validar resultado
        criteria = CompletionCriteria(
            tests_must_pass=True,
            linter_must_pass=False,  # Menos estricto
            agent_exit_signal=False
        )
        
        if criteria.is_complete(result):
            return result
        
        # Si no pasa validación, escalar (no loop)
        return ActionResult(
            success=False,
            action_taken="escalated",
            escalated=True,
            escalation_reason="Task validation failed after single execution"
        )
    
    async def _execute_task_once(
        self,
        task: Task,
        agent_role: AgentRole
    ) -> ActionResult:
        """
        Ejecuta tarea una vez (método helper).
        """
        # Implementación básica de ejecución única
        # Similar a lo que hacen los ejemplos actuales
        # ...
```

### 3. Modificar `DT.assign_task()` para Integrar Automáticamente

**ANTES** (actual):
```python
async def assign_task(
    self, task: Task, agent_role: AgentRole
) -> TaskAssignment:
    """Assign a task to an agent."""
    task.assigned_agent = agent_role
    task.update_status("in-progress")
    self.task_storage.save_task(task)
    return TaskAssignment(...)
```

**DESPUÉS** (con ejecución automática):
```python
async def assign_task(
    self, task: Task, agent_role: AgentRole
) -> TaskAssignment:
    """
    Assign a task to an agent and execute autonomously.
    
    El sistema decide automáticamente:
    - Si usar loop autónomo (nivel 4)
    - Si usar loop validado (nivel 3)
    - Si usar ejecución simple (nivel 2)
    - Si escalar a humano (nivel 1)
    """
    # Asignar tarea
    task.assigned_agent = agent_role
    task.update_status("in-progress")
    self.task_storage.save_task(task)
    
    # Crear situación para decisión de autonomía
    situation = Situation(
        task=task,
        context={"assigned_agent": agent_role},
        available_agents=[agent_role],
        constraints={}
    )
    
    # Decidir y ejecutar automáticamente
    if self.autonomy_engine:
        result = await self.autonomy_engine.decide_and_act(situation)
        
        # Actualizar estado según resultado
        if result.success:
            await self.update_task_status(task.id, "done", agent_result=result)
        elif result.escalated:
            await self.update_task_status(task.id, "blocked")
            # Log escalation reason
        else:
            await self.update_task_status(task.id, "in-progress")
    
    return TaskAssignment(
        task_id=task.id,
        agent_role=agent_role
    )
```

---

## 📊 Matriz de Decisión Automática

| Nivel Autonomía | Confianza | Riesgo | Modo Ejecución | Max Iteraciones | Validación |
|----------------|-----------|--------|----------------|-----------------|------------|
| **4** | ≥ 0.9 | ≤ 0.2 | Loop Autónomo Completo | 50 | Estricta (tests + linter) |
| **3** | ≥ 0.8 | ≤ 0.4 | Loop Validado | 30 | Estricta + validación cada iteración |
| **2** | ≥ 0.6 | ≤ 0.6 | Ejecución Simple | 1 | Básica (tests) |
| **1** | < 0.6 | > 0.6 | Escalar a Humano | 0 | N/A |

---

## 🎯 Criterios de Completitud Automáticos

El sistema determina automáticamente qué criterios usar según el tipo de tarea:

```python
class CompletionCriteriaFactory:
    """Factory para crear criterios según tipo de tarea."""
    
    @staticmethod
    def create_for_task(task: Task, autonomy_level: int) -> CompletionCriteria:
        """
        Crea criterios de completitud según tipo de tarea y nivel.
        """
        # Detectar tipo de tarea
        task_type = CompletionCriteriaFactory._detect_task_type(task)
        
        if task_type == "code_implementation":
            return CompletionCriteria(
                tests_must_pass=True,
                linter_must_pass=True,
                build_must_succeed=True,
                agent_exit_signal=True,
                min_completion_indicators=2 if autonomy_level >= 4 else 3
            )
        
        elif task_type == "documentation":
            return CompletionCriteria(
                tests_must_pass=False,
                linter_must_pass=True,  # Solo formato
                agent_exit_signal=True,
                min_completion_indicators=1
            )
        
        elif task_type == "research":
            return CompletionCriteria(
                tests_must_pass=False,
                linter_must_pass=False,
                agent_exit_signal=True,
                min_completion_indicators=2
            )
        
        # Default
        return CompletionCriteria(
            agent_exit_signal=True,
            min_completion_indicators=2
        )
    
    @staticmethod
    def _detect_task_type(task: Task) -> str:
        """Detecta tipo de tarea por tags/descripción."""
        desc_lower = task.description.lower()
        tags_lower = [t.lower() for t in task.tags]
        
        if any(word in desc_lower for word in ["implement", "code", "function", "class"]):
            return "code_implementation"
        elif any(word in desc_lower for word in ["document", "write", "readme", "guide"]):
            return "documentation"
        elif any(word in desc_lower for word in ["research", "investigate", "analyze"]):
            return "research"
        
        return "general"
```

---

## 🔄 Flujo Completo Integrado

```
Usuario llama:
  dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)
  
  ↓
  
DT.assign_task():
  1. Asigna tarea
  2. Crea Situation
  3. Llama autonomy_engine.decide_and_act()
  
  ↓
  
DTAutonomyEngine.decide_and_act():
  1. Analiza situación
  2. Calcula confianza y riesgo
  3. Decide nivel (1-4)
  
  ↓
  
Si nivel 4:
  → _execute_with_autonomous_loop()
    → AutonomousTaskExecutor.execute_until_complete()
      → Loop hasta completitud verificable
      
Si nivel 3:
  → _execute_with_validated_loop()
    → AutonomousTaskExecutor.execute_until_complete()
      → Loop con validación estricta
      
Si nivel 2:
  → _execute_simple_with_validation()
    → Ejecuta una vez + valida
    → Si falla, escala (no loop)
    
Si nivel 1:
  → Escala a humano
  
  ↓
  
DT actualiza estado de tarea según resultado
```

---

## ✅ Ventajas de Este Enfoque

1. **Transparente para el usuario**: Solo llama `assign_task()`, el sistema decide todo
2. **Inteligente**: Usa el sistema de autonomía existente para decidir
3. **Adaptativo**: Aprende de ejecuciones previas (ya está en `DTAutonomyEngine`)
4. **Seguro**: Niveles más bajos = menos iteraciones, más validación
5. **No rompe nada**: Los componentes nuevos se integran en el flujo existente

---

## 🚫 Lo que NO necesita el usuario

El usuario **NO** necesita:
- ❌ Llamar `enable_autonomous_loops()`
- ❌ Decidir cuándo usar loops
- ❌ Configurar criterios de completitud manualmente
- ❌ Saber sobre circuit breakers o sesiones

El usuario **SOLO** necesita:
- ✅ Llamar `dt.assign_task(task, agent_role)`
- ✅ El sistema hace el resto automáticamente

---

## 🔧 Componentes Nuevos (Igual que antes)

Los componentes nuevos siguen siendo los mismos, pero ahora se usan automáticamente:

1. **`AutonomousTaskExecutor`** - Usado automáticamente para niveles 4 y 3
2. **`CompletionCriteria`** - Creado automáticamente según tipo de tarea
3. **`TaskProgressTracker`** - Usado automáticamente en loops
4. **`TaskCircuitBreaker`** - Activado automáticamente en loops
5. **`TaskSessionManager`** - Usado automáticamente para mantener contexto

---

## 📝 Ejemplo de Uso (Sin cambios para el usuario)

```python
# El usuario hace esto (igual que antes):
system = AgentSystem()
dt = DT()
system.register_agent(dt)
await system.start()

tasks = await dt.parse_prd("prd.txt")

for task in tasks:
    # Esto es TODO lo que necesita hacer
    await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)
    
    # El sistema automáticamente:
    # - Decide nivel de autonomía
    # - Ejecuta con loop si corresponde (nivel 4/3)
    # - Ejecuta simple si corresponde (nivel 2)
    # - Escala si corresponde (nivel 1)
    # - Actualiza estado de tarea

await system.stop()
```

**El usuario no sabe ni le importa si se usó un loop o no. Solo sabe que la tarea se ejecutó.**

---

## 🎯 Resumen de Cambios

### ✅ Se MODIFICA (Integración automática)

1. **`DTAutonomyEngine._execute_autonomously()`**
   - Ahora decide automáticamente el modo de ejecución
   - Llama a los loops cuando corresponde

2. **`DT.assign_task()`**
   - Ahora ejecuta automáticamente después de asignar
   - Usa `DTAutonomyEngine` para decidir cómo ejecutar

3. **`DTAutonomyEngine`**
   - Se agregan métodos nuevos para diferentes modos de ejecución
   - Se integra con componentes de loops

### 🆕 Se AGREGA (Componentes nuevos, usados automáticamente)

1. **`AutonomousTaskExecutor`** - Usado automáticamente
2. **`CompletionCriteria`** - Creado automáticamente
3. **`TaskProgressTracker`** - Usado automáticamente
4. **`TaskCircuitBreaker`** - Activado automáticamente
5. **`TaskSessionManager`** - Usado automáticamente
6. **`CompletionCriteriaFactory`** - Crea criterios automáticamente

### ❌ NO se REEMPLAZA nada

- Todo sigue funcionando igual
- Solo se agrega inteligencia automática encima

---

## 💡 Filosofía del Diseño

**"El sistema debe ser inteligente por defecto, no requerir configuración manual."**

- El usuario no debería tener que pensar en loops, circuit breakers, o criterios
- El sistema debe usar su inteligencia (DTAutonomyEngine) para decidir automáticamente
- La complejidad está dentro del sistema, no expuesta al usuario
- El usuario solo dice "haz esta tarea" y el sistema decide cómo hacerla mejor
