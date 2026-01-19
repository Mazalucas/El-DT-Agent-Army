# Integración de Sistema de Reglas de Taskmaster en El DT

## Visión General

Este documento explica cómo replicar y adaptar la infraestructura de reglas de [taskmaster](https://github.com/eyaltoledano/claude-task-master) para que **El DT** pueda actuar de forma autónoma, similar a taskmaster pero adaptado para un sistema multi-agente.

## ¿Qué es el Sistema de Reglas de Taskmaster?

El sistema de reglas de taskmaster permite que el agente actúe de forma **autónoma** siguiendo protocolos y reglas predefinidas, sin necesidad de intervención humana constante. Esto incluye:

1. **Reglas de comportamiento**: Cómo debe actuar el agente
2. **Protocolos de acción**: Cuándo y cómo ejecutar tareas
3. **Permisos y límites**: Qué puede y no puede hacer
4. **Estructura de proyecto**: Organización de archivos y directorios
5. **Configuración persistente**: Reglas que se mantienen entre sesiones

## Estructura de Archivos de Taskmaster

### Estructura Base

```
.taskmaster/
├── docs/
│   └── prd.txt                    # Product Requirements Document
├── tasks/
│   ├── pending/
│   ├── in-progress/
│   └── done/
├── templates/
│   └── example_prd.txt
├── rules/
│   ├── cursor.md                  # Reglas específicas para Cursor
│   ├── windsurf.md                # Reglas específicas para Windsurf
│   ├── vscode.md                  # Reglas específicas para VSCode
│   └── common.md                  # Reglas comunes
├── context/
│   └── project_context.json       # Contexto del proyecto
└── config/
    └── taskmaster.json            # Configuración principal
```

### Archivos de Reglas

Taskmaster usa archivos de reglas en formato Markdown que definen:

1. **Comportamiento del agente**: Instrucciones de cómo actuar
2. **Protocolos de trabajo**: Flujos de trabajo específicos
3. **Límites y restricciones**: Qué no debe hacer
4. **Herramientas permitidas**: Qué herramientas puede usar
5. **Formato de salida**: Cómo estructurar outputs

## Estrategia de Integración: Replicar vs Adaptar

### Opción 1: Replicar Exactamente (NO recomendado)

**Ventajas**:
- Compatibilidad total con taskmaster
- Menos trabajo de diseño

**Desventajas**:
- No adaptado a multi-agente
- Nombres genéricos (no "El DT")
- No aprovecha nuestras especificaciones

### Opción 2: Adaptar y Extender (RECOMENDADO)

**Ventajas**:
- Adaptado a nuestro sistema multi-agente
- Nombres y roles específicos
- Extensible para nuestros agentes

**Desventajas**:
- Requiere más trabajo inicial
- Necesita mantenimiento

### Opción 3: Híbrida (MEJOR OPCIÓN)

**Replicar estructura base** + **Adaptar contenido** para multi-agente

## Propuesta: Estructura de Archivos para El DT

### Estructura Base Adaptada

```
.taskmaster/                        # Mantenemos nombre para compatibilidad
├── docs/
│   ├── prd.txt                    # Product Requirements Document
│   └── project_brief.md           # Brief del proyecto
├── tasks/
│   ├── pending/
│   ├── in-progress/
│   ├── done/
│   └── blocked/
├── agents/                         # NUEVO: Gestión de agentes
│   ├── assignments.json           # Asignaciones de tareas a agentes
│   └── status.json                # Estado de cada agente
├── rules/                          # Reglas y protocolos
│   ├── dt_rules.md                # Reglas específicas de El DT
│   ├── agent_protocols.md          # Protocolos de comunicación
│   ├── tool_permissions.json      # Permisos de herramientas por agente
│   ├── mandatory_rules.md          # Reglas obligatorias
│   ├── editor_specific/           # Reglas por editor
│   │   ├── cursor.md
│   │   ├── windsurf.md
│   │   └── vscode.md
│   └── department_specific/        # NUEVO: Reglas por departamento
│       ├── engineering.md
│       ├── marketing.md
│       ├── design.md
│       └── product.md
├── context/
│   ├── project_context.json       # Contexto del proyecto
│   ├── agent_contexts/            # NUEVO: Contextos por agente
│   │   ├── brand_guardian.json
│   │   ├── marketing_strategist.json
│   │   └── ...
│   └── memory/                    # Memoria persistente
│       ├── sessions/
│       └── long_term/
├── config/
│   ├── dt_config.json             # Configuración de El DT
│   ├── agents_config.yaml         # Configuración de agentes
│   ├── mcp_config.json            # Configuración MCP
│   └── rules_config.json           # Configuración de reglas
└── templates/
    ├── example_prd.txt
    ├── task_template.md
    └── agent_brief_template.md
```

## Archivos de Reglas Detallados

### 1. `.taskmaster/rules/dt_rules.md`

**Propósito**: Reglas principales de El DT que permiten acción autónoma.

```markdown
# Reglas de El DT (Director Técnico)

## Autonomía y Autoridad

El DT puede actuar autónomamente en las siguientes situaciones:

### 1. Gestión de Tareas
- ✅ Parsear PRD y generar tareas automáticamente
- ✅ Asignar tareas a agentes sin consultar (si está dentro de protocolo)
- ✅ Priorizar tareas basándose en dependencias y urgencia
- ✅ Marcar tareas como completadas si el agente reporta éxito y pasa validación

### 2. Asignación de Agentes
- ✅ Asignar tareas a agentes especializados automáticamente
- ✅ Reasignar tareas si un agente falla (máximo 2 reintentos)
- ✅ Crear subtareas y asignarlas a diferentes agentes

### 3. Resolución de Conflictos
- ✅ Resolver conflictos menores entre agentes
- ❌ Escalar conflictos mayores a supervisor humano

### 4. Validación
- ✅ Validar outputs de agentes usando Validator agent
- ✅ Aprobar tareas si pasan validación (score > 0.7)
- ❌ Rechazar sin consultar si score < 0.5

## Límites de Autonomía

El DT NO puede:
- ❌ Modificar reglas del sistema sin aprobación
- ❌ Asignar tareas fuera del dominio de un agente
- ❌ Omitir validaciones obligatorias
- ❌ Acceder a datos sensibles sin autorización
- ❌ Ejecutar tareas directamente (solo coordinar)

## Protocolos de Acción

### Protocolo de Tarea Nueva
1. Recibir solicitud de tarea
2. Analizar tipo y complejidad
3. Descomponer si es necesario (máx. 10 subtareas)
4. Asignar a agente(s) apropiado(s)
5. Monitorear progreso
6. Validar resultado
7. Marcar como completada o escalar

### Protocolo de Error
1. Detectar error de agente
2. Evaluar si es recuperable
3. Si es recuperable: reintentar (máx. 2 veces)
4. Si no es recuperable: escalar a supervisor
5. Registrar en logs

## Reglas de Priorización

Prioridad se asigna basándose en:
1. Dependencias (tareas bloqueantes tienen prioridad alta)
2. Urgencia (deadlines cercanos)
3. Valor de negocio (definido en PRD)
4. Recursos disponibles

## Comunicación

- El DT debe reportar estado cada 5 minutos en tareas largas
- Debe notificar inmediatamente errores críticos
- Debe mantener logs de todas las decisiones
```

### 2. `.taskmaster/rules/agent_protocols.md`

**Propósito**: Protocolos de comunicación y colaboración entre agentes.

```markdown
# Protocolos de Agentes

## Comunicación Entre Agentes

### Mensajes Estándar
Todos los mensajes deben seguir el formato definido en PROTOCOL.md

### Flujos de Trabajo

#### Flujo Simple
1. El DT → Agente: task_request
2. Agente → El DT: task_response
3. El DT → Validator: validation_request
4. Validator → El DT: validation_response
5. El DT: Aprobar o rechazar

#### Flujo Multi-Agente
1. El DT → Agente A: task_request (parte 1)
2. El DT → Agente B: task_request (parte 2, en paralelo)
3. Agente A → El DT: task_response
4. Agente B → El DT: task_response
5. El DT: Sintetizar resultados
6. El DT → Validator: validation_request
7. Validator → El DT: validation_response

## Reglas de Colaboración

- Los agentes NO pueden comunicarse directamente entre sí
- Toda comunicación pasa por El DT
- Los agentes pueden solicitar ayuda a otros agentes vía El DT
- El DT decide si permite la colaboración

## Límites de Agentes

Cada agente tiene límites definidos en su configuración:
- Tiempo máximo de ejecución
- Número máximo de herramientas por tarea
- Límites de tokens
- Acceso restringido a ciertas herramientas
```

### 3. `.taskmaster/config/tool_permissions.json`

**Propósito**: Define qué herramientas puede usar cada agente.

```json
{
  "tool_permissions": {
    "dt": {
      "allowed_tools": ["*"],
      "restricted_tools": [],
      "mcp_servers": ["*"]
    },
    "marketing_strategist": {
      "allowed_tools": [
        "market_analyzer",
        "competitor_analyzer",
        "strategy_framework",
        "kpi_tracker"
      ],
      "restricted_tools": [
        "code_generator",
        "infrastructure_tool"
      ],
      "mcp_servers": [
        "marketing_platforms"
      ]
    },
    "brand_guardian": {
      "allowed_tools": [
        "brand_guidelines_manager",
        "visual_consistency_checker",
        "voice_analyzer",
        "asset_library"
      ],
      "mcp_servers": [
        "brand_assets"
      ]
    },
    "content_creator": {
      "allowed_tools": [
        "content_generator",
        "seo_optimizer",
        "calendar_manager"
      ],
      "mcp_servers": [
        "brand_assets"
      ]
    }
  },
  "default_permissions": {
    "max_tools_per_task": 5,
    "require_approval_for": [
      "code_execution",
      "database_modification",
      "external_api_calls"
    ]
  }
}
```

### 4. `.taskmaster/rules/mandatory_rules.md`

**Propósito**: Reglas que NUNCA pueden ser violadas.

```markdown
# Reglas Obligatorias

Estas reglas son ABSOLUTAS y no pueden ser violadas por ningún agente.

## Seguridad
1. ❌ NUNCA exponer API keys o credenciales en outputs
2. ❌ NUNCA ejecutar código sin validación
3. ❌ NUNCA modificar archivos fuera del proyecto sin autorización
4. ❌ NUNCA acceder a datos sensibles sin permiso explícito

## Calidad
1. ✅ SIEMPRE validar outputs antes de marcar tareas como completadas
2. ✅ SIEMPRE seguir brand guidelines en contenido de marketing
3. ✅ SIEMPRE citar fuentes en investigación
4. ✅ SIEMPRE mantener coherencia con el PRD

## Ética
1. ❌ NUNCA generar contenido ofensivo o discriminatorio
2. ❌ NUNCA violar privacidad de usuarios
3. ❌ NUNCA crear contenido engañoso

## Protocolo
1. ✅ SIEMPRE reportar errores a El DT
2. ✅ SIEMPRE seguir el protocolo de comunicación
3. ✅ SIEMPRE respetar límites de tiempo y recursos
```

### 5. `.taskmaster/config/dt_config.json`

**Propósito**: Configuración principal de El DT.

```json
{
  "dt": {
    "name": "El DT",
    "version": "1.0.0",
    "autonomy_level": "high",
    "max_concurrent_tasks": 10,
    "task_timeout": 300,
    "max_retries": 2,
    "auto_approve_threshold": 0.8,
    "escalation_threshold": 0.5,
    "rules": {
      "enforce_mandatory": true,
      "validate_all_outputs": true,
      "require_human_approval_for": [
        "major_brand_changes",
        "large_budget_decisions",
        "legal_compliance_issues"
      ]
    },
    "mcp": {
      "enabled": true,
      "servers": [
        "brand_assets",
        "marketing_platforms",
        "project_tools"
      ]
    },
    "agents": {
      "auto_assign": true,
      "reassign_on_failure": true,
      "load_balancing": true
    }
  }
}
```

## Implementación en El DT

### Carga de Reglas

```python
class DT(Agent):
    def __init__(self, ...):
        # Cargar reglas al inicializar
        self.rules = RulesLoader.load_all()
        self.mandatory_rules = RulesLoader.load_mandatory()
        self.tool_permissions = ToolPermissions.load()
        self.config = DTConfig.load()
    
    async def can_act_autonomously(
        self,
        action: str,
        context: dict
    ) -> bool:
        """
        Determina si El DT puede actuar autónomamente.
        
        Args:
            action: Tipo de acción a realizar
            context: Contexto de la acción
        
        Returns:
            True si puede actuar autónomamente, False si requiere aprobación
        """
        # Verificar reglas obligatorias
        if not self.mandatory_rules.allows(action, context):
            return False
        
        # Verificar configuración
        if action in self.config.require_human_approval_for:
            return False
        
        # Verificar umbrales
        if context.get("risk_level", 0) > self.config.escalation_threshold:
            return False
        
        return True
    
    async def validate_agent_output(
        self,
        output: Any,
        agent: Agent
    ) -> ValidationResult:
        """
        Valida output de agente según reglas.
        """
        # Cargar reglas específicas del agente
        agent_rules = self.rules.get_agent_rules(agent.role)
        
        # Validar contra reglas obligatorias
        mandatory_check = self.mandatory_rules.validate(output)
        if not mandatory_check.passed:
            return ValidationResult(
                valid=False,
                reason="Violates mandatory rules",
                details=mandatory_check.issues
            )
        
        # Validar contra reglas específicas del agente
        agent_check = agent_rules.validate(output)
        
        return ValidationResult(
            valid=agent_check.passed,
            score=agent_check.score,
            issues=agent_check.issues
        )
```

### Sistema de Carga de Reglas

```python
class RulesLoader:
    @staticmethod
    def load_all() -> Rules:
        """
        Carga todas las reglas desde .taskmaster/rules/
        """
        rules = Rules()
        
        # Cargar reglas principales
        rules.dt_rules = load_markdown(".taskmaster/rules/dt_rules.md")
        rules.agent_protocols = load_markdown(".taskmaster/rules/agent_protocols.md")
        rules.mandatory = load_markdown(".taskmaster/rules/mandatory_rules.md")
        
        # Cargar reglas por departamento
        for dept_file in glob(".taskmaster/rules/department_specific/*.md"):
            dept = extract_department(dept_file)
            rules.departments[dept] = load_markdown(dept_file)
        
        # Cargar reglas por editor
        for editor_file in glob(".taskmaster/rules/editor_specific/*.md"):
            editor = extract_editor(editor_file)
            rules.editors[editor] = load_markdown(editor_file)
        
        return rules
    
    @staticmethod
    def load_mandatory() -> MandatoryRules:
        """
        Carga solo reglas obligatorias.
        """
        return MandatoryRules.from_markdown(
            ".taskmaster/rules/mandatory_rules.md"
        )
```

## Comparación: Taskmaster vs El DT

| Aspecto | Taskmaster | El DT |
|---------|------------|-------|
| **Estructura base** | `.taskmaster/` | `.taskmaster/` (mismo) |
| **Reglas** | Archivos Markdown | Archivos Markdown (adaptados) |
| **Configuración** | `config.json` | `dt_config.json` + `agents_config.yaml` |
| **Tareas** | Gestión simple | Gestión + asignación a agentes |
| **Autonomía** | Alta (un agente) | Alta pero coordinada (multi-agente) |
| **Permisos** | Básicos | Por agente (tool_permissions.json) |
| **MCP** | Integrado | Extendido para multi-agente |

## Archivos a Crear vs Modificar

### Archivos Nuevos (Específicos de El DT)

1. ✅ `.taskmaster/rules/dt_rules.md` - Reglas de El DT
2. ✅ `.taskmaster/rules/agent_protocols.md` - Protocolos multi-agente
3. ✅ `.taskmaster/config/tool_permissions.json` - Permisos por agente
4. ✅ `.taskmaster/config/dt_config.json` - Config de El DT
5. ✅ `.taskmaster/agents/` - Directorio de gestión de agentes
6. ✅ `.taskmaster/rules/department_specific/` - Reglas por departamento

### Archivos Adaptados (Basados en Taskmaster)

1. 🔄 `.taskmaster/rules/common.md` - Adaptado para multi-agente
2. 🔄 `.taskmaster/config/taskmaster.json` - Extendido con config de agentes
3. 🔄 `.taskmaster/templates/` - Templates adaptados

### Archivos Replicados (Igual que Taskmaster)

1. ✅ `.taskmaster/docs/prd.txt` - Mismo formato
2. ✅ `.taskmaster/tasks/` - Misma estructura
3. ✅ `.taskmaster/rules/editor_specific/` - Mismo formato

## Flujo de Carga de Reglas

```
Inicialización de El DT
    │
    ├─→ Cargar dt_config.json
    │
    ├─→ Cargar rules/dt_rules.md
    │
    ├─→ Cargar rules/mandatory_rules.md
    │
    ├─→ Cargar config/tool_permissions.json
    │
    ├─→ Cargar rules/agent_protocols.md
    │
    ├─→ Cargar rules/department_specific/*.md
    │
    └─→ Validar coherencia de reglas
```

## Validación de Reglas

El DT debe validar que:
1. ✅ Todas las reglas obligatorias están presentes
2. ✅ No hay conflictos entre reglas
3. ✅ Los permisos de herramientas son coherentes
4. ✅ Los protocolos están bien definidos
5. ✅ La configuración es válida

## Próximos Pasos

1. **Crear estructura de directorios** según propuesta
2. **Implementar RulesLoader** para cargar reglas
3. **Implementar sistema de validación** de reglas
4. **Crear templates** de reglas para cada departamento
5. **Integrar con El DT** para acción autónoma

---

**Última actualización**: Enero 2025  
**Estado**: Propuesta de Diseño
