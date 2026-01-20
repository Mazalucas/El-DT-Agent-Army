# Solución de Problemas: Agents_Army

## Visión General

Esta guía ayuda a diagnosticar y resolver problemas comunes en **Agents_Army**.

## Problemas Comunes

### 1. El DT no Inicializa

**Síntomas**:
- Error al crear DT
- No se puede inicializar proyecto

**Diagnóstico**:
```python
# Verificar configuración
try:
    dt = DT()
except Exception as e:
    print(f"Error: {e}")
    # Verificar que existe .dt/
    # Verificar que existe config/
```

**Soluciones**:
1. Verificar estructura de directorios:
```bash
.dt/
├── config/
│   └── dt_config.json
└── docs/
    └── prd.txt
```

2. Verificar permisos de archivos
3. Verificar variables de entorno (API keys)

### 2. Agentes no Responden

**Síntomas**:
- Tareas quedan en "pending"
- Timeouts frecuentes
- Agentes no ejecutan

**Diagnóstico**:
```python
# Verificar estado de agentes
system = AgentSystem.get_instance()
for agent in system.get_agents():
    print(f"{agent.role}: {agent.status}")
    print(f"  - Disponible: {agent.is_available()}")
    print(f"  - Última actividad: {agent.last_activity}")

# Verificar logs
logs = await system.get_agent_logs()
for log in logs:
    if log.level == "ERROR":
        print(f"Error en {log.agent}: {log.message}")
```

**Soluciones**:
1. Verificar que agentes están registrados
2. Verificar conectividad con LLM APIs
3. Verificar rate limits
4. Verificar que agentes tienen herramientas necesarias

### 3. El DT no Actúa Autónomamente

**Síntomas**:
- Todas las decisiones se escalan
- El DT siempre consulta

**Diagnóstico**:
```python
# Verificar configuración de autonomía
config = dt.get_config()
print(f"Autonomía habilitada: {config.autonomy.enabled}")
print(f"Umbral autónomo: {config.autonomy.thresholds.autonomous}")

# Verificar decisiones recientes
decisions = await dt.get_recent_decisions(limit=10)
for decision in decisions:
    print(f"{decision.action}: conf={decision.confidence}, risk={decision.risk}")
```

**Soluciones**:
1. Ajustar umbrales de autonomía:
```yaml
dt:
  autonomy:
    thresholds:
      autonomous: 0.7  # Bajar umbral
```

2. Verificar reglas que bloquean autonomía
3. Revisar historial de decisiones fallidas

### 4. Costos Muy Altos

**Síntomas**:
- Costos diarios exceden presupuesto
- Llamadas excesivas a LLMs

**Diagnóstico**:
```python
# Ver costos por agente
costs = await dt.get_cost_breakdown()
for agent, cost in costs.by_agent.items():
    print(f"{agent}: ${cost}")

# Ver costos por modelo
for model, cost in costs.by_model.items():
    print(f"{model}: ${cost}")

# Ver tareas más costosas
expensive_tasks = await dt.get_expensive_tasks(limit=10)
for task in expensive_tasks:
    print(f"{task.id}: ${task.cost}")
```

**Soluciones**:
1. Usar modelos más económicos para tareas simples
2. Habilitar cache
3. Optimizar prompts para reducir tokens
4. Revisar tareas que fallan y se reintentan

### 5. Tareas se Bloquean

**Síntomas**:
- Tareas en estado "blocked"
- Dependencias no se resuelven

**Diagnóstico**:
```python
# Ver tareas bloqueadas
blocked = await dt.get_tasks(status="blocked")
for task in blocked:
    print(f"{task.id}: {task.title}")
    print(f"  Dependencias: {task.dependencies}")
    
    # Verificar dependencias
    for dep_id in task.dependencies:
        dep_task = await dt.get_task(dep_id)
        print(f"    {dep_id}: {dep_task.status}")
```

**Soluciones**:
1. Completar tareas dependientes
2. Revisar dependencias circulares
3. Eliminar dependencias innecesarias

### 6. Errores de Validación

**Síntomas**:
- Outputs rechazados por validator
- Score de calidad bajo

