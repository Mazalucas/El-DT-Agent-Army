# Agentes Planificadores

Este documento describe los agentes planificadores disponibles en Agents_Army para las etapas iniciales de creación de proyectos.

## Visión General

Los agentes planificadores están diseñados para crear documentación y planes estructurados que sirven como base para el desarrollo de software. Estos agentes trabajan en secuencia para transformar una idea de producto en un plan de desarrollo ejecutable.

## Flujo de Trabajo

```
Idea de Producto
    ↓
PRD Creator → Product Requirements Document
    ↓
SRD Creator → Software Requirements Document
    ↓
Development Planner → Development Plan (fases, stack, MVP, roadmap)
    ↓
DT → Extrae tareas y asigna a agentes especializados
```

## Agentes Disponibles

### 1. PRD Creator

**Rol**: `PRD_CREATOR`  
**Departamento**: Planning  
**Propósito**: Crear Product Requirements Documents (PRDs) completos

#### Capacidades

- Crear PRDs estructurados con todas las secciones necesarias
- Identificar user personas y user stories
- Definir features y acceptance criteria
- Establecer success metrics y KPIs
- Refinar PRDs existentes basado en feedback

#### Métodos Principales

```python
# Crear un PRD
prd = await prd_creator.create_prd(
    product_idea="Descripción de la idea del producto",
    business_objectives=["Objetivo 1", "Objetivo 2"],
    target_users=["Persona 1", "Persona 2"],
    constraints={"budget": "...", "timeline": "..."},
    context={"market": "...", "competition": "..."}
)

# Refinar un PRD existente
updated_prd = await prd_creator.refine_prd(
    prd=prd,
    feedback="Feedback del usuario",
    changes={"section": "nuevo contenido"}
)
```

#### Estructura del PRD

El PRD generado incluye:

1. **Executive Summary**: Visión, objetivos, criterios de éxito
2. **Product Overview**: Problema, solución, propuesta de valor
3. **User Personas & User Stories**: Personas detalladas y user stories
4. **Features & Requirements**: Features core y nice-to-have
5. **Success Metrics & KPIs**: Métricas y KPIs clave
6. **Acceptance Criteria**: Criterios de aceptación por feature
7. **Non-Functional Requirements**: Performance, seguridad, escalabilidad
8. **Out of Scope**: Qué NO está incluido
9. **Dependencies & Risks**: Dependencias y riesgos identificados
10. **Timeline & Milestones**: Timeline de alto nivel y milestones

---

### 2. SRD Creator

**Rol**: `SRD_CREATOR`  
**Departamento**: Planning  
**Propósito**: Crear Software Requirements Documents (SRDs) que traducen PRDs en especificaciones técnicas

#### Capacidades

- Analizar PRDs y extraer requisitos técnicos
- Definir arquitectura del sistema y componentes
- Especificar APIs, modelos de datos e interfaces
- Identificar constraints técnicos y dependencias
- Definir requisitos de integración

#### Métodos Principales

```python
# Crear un SRD desde un PRD
srd = await srd_creator.create_srd(
    prd=prd,
    technical_context={
        "current_stack": "Python, React, PostgreSQL",
        "infrastructure": "Cloud-based"
    },
    existing_systems=["Auth0", "Stripe"],
    technical_constraints={
        "must_use": "React",
        "scalability": "10,000 concurrent users"
    }
)

# Refinar un SRD existente
updated_srd = await srd_creator.refine_srd(
    srd=srd,
    feedback="Feedback técnico",
    changes={"architecture": "nuevo diseño"}
)
```

#### Estructura del SRD

El SRD generado incluye:

1. **System Overview**: Arquitectura de alto nivel, stack tecnológico
2. **Functional Requirements**: Especificaciones funcionales detalladas
3. **System Architecture**: Patrones arquitectónicos, componentes, servicios
4. **Data Models & Database Design**: Modelos de datos, esquemas
5. **API Specifications**: Endpoints REST/GraphQL, schemas
6. **Integration Requirements**: Integraciones con sistemas externos
7. **Non-Functional Requirements**: Performance, seguridad, escalabilidad
8. **Technical Constraints**: Constraints técnicos
9. **Development Phases**: Fases de desarrollo, dependencias
10. **Testing Requirements**: Requisitos de testing
11. **Deployment & DevOps**: Arquitectura de deployment, CI/CD
12. **Risk Assessment**: Riesgos técnicos y mitigaciones

---

### 3. Development Planner

**Rol**: `DEVELOPMENT_PLANNER`  
**Departamento**: Planning  
**Propósito**: Crear planes de desarrollo por fases con stack tecnológico, MVP, roadmap y tiempos

#### Capacidades

- Definir MVP y scope
- Seleccionar stack tecnológico apropiado
- Crear roadmap por fases con dependencias
- Estimar tiempos y recursos
- Identificar critical path y riesgos
- Extraer tareas ejecutables del plan

#### Métodos Principales

```python
# Crear un plan de desarrollo
plan = await planner.create_development_plan(
    prd=prd,
    srd=srd,
    constraints={
        "timeline": "3 months",
        "team_size": "4 people",
        "budget": "$50,000"
    },
    preferences={
        "methodology": "Agile/Scrum",
        "sprints": "2-week sprints"
    }
)

# Refinar un plan existente
updated_plan = await planner.refine_plan(
    plan=plan,
    feedback="Cambios solicitados",
    changes={"timeline": "4 months"}
)

# Extraer tareas del plan
tasks = await planner.extract_tasks_from_plan(
    plan=plan,
    phase="Phase 1"  # Opcional: filtrar por fase
)
```

