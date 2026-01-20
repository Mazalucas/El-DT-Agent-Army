# Loops Autónomos: Documentación Técnica

## Visión General

El sistema de loops autónomos permite que las tareas se ejecuten iterativamente hasta alcanzar criterios de completitud verificables. El sistema decide automáticamente cuándo usar loops basándose en el nivel de autonomía calculado por `DTAutonomyEngine`.

## Arquitectura

### Componentes Principales

1. **AutonomousTaskExecutor**: Orquestador principal que ejecuta loops iterativos
2. **CompletionCriteria**: Verifica si una tarea está completa
3. **TaskProgressTracker**: Rastrea progreso entre iteraciones
4. **TaskCircuitBreaker**: Detecta y previene loops sin progreso
5. **TaskSessionManager**: Gestiona sesiones persistentes
6. **ValidationRunner**: Ejecuta tests, linters y builds
7. **FileChangeDetector**: Detecta cambios de archivos

### Flujo de Decisión

El sistema usa `DTAutonomyEngine` para calcular niveles de autonomía:

- **Nivel 4** (Confianza ≥ 0.9, Riesgo ≤ 0.2): Loop autónomo completo
  - Máximo 50 iteraciones
  - Validación estricta (tests + linter)
  - Circuit breaker activo
  - Sesiones persistentes

- **Nivel 3** (Confianza ≥ 0.8, Riesgo ≤ 0.4): Loop validado
  - Máximo 30 iteraciones
  - Validación estricta + validación cada iteración
  - Circuit breaker estricto
  - Sesiones persistentes

- **Nivel 2** (Confianza ≥ 0.6, Riesgo ≤ 0.6): Ejecución simple
  - 1 ejecución + validación
  - Si falla, escala (no loop)

- **Nivel 1** (Confianza < 0.6, Riesgo > 0.6): Escalar a humano
  - No ejecuta automáticamente
  - Tarea queda en estado "blocked"

## Criterios de Completitud

### CompletionCriteria

Verifica múltiples condiciones:

1. **Indicadores de Completitud**: Cuenta frases como "complete", "done", "finished"
2. **Exit Signal**: Requiere señal explícita `EXIT_SIGNAL: true` del agente
3. **Tests**: Verifica que tests pasen (si `tests_must_pass=True`)
4. **Linter**: Verifica que linter pase (si `linter_must_pass=True`)
5. **Build**: Verifica que build funcione (si `build_must_succeed=True`)
6. **Cambios de Archivos**: Requiere mínimo de cambios (default: 1)

### CompletionCriteriaFactory

Crea criterios automáticamente según tipo de tarea:

- **code_implementation**: Requiere tests, linter y build
- **documentation**: Solo requiere linter (formato)
- **research**: Solo requiere exit signal
- **general**: Criterios básicos

## Circuit Breaker

### Estados

- **CLOSED**: Operación normal
- **OPEN**: Circuito abierto, bloquea ejecución
- **HALF_OPEN**: Probando si el problema se resolvió

### Condiciones de Apertura

1. **Sin progreso**: N iteraciones sin cambios de archivos
2. **Errores repetidos**: Mismo error repetido N veces
3. **Estancamiento**: Sin progreso + errores repetidos

### Recuperación

- Espera 60 segundos antes de intentar HALF_OPEN
- Si hay progreso en HALF_OPEN, cierra el circuito
- Si no hay progreso, vuelve a OPEN

## Gestión de Sesiones

### TaskSession

Almacena:
- Historial de iteraciones
- Contexto acumulado
- Timestamp de creación y último acceso

### Expiración

- Sesiones expiran después de 24 horas (configurable)
- Se resetean automáticamente cuando:
  - Circuit breaker se abre
  - Interrupción manual
  - Proyecto completado
  - Agente asignado cambia

### Contexto Persistente

El contexto se acumula entre iteraciones:
- Outputs previos del agente
- Errores encontrados
- Archivos modificados
- Estado de validaciones

## Detección de Progreso

### TaskProgressTracker

Rastrea:
- Cambios de archivos por iteración
- Resultados de tests
- Errores encontrados
- Output del agente

### Detección de Progreso

Progreso se detecta cuando:
- Hay cambios de archivos
- Tests mejoran (de fallar a pasar)
- Errores disminuyen
- Output del agente indica avance

### Detección de Estancamiento

Estancamiento cuando:
- Sin progreso en últimas N iteraciones
- Mismos errores repetidos
- Sin cambios de archivos

## Validación Externa

### ValidationRunner

Ejecuta comandos externos:
- **Tests**: `pytest` (configurable)
- **Linter**: `flake8` (configurable)
- **Build**: Comando configurable (opcional)

### Configuración

