# Guía de Usuario: Agents_Army

## Visión General

Esta guía está dirigida a usuarios finales que quieren usar **Agents_Army** en sus proyectos. Explica cómo empezar, conceptos básicos, y casos de uso comunes.

## Quick Start

Ver **[QUICK_START.md](QUICK_START.md)** para inicio rápido.

### Dos Caminos para Empezar

#### 1️⃣ Ya Tienes un Proyecto
Integra El DT en tu proyecto existente. Ver [QUICK_START.md](QUICK_START.md#camino-1-ya-tienes-un-proyecto).

#### 2️⃣ Conversar con El DT para Planear
El DT te ayuda a planear y armar tu proyecto desde cero. Ver [QUICK_START.md](QUICK_START.md#camino-2-conversar-con-el-dt-para-planear-y-armar-el-proyecto).

### Instalación

```bash
# Clonar e instalar
git clone https://github.com/Mazalucas/El-DT-Agent-Army.git
cd El-DT-Agent-Army
pip install -e .
```

## Conceptos Básicos

### ¿Qué es El DT?

**El DT** (Director Técnico) es el coordinador principal que:
- Gestiona tareas de tu proyecto
- Asigna trabajo a agentes especializados
- Toma decisiones autónomas
- Coordina la colaboración entre agentes

### ¿Qué son los Agentes?

Los **agentes** son especialistas que ejecutan tareas específicas:
- **Researcher**: Busca información
- **Writer**: Escribe contenido
- **Marketing Strategist**: Crea estrategias de marketing
- Y muchos más...

### ¿Qué es una Tarea?

Una **tarea** es una unidad de trabajo que El DT puede:
- Descomponer en subtareas
- Asignar a agentes
- Supervisar y validar

## Primeros Pasos

### 1. Crear un PRD

Crea un archivo `.dt/docs/prd.txt`:

```markdown
# Product Requirements Document

## Objetivo
Crear una campaña de marketing para nuestro nuevo producto.

## Features Requeridas
1. Estrategia de marketing
2. Contenido para redes sociales
3. Pitch para inversores
4. Material visual

## Restricciones
- Presupuesto: $10,000
- Timeline: 2 semanas
- Audiencia: Tech-savvy millennials
```

### 2. Parsear el PRD

```python
# El DT parsea el PRD y genera tareas
tasks = await dt.parse_prd(".dt/docs/prd.txt")

print(f"Generadas {len(tasks)} tareas")
for task in tasks:
    print(f"- {task.title}")
```

### 3. Ejecutar Tareas

```python
# El DT asigna y ejecuta tareas automáticamente
for task in tasks:
    result = await dt.execute_task(task)
    print(f"Tarea {task.id}: {result.status}")
```

## Casos de Uso Comunes

### Caso 1: Crear Estrategia de Marketing

```python
# 1. Crear tarea
task = Task(
    description="Crear estrategia de marketing para Q1 2025",
    type="marketing_strategy",
    parameters={
        "budget": 50000,
        "target_audience": "B2B SaaS companies",
        "channels": ["linkedin", "content", "events"]
    }
)

# 2. El DT asigna a Marketing Strategist
result = await dt.execute_task(task)

# 3. Obtener resultado
strategy = result.content
print(strategy)
```

### Caso 2: Crear Contenido

```python
# 1. Investigar primero
research_task = Task(
    description="Investigar mejores prácticas de contenido B2B",
    type="research"
)

research_result = await dt.execute_task(research_task)

# 2. Crear contenido basado en investigación
content_task = Task(
    description="Crear artículo de blog sobre mejores prácticas",
    type="content_creation",
    context=research_result.content
)

content_result = await dt.execute_task(content_task)
```

### Caso 3: Crear Pitch

```python
# El DT coordina múltiples agentes
pitch_task = Task(
    description="Crear pitch para inversores",
    type="pitch",
    parameters={
        "audience": "investors",
        "duration": "10 minutes",
        "focus": "product-market-fit"
    }
)

# El DT automáticamente:
# 1. Asigna a Researcher para investigación
# 2. Asigna a Storytelling Specialist para narrativa
# 3. Asigna a Pitch Specialist para estructura
# 4. Valida con Brand Guardian
# 5. Entrega resultado final

pitch_result = await dt.execute_task(pitch_task)
```

## Configuración

### Configurar Agentes

```yaml
# .dt/config/agents_config.yaml
agents:
  marketing_strategist:
    enabled: true
    model: "gpt-4"
    tools:
      - market_analyzer
      - competitor_analyzer
  
  content_creator:
    enabled: true
    model: "gpt-4"
    tools:
      - content_generator
      - seo_optimizer
```

### Configurar El DT

```yaml
# .dt/config/dt_config.json
{
  "dt": {
    "autonomy_level": "high",
    "auto_approve_threshold": 0.8,
    "max_concurrent_tasks": 10
  }
}
```

## Comandos Comunes

### Ver Tareas

```python
# Ver todas las tareas
tasks = await dt.get_tasks()
for task in tasks:
    print(f"{task.id}: {task.title} - {task.status}")

# Ver siguiente tarea
next_task = await dt.get_next_task()
print(f"Próxima: {next_task.title}")

# Ver tareas por estado
pending = await dt.get_tasks(status="pending")
in_progress = await dt.get_tasks(status="in-progress")
```

### Gestionar Tareas

```python
# Actualizar estado
await dt.update_task_status("task_123", "done")

# Expandir tarea
expanded = await dt.expand_task("task_123")

# Asignar tarea (ahora ejecuta automáticamente)
await dt.assign_task(task, agent)
# El sistema automáticamente:
# - Decide nivel de autonomía (1-4)
# - Ejecuta con loop si corresponde (niveles 4/3)
# - Ejecuta simple si corresponde (nivel 2)
# - Escala si corresponde (nivel 1)
# - Actualiza estado de tarea según resultado
```

### Investigar

```python
# Investigación simple
result = await dt.research("Latest trends in AI agents")

# Investigación con contexto
result = await dt.research(
    "Best practices for JWT authentication",
    context="Our current implementation uses..."
)
```

## Ejemplos Prácticos

### Ejemplo 1: Proyecto Completo

```python
# 1. Inicializar
dt = DT()
project = await dt.initialize_project("Nuevo Producto")

# 2. Parsear PRD
tasks = await dt.parse_prd()

# 3. Ejecutar todas las tareas (ahora con ejecución automática)
for task in tasks:
    # assign_task() ahora ejecuta automáticamente según nivel de autonomía
    assignment = await dt.assign_task(task, AgentRole.BACKEND_ARCHITECT)
    # El sistema decide y ejecuta:
    # - Si nivel 4: Loop autónomo completo hasta completitud
    # - Si nivel 3: Loop validado con validación estricta
    # - Si nivel 2: Ejecución simple con validación
    # - Si nivel 1: Escala a humano (tarea queda en "blocked")
    
    # Verificar estado
    updated_task = dt.task_storage.load_task(task.id)
    if updated_task.status == "done":
        print(f"✓ {task.title} completado")
    elif updated_task.status == "blocked":
        print(f"⚠ {task.title} requiere atención humana")

# 4. Obtener resultado final
final_result = await dt.synthesize_results()
```

### Ejemplo 2: Workflow Personalizado

```python
# Crear crew personalizado
crew = await dt.create_crew(
    agents_needed=["researcher", "writer", "validator"]
)

# Ejecutar crew
result = await dt.execute_crew(crew)
```

## Troubleshooting

### Problema: Tareas no se ejecutan

**Solución**:
```python
# Verificar estado de agentes
system = AgentSystem.get_instance()
for agent in system.get_agents():
    print(f"{agent.role}: {agent.status}")

# Verificar logs
logs = await dt.get_logs()
print(logs)
```

### Problema: Costos muy altos

**Solución**:
```python
# Ver costos
costs = await dt.get_daily_costs()
print(f"Costo diario: ${costs.total}")

# Optimizar
suggestions = await dt.optimize_costs()
for suggestion in suggestions:
    print(suggestion)
```

### Problema: El DT no actúa autónomamente

**Solución**:
```python
# Verificar configuración
config = dt.get_config()
print(f"Autonomía: {config.autonomy_level}")

# Verificar umbrales
thresholds = dt.get_thresholds()
print(f"Umbral autónomo: {thresholds.autonomous}")

# Ver decisiones recientes
decisions = await dt.get_recent_decisions()
for decision in decisions:
    print(f"{decision.action}: {decision.confidence}")
```

## Mejores Prácticas

### 1. PRD Detallado

Cuanto más detallado el PRD, mejores las tareas generadas:

```markdown
# ✅ Buen PRD
## Feature: User Authentication
- Método: JWT tokens
- Expiración: 1 hora
- Refresh tokens: Sí
- Integración con: Auth0

# ❌ PRD Vago
## Feature: Login
- Hacer login
```

### 2. Revisar Tareas Generadas

Siempre revisa las tareas antes de ejecutar:

```python
tasks = await dt.parse_prd()
for task in tasks:
    print(f"{task.title}: {task.description}")
    # Ajustar si es necesario
    if task.needs_adjustment:
        task = await dt.expand_task(task.id)
```

### 3. Monitorear Costos

```python
# Configurar alertas
await dt.set_budget_alert(threshold=80)  # 80% del presupuesto

# Revisar regularmente
daily_cost = await dt.get_daily_cost()
if daily_cost > budget * 0.8:
    print("⚠️ Presupuesto alto")
```

## FAQ

### ¿Puedo usar solo algunos agentes?

Sí, puedes deshabilitar agentes en la configuración:

```yaml
agents:
  some_agent:
    enabled: false
```

### ¿Cómo cambio el modelo LLM?

```python
# Por agente
agent = Researcher(model="gpt-3.5-turbo")

# Globalmente
dt = DT(default_model="gpt-3.5-turbo")
```

### ¿El DT puede trabajar sin intervención?

Sí, El DT puede actuar autónomamente según su configuración. Ver [DT_AUTONOMY.md](DT_AUTONOMY.md) para más detalles.

### ¿Cómo veo qué está haciendo El DT?

```python
# Ver decisiones recientes
decisions = await dt.get_recent_decisions()

# Ver logs
logs = await dt.get_logs(level="INFO")

# Ver métricas
metrics = await dt.get_metrics()
```

---

**Última actualización**: Enero 2025  
**Para más información**: Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