#### Estructura del Development Plan

El plan generado incluye:

1. **Executive Summary**: Resumen del proyecto
2. **Technology Stack Selection**: Stack recomendado con justificación
3. **MVP Definition**: Scope del MVP, features, timeline
4. **Development Phases**: Fases detalladas con objetivos, features, timeline
5. **Detailed Roadmap**: Timeline visual, critical path, milestones
6. **Scope Definition**: In-scope y out-of-scope por fase
7. **Resource Planning**: Composición del equipo, roles, presupuesto
8. **Risk Assessment & Mitigation**: Riesgos y estrategias de mitigación
9. **Quality Assurance Plan**: Estrategia de testing por fase
10. **Success Metrics**: Criterios de éxito por fase
11. **Post-MVP Roadmap**: Roadmap futuro más allá del MVP

---

## Integración con el DT

El DT (Director Técnico) puede trabajar con los agentes planificadores para:

### 1. Crear Documentos de Planificación

```python
# Crear PRD
prd = await dt.create_prd(
    product_idea="...",
    business_objectives=["..."],
    target_users=["..."]
)

# Crear SRD
srd = await dt.create_srd(
    prd=prd,
    technical_context={...}
)

# Crear Development Plan
plan = await dt.create_development_plan(
    prd=prd,
    srd=srd,
    constraints={...}
)
```

### 2. Extraer Tareas del Plan

```python
# Extraer todas las tareas del plan
tasks = await dt.extract_tasks_from_plan(plan)

# Extraer tareas de una fase específica
phase_tasks = await dt.extract_tasks_from_plan(plan, phase="Phase 1")
```

### 3. Mapear Tareas a Agentes

```python
# Mapear una tarea al agente apropiado
agent_role = await dt.map_task_to_agent(task, plan)

# El DT analiza:
# - Contenido de la tarea
# - Tags y metadata
# - Contexto del plan de desarrollo
# - Skills requeridos
```

### 4. Ejecutar el Plan

```python
# Ejecutar el plan completo (extrae tareas y asigna automáticamente)
assignments = await dt.execute_plan(
    plan=plan,
    phase=None,  # Opcional: ejecutar solo una fase
    auto_assign=True  # Asignar automáticamente a agentes
)

# El DT:
# 1. Extrae tareas del plan
# 2. Mapea cada tarea al agente apropiado
# 3. Asigna las tareas
# 4. Retorna las asignaciones creadas
```

## Ejemplo Completo

Ver `examples/planning_agents_example.py` para un ejemplo completo que muestra:

1. Creación de PRD
2. Creación de SRD basado en PRD
3. Creación de Development Plan
4. Extracción de tareas
5. Asignación automática a agentes
6. Monitoreo del progreso

## Uso en Flujo de Trabajo Real

### Paso 1: Inicializar Sistema y Agentes

```python
from agents_army import AgentSystem, DT, PRDCreator, SRDCreator, DevelopmentPlanner

system = AgentSystem()
dt = DT(project_path=".dt")
prd_creator = PRDCreator()
srd_creator = SRDCreator()
planner = DevelopmentPlanner()

system.register_agent(dt)
system.register_agent(prd_creator)
system.register_agent(srd_creator)
system.register_agent(planner)

dt.system = system  # Necesario para que DT acceda a otros agentes
```

### Paso 2: Crear PRD

```python
prd = await dt.create_prd(
    product_idea="Aplicación de gestión de tareas para equipos pequeños",
    business_objectives=["Aumentar productividad 30%", "Lanzar MVP en 3 meses"],
    target_users=["Team managers", "Project coordinators"],
    constraints={"timeline": "3 months", "budget": "Limited"}
)
```

### Paso 3: Crear SRD

```python
srd = await dt.create_srd(
    prd=prd,
    technical_context={"current_stack": "Python, React, PostgreSQL"},
    existing_systems=["Auth0", "Stripe"],
    technical_constraints={"scalability": "10,000 users"}
)
```

### Paso 4: Crear Development Plan

```python
plan = await dt.create_development_plan(
    prd=prd,
    srd=srd,
    constraints={"timeline": "3 months", "team_size": "4"},
    preferences={"methodology": "Agile"}
)
```

### Paso 5: Ejecutar Plan

```python
# El DT extrae tareas y las asigna automáticamente
assignments = await dt.execute_plan(plan, auto_assign=True)

# Ver tareas asignadas
tasks = await dt.get_tasks(status="in-progress")
for task in tasks:
    print(f"{task.title} -> {task.assigned_agent}")
```

## Mejores Prácticas

1. **Iteración**: Los planes pueden refinarse. Usa `refine_prd()`, `refine_srd()`, `refine_plan()` para mejorar documentos basado en feedback.

2. **Validación**: Revisa los documentos generados antes de ejecutar el plan. Los agentes son guías, no reemplazan la revisión humana.

3. **Especificidad**: Proporciona contexto detallado (constraints, preferences, technical context) para obtener planes más precisos.

4. **Fases Incrementales**: Ejecuta el plan por fases usando el parámetro `phase` en `execute_plan()`.

5. **Monitoreo**: Usa `dt.get_tasks()` para monitorear el progreso de las tareas asignadas.

## Notas Técnicas

- Los agentes planificadores requieren que el DT esté registrado en un `AgentSystem` para funcionar.
- Los documentos generados se almacenan en memoria. Para persistencia, guarda los documentos manualmente.
- El mapeo de tareas a agentes usa heurísticas basadas en contenido. Revisa las asignaciones antes de ejecutar.
- Los planes pueden ser refinados múltiples veces. Cada refinamiento incrementa la versión del documento.