**Diagnóstico**:
```python
# Ver errores de validación
validation_errors = await dt.get_validation_errors()
for error in validation_errors:
    print(f"Tarea {error.task_id}:")
    print(f"  Score: {error.score}")
    print(f"  Issues: {error.issues}")
```

**Soluciones**:
1. Revisar criterios de validación
2. Ajustar instrucciones del agente
3. Proporcionar más contexto
4. Revisar ejemplos de outputs esperados

### 7. Problemas de Memoria

**Síntomas**:
- Contexto se pierde
- Memoria no persiste
- Búsquedas no encuentran información

**Diagnóstico**:
```python
# Verificar conexión a memoria
memory = MemorySystem.get_instance()
status = await memory.check_health()
print(f"Memoria conectada: {status.connected}")
print(f"Items almacenados: {status.item_count}")

# Probar almacenamiento
test_key = "test_key"
await memory.store(test_key, {"test": "data"})
retrieved = await memory.retrieve(test_key)
print(f"Recuperado: {retrieved is not None}")
```

**Soluciones**:
1. Verificar conexión a base de datos
2. Verificar permisos de escritura
3. Verificar políticas de retención
4. Limpiar memoria antigua si es necesario

### 8. Problemas de Comunicación

**Síntomas**:
- Mensajes no llegan
- Agentes no se comunican
- Timeouts en comunicación

**Diagnóstico**:
```python
# Verificar router de mensajes
router = MessageRouter.get_instance()
status = router.get_status()
print(f"Router activo: {status.active}")
print(f"Mensajes en cola: {status.queue_size}")

# Ver mensajes recientes
recent = await router.get_recent_messages(limit=10)
for msg in recent:
    print(f"{msg.from_role} → {msg.to_role}: {msg.type}")
    if msg.status == "failed":
        print(f"  Error: {msg.error}")
```

**Soluciones**:
1. Verificar que agentes están registrados
2. Verificar permisos de comunicación
3. Revisar timeouts
4. Verificar red/conectividad

## Comandos de Diagnóstico

### Health Check Completo

```python
async def health_check():
    """Health check completo del sistema."""
    checks = {
        "dt": await dt.health_check(),
        "agents": await system.agents_health_check(),
        "memory": await memory.health_check(),
        "tools": await tools.health_check(),
        "protocol": await protocol.health_check()
    }
    
    all_healthy = all(c["healthy"] for c in checks.values())
    
    return {
        "overall": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }
```

### Diagnostic Report

```python
async def generate_diagnostic_report():
    """Genera reporte de diagnóstico completo."""
    report = {
        "system": {
            "version": get_version(),
            "uptime": get_uptime(),
            "agents_loaded": len(system.get_agents()),
            "tasks_total": await dt.get_task_count()
        },
        "performance": {
            "avg_latency": await get_avg_latency(),
            "error_rate": await get_error_rate(),
            "success_rate": await get_success_rate()
        },
        "costs": {
            "daily": await get_daily_cost(),
            "trend": await get_cost_trend()
        },
        "issues": await identify_issues()
    }
    
    return report
```

## Logs y Debugging

### Habilitar Debug Logging

```python
import logging

# Habilitar debug
logging.basicConfig(level=logging.DEBUG)

# O específico por componente
logger = logging.getLogger("agents_army.dt")
logger.setLevel(logging.DEBUG)
```

### Ver Logs Estructurados

```python
# Ver logs recientes
logs = await dt.get_logs(
    level="DEBUG",
    limit=100,
    component="dt"
)

for log in logs:
    print(f"{log.timestamp}: {log.level} - {log.message}")
    if log.metadata:
        print(f"  Metadata: {log.metadata}")
```

## Recursos de Ayuda

### Documentación
- [USER_GUIDE.md](USER_GUIDE.md) - Guía de usuario
- [SPECIFICATIONS_V2.md](SPECIFICATIONS_V2.md) - Especificaciones técnicas
- [DT_AUTONOMY.md](DT_AUTONOMY.md) - Autonomía del DT

### Comunidad
- GitHub Issues
- Discord/Slack (si existe)
- Documentación online

---

**Última actualización**: Enero 2025