Configuración en `.dt/config/validation.json`:
```json
{
  "test_command": "pytest",
  "test_args": ["-v"],
  "linter_command": "flake8",
  "linter_args": ["--max-line-length=100"],
  "build_command": "npm run build",
  "build_args": []
}
```

## Detección de Cambios de Archivos

### FileChangeDetector

Métodos de detección:
1. **Git diff** (preferido): Usa `git diff --name-only HEAD`
2. **Filesystem** (fallback): Compara timestamps de archivos

### Tracking Inicial

- Guarda estado inicial cuando comienza la tarea
- Compara estado actual con inicial
- Detecta archivos nuevos o modificados

## Integración con DTAutonomyEngine

### Modificación de `_execute_autonomously()`

Ahora decide automáticamente el modo según nivel:

```python
if decision.level == 4:
    return await self._execute_with_autonomous_loop(...)
elif decision.level == 3:
    return await self._execute_with_validated_loop(...)
elif decision.level == 2:
    return await self._execute_simple_with_validation(...)
```

### Métodos Nuevos

- `_execute_with_autonomous_loop()`: Para nivel 4
- `_execute_with_validated_loop()`: Para nivel 3
- `_execute_simple_with_validation()`: Para nivel 2
- `_execute_task_once()`: Helper para ejecución única

## Integración con DT

### Modificación de `assign_task()`

Ahora ejecuta automáticamente después de asignar:

```python
async def assign_task(self, task: Task, agent_role: AgentRole):
    # ... asignación ...
    
    # Crear situación y ejecutar
    situation = Situation(...)
    result = await self.autonomy_engine.decide_and_act(situation)
    
    # Actualizar estado según resultado
    if result.success:
        await self.update_task_status(task.id, "done")
    elif result.escalated:
        await self.update_task_status(task.id, "blocked")
```

## Configuración

### Parámetros Configurables

En `DTAutonomyEngine`:
- `autonomy_level_4`: Umbrales de confianza/riesgo
- `autonomy_level_3`: Umbrales de confianza/riesgo
- `autonomy_level_2`: Umbrales de confianza/riesgo

En `AutonomousTaskExecutor`:
- `max_iterations`: Máximo de iteraciones (default: 50)
- `enable_circuit_breaker`: Habilitar circuit breaker (default: True)
- `enable_sessions`: Habilitar sesiones (default: True)
- `circuit_breaker_strict`: Modo estricto (default: False)

En `TaskCircuitBreaker`:
- `no_progress_threshold`: Iteraciones sin progreso (default: 3)
- `same_error_threshold`: Errores repetidos (default: 5)

En `TaskSessionManager`:
- `expiration_hours`: Horas hasta expiración (default: 24)

## Troubleshooting

### Loop no termina

1. Verificar criterios de completitud
2. Verificar que agente emite `EXIT_SIGNAL: true`
3. Verificar que tests/linter pasan si están requeridos
4. Verificar que hay cambios de archivos

### Circuit breaker se abre prematuramente

1. Ajustar `no_progress_threshold`
2. Verificar que hay progreso real (cambios de archivos)
3. Revisar errores repetidos

### Sesión expira

1. Aumentar `expiration_hours`
2. Verificar que sesión se usa regularmente
3. Revisar si hay interrupciones manuales

### Validación falla

1. Verificar que comandos de test/linter están instalados
2. Verificar configuración en `.dt/config/validation.json`
3. Verificar permisos de ejecución

## Mejores Prácticas

1. **Criterios Claros**: Define criterios de completitud verificables
2. **Tests Automáticos**: Usa tests para validar completitud
3. **Monitoreo**: Revisa logs de progreso regularmente
4. **Límites**: Configura `max_iterations` apropiadamente
5. **Circuit Breaker**: Deja habilitado para prevenir loops infinitos

## Ejemplos de Uso

### Uso Básico (Automático)

```python
# El usuario solo llama assign_task()
task = await dt.get_next_task()
assignment = await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)

# El sistema automáticamente:
# - Decide nivel de autonomía
# - Ejecuta con loop si corresponde
# - Actualiza estado de tarea
```

### Verificación de Estado

```python
# Después de assign_task(), verificar estado
task = dt.task_storage.load_task(task_id)

if task.status == "done":
    print("Tarea completada exitosamente")
elif task.status == "blocked":
    print("Tarea requiere atención humana")
elif task.status == "in-progress":
    print("Tarea aún en ejecución")
```

## Referencias

- [RALPH_INTEGRATION_V2.md](RALPH_INTEGRATION_V2.md): Propuesta de integración completa
- [ARCHITECTURE.md](ARCHITECTURE.md): Arquitectura del sistema
- [USER_GUIDE.md](USER_GUIDE.md): Guía de usuario
