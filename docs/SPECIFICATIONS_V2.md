# Especificaciones Técnicas Detalladas: Agents_Army v2.0

## Visión General

Este documento define **específicamente** qué vamos a construir: cuántos agentes, cuáles, qué funcionalidad exacta, qué profundidad de implementación, y todas las definiciones técnicas necesarias.

**Cambios principales respecto a v1.0**:
- ✅ Coordinator renombrado a **"El DT"** (Director Técnico)
- ✅ El DT basado en [claude-task-master](https://github.com/eyaltoledano/claude-task-master)
- ✅ Expandido de 5 a **12-15 agentes** organizados por departamentos
- ✅ Inspirado en [contains-studio/agents](https://github.com/contains-studio/agents)

---

## Alcance del MVP (Versión 1.0)

### Agentes a Implementar

**Total: 1 DT + 16 agentes especializados + 1 sistema de memoria = 18 componentes**

#### El DT (Director Técnico)
1. **El DT** (1 agente coordinador, basado en taskmaster)

#### Agentes por Departamento

**Engineering (3 agentes)**:
2. **Backend Architect**
3. **DevOps Automator**
4. **Frontend Developer**

**Product (2 agentes)**:
5. **Product Strategist**
6. **Feedback Synthesizer**

**Design (2 agentes)**:
7. **UX Researcher**
8. **UI Designer**

**Marketing (6 agentes)**:
9. **Marketing Strategist** (Estrategia de Marketing)
10. **Brand Guardian** (Cuidado de Marca)
11. **Content Creator** (Creación de Contenido)
12. **Storytelling Specialist** (Especialista en Storytelling)
13. **Pitch Specialist** (Especialista en Pitches)
14. **Growth Hacker** (Crecimiento y Adquisición)

**Testing (1 agente)**:
15. **QA Tester**

**Operations (1 agente)**:
16. **Operations Maintainer**

**Research (1 agente)**:
17. **Researcher** (agente genérico de investigación)

#### Infraestructura
18. **MemorySystem** (sistema de memoria)
19. **Tool Registry** (infraestructura)
20. **MCP Server** (Model Context Protocol - integración con herramientas externas)

**NO incluidos en MVP (para v2.0)**:
- AI Engineer
- Mobile App Builder
- Legal Compliance Checker
- Support Responder
- Otros especialistas avanzados

---

## 1. El DT (Director Técnico)

### Especificación Técnica

**Clase**: `DT(Agent)` (basado en taskmaster architecture)

**Inspiración**: [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

**Responsabilidades Específicas**:
1. **Gestión de Tareas** (core de taskmaster):
   - Parsear PRD (Product Requirements Document)
   - Generar tareas desde PRD
   - Gestionar backlog de tareas
   - Priorizar tareas según urgencia y dependencias
   - Asignar tareas a agentes especializados
   
2. **Coordinación de Agentes**:
   - Seleccionar agentes adecuados para cada tarea
   - Supervisar progreso de agentes
   - Resolver conflictos entre agentes
   - Revisar y aprobar entregables clave
   
3. **Gestión de Proyecto**:
   - Mantener visión estratégica del proyecto
   - Asegurar coherencia entre entregables
   - Monitorear métricas globales (velocidad, calidad)
   - Gestionar dependencias entre tareas
   
4. **Comunicación**:
   - Reportar estado del proyecto
   - Escalar problemas cuando sea necesario
   - Proporcionar feedback a agentes

**Métodos Públicos** (basados en taskmaster):

```python
class DT(Agent):
    def __init__(
        self,
        name: str = "El DT",
        instructions: str = None,  # Usa instrucciones por defecto de taskmaster
        model: str = "gpt-4",
        project_path: str = ".dt",
        prd_path: str = ".dt/docs/prd.txt"
    ) -> None
    
    async def initialize_project(
        self,
        project_name: str,
        description: str,
        rules: List[str] = None
    ) -> Project:
        """
        Inicializa un nuevo proyecto (equivalente a task-master init).
        
        Crea estructura:
        - .dt/
          - docs/prd.txt
          - tasks/
          - templates/
        
        Returns:
            Project con configuración inicial
        """
    
    async def parse_prd(
        self,
        prd_path: str = None
    ) -> List[Task]:
        """
        Parsea un PRD y genera tareas (equivalente a task-master parse-prd).
        
        Returns:
            Lista de Task generadas desde el PRD
        """
    
    async def get_tasks(
        self,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 10
    ) -> List[Task]:
        """
        Obtiene lista de tareas (equivalente a task-master list).
        
        Args:
            status: "pending" | "in-progress" | "done" | "blocked"
            tag: Filtrar por tag
            limit: Máximo de tareas a retornar
        """
    
    async def get_next_task(
        self
    ) -> Optional[Task]:
        """
        Obtiene la siguiente tarea a trabajar (equivalente a task-master next).
        
        Retorna la tarea con mayor prioridad que esté lista para ejecutar.
        """
    
    async def assign_task(
        self,
        task: Task,
        agent: Agent
    ) -> TaskAssignment:
        """
        Asigna una tarea a un agente especializado.
        
        El DT decide qué agente es el más adecuado basándose en:
        - Tipo de tarea
        - Especialización del agente
        - Carga de trabajo actual
        - Dependencias
        """
    
    async def decompose_task(
        self,
        task: Task
    ) -> List[SubTask]:
        """
        Divide una tarea compleja en subtareas.
        
        Similar a taskmaster pero adaptado para asignar a agentes.
        """
    
    async def update_task_status(
        self,
        task_id: str,
        status: str,
        agent_result: Optional[TaskResult] = None
    ) -> Task:
        """
        Actualiza el estado de una tarea (equivalente a task-master set-status).
        """
    
    async def expand_task(
        self,
        task_id: str
    ) -> Task:
        """
        Expande una tarea con más detalles (equivalente a task-master expand).
        """
    
    async def research(
        self,
        query: str,
        context: Optional[str] = None
    ) -> ResearchResult:
        """
        Realiza investigación (equivalente a task-master research).
        
        Puede delegar al Researcher agent o usar herramientas directamente.
        """
    
    async def synthesize_results(
        self,
        task_results: List[TaskResult]
    ) -> TaskResult:
        """
        Sintetiza resultados de múltiples agentes para una tarea compleja.
        """
    
    async def resolve_conflict(
        self,
        conflict: AgentConflict
    ) -> ConflictResolution:
        """
        Resuelve conflictos entre agentes (opiniones contradictorias, etc.).
        """
```

**Estructura de Datos (basada en taskmaster)**:

```python
@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str  # "pending" | "in-progress" | "done" | "blocked"
    priority: int  # 1-5
    tags: List[str]
    dependencies: List[str]  # IDs de tareas dependientes
    assigned_agent: Optional[AgentRole] = None
    subtasks: List[SubTask] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Project:
    name: str
    description: str
    path: str  # .dt
    prd_path: str
    rules: List[str]
    created_at: datetime
```

**Configuración**:

```yaml
dt:
  name: "El DT"
  model: "gpt-4"
  instructions: |
    You are El DT (Director Técnico), the technical director of this project.
    Your role is inspired by taskmaster but adapted for multi-agent coordination.
    
    Your responsibilities:
    1. Parse PRDs and generate tasks
    2. Manage task backlog and priorities
    3. Assign tasks to specialized agents
    4. Coordinate agent collaboration
    5. Resolve conflicts between agents
    6. Ensure project coherence and quality
    
    Rules:
    - Always prioritize tasks based on dependencies and urgency
    - Assign tasks to the most appropriate agent
    - Review agent outputs before marking tasks as done
    - Escalate conflicts that cannot be resolved automatically
    - Maintain project vision and strategic alignment
  project_path: ".dt"
  prd_path: ".dt/docs/prd.txt"
  max_concurrent_tasks: 10
  task_timeout: 300  # 5 minutos
```

**Soporte MCP (Model Context Protocol)**:

El DT actúa como servidor MCP, permitiendo integración con herramientas externas y otros sistemas, similar a taskmaster.

```python
class DT(Agent):
    def __init__(
        self,
        # ... parámetros anteriores ...
        mcp_enabled: bool = True,
        mcp_servers: List[MCPServer] = None
    ) -> None
    
    async def setup_mcp_server(
        self,
        server_config: MCPServerConfig
    ) -> MCPServer:
        """
        Configura un servidor MCP para El DT.
        
        Permite integrar:
        - Herramientas externas (APIs, bases de datos)
        - Servidores MCP existentes (Slack, Jira, etc.)
        - Recursos compartidos entre agentes
        
        Returns:
            MCPServer configurado
        """
    
    async def register_mcp_tool(
        self,
        tool: MCPTool,
        accessible_by: List[AgentRole] = None
    ) -> None:
        """
        Registra una herramienta MCP para uso de agentes.
        
        Args:
            tool: Herramienta MCP a registrar
            accessible_by: Lista de roles que pueden usar esta herramienta
                          (None = todos los agentes)
        """
    
    async def get_mcp_tools(
        self,
        agent_role: AgentRole
    ) -> List[MCPTool]:
        """
        Obtiene herramientas MCP disponibles para un agente.
        """
```

**Configuración MCP**:

```yaml
dt:
  # ... configuración anterior ...
  mcp:
    enabled: true
    servers:
      - name: "brand_assets"
        type: "filesystem"
        path: ".dt/brand_assets"
        accessible_by: ["brand_guardian", "content_creator", "storytelling_specialist"]
      - name: "marketing_platforms"
        type: "api"
        endpoints:
          - google_ads
          - facebook_ads
          - analytics
        accessible_by: ["marketing_strategist", "growth_hacker"]
      - name: "project_tools"
        type: "mcp_server"
        command: "npx"
        args: ["-y", "task-master-ai"]
        accessible_by: ["dt"]  # Solo El DT puede usar taskmaster directamente
```

**Sistema de Reglas y Autonomía**:

El DT implementa el sistema de reglas de taskmaster adaptado para multi-agente, permitiendo acción autónoma.

```python
class DT(Agent):
    def __init__(self, ...):
        # Cargar sistema de reglas
        self.rules = RulesLoader.load_all()
        self.mandatory_rules = RulesLoader.load_mandatory()
        self.tool_permissions = ToolPermissions.load()
    
    async def can_act_autonomously(
        self,
        action: str,
        context: dict
    ) -> bool:
        """
        Determina si puede actuar autónomamente según reglas.
        """
        # Verificar reglas obligatorias
        if not self.mandatory_rules.allows(action, context):
            return False
        
        # Verificar umbrales de configuración
        if context.get("risk_level", 0) > self.config.escalation_threshold:
            return False
        
        return True
```

**Estructura de Reglas** (basada en taskmaster):

```
.dt/
├── rules/
│   ├── dt_rules.md              # Reglas de El DT (autonomía)
│   ├── agent_protocols.md       # Protocolos multi-agente
│   ├── mandatory_rules.md       # Reglas obligatorias
│   ├── department_specific/     # Reglas por departamento
│   └── editor_specific/         # Reglas por editor
├── config/
│   ├── dt_config.json           # Config de El DT
│   ├── tool_permissions.json    # Permisos por agente
│   └── agents_config.yaml       # Config de agentes
└── agents/
    ├── assignments.json         # Asignaciones
    └── status.json              # Estado de agentes
```

**Profundidad de Implementación**:
- ✅ Funcionalidad core de taskmaster (init, parse-prd, list, next, expand)
- ✅ Gestión de tareas con estados y dependencias
- ✅ Asignación de tareas a agentes
- ✅ Resolución de conflictos básica
- ✅ Síntesis de resultados
- ✅ **Sistema de reglas completo** (carga, validación, aplicación)
- ✅ **Acción autónoma** basada en reglas
- ✅ **Soporte MCP básico** (registro de herramientas, acceso controlado)
- ✅ **Integración con servidores MCP externos**
- ❌ Interfaz CLI completa (para v2.0)
- ❌ Dashboard visual (para v2.0)
- ❌ MCP avanzado (streaming, subscriptions) (para v2.0)

**Ver [TASKMASTER_RULES_INTEGRATION.md](TASKMASTER_RULES_INTEGRATION.md) para detalles completos del sistema de reglas.**

**Ver [CREWAI_LEARNINGS.md](CREWAI_LEARNINGS.md) para lecciones y adaptaciones de CrewAI.**

---

## 2. Backend Architect

### Especificación Técnica

**Clase**: `BackendArchitect(Specialist)`

**Departamento**: Engineering

**Responsabilidades Específicas**:
1. Diseñar arquitectura server-side
2. Diseñar APIs REST/GraphQL
3. Planificar escalabilidad y performance
4. Definir estructura de base de datos
5. Proporcionar especificaciones técnicas

**Métodos Públicos**:

```python
class BackendArchitect(Specialist):
    async def design_architecture(
        self,
        requirements: dict
    ) -> ArchitectureDesign:
        """
        Diseña la arquitectura backend.
        
        Returns:
            ArchitectureDesign con:
                - components: List[Component]
                - api_endpoints: List[Endpoint]
                - database_schema: DatabaseSchema
                - scalability_plan: ScalabilityPlan
        """
    
    async def design_api(
        self,
        requirements: dict
    ) -> APIDesign:
        """
        Diseña especificación de API.
        """
```

**Herramientas**:
- `code_analyzer`: Análisis de código existente
- `api_designer`: Generación de especificaciones API
- `database_designer`: Diseño de esquemas

**Configuración**:

```yaml
backend_architect:
  name: "Backend Architect"
  department: "engineering"
  model: "gpt-4"
  instructions: |
    You are a Backend Architect specializing in server-side architecture.
    You design scalable, maintainable backend systems.
    
    Focus on:
    - API design (REST, GraphQL)
    - Database architecture
    - Scalability and performance
    - Security best practices
  tools:
    - code_analyzer
    - api_designer
    - database_designer
```

---

## 3. DevOps Automator

### Especificación Técnica

**Clase**: `DevOpsAutomator(Specialist)`

**Departamento**: Engineering

**Responsabilidades Específicas**:
1. Automatizar despliegues (CI/CD)
2. Configurar infraestructura como código
3. Optimizar pipelines
4. Gestionar ambientes (dev, staging, prod)

**Métodos Públicos**:

```python
class DevOpsAutomator(Specialist):
    async def create_cicd_pipeline(
        self,
        project_config: dict
    ) -> CICDPipeline:
        """
        Crea pipeline de CI/CD.
        """
    
    async def setup_infrastructure(
        self,
        requirements: dict
    ) -> InfrastructureConfig:
        """
        Configura infraestructura (Docker, Kubernetes, etc.).
        """
```

**Herramientas**:
- `pipeline_generator`: Generación de pipelines
- `infrastructure_tool`: Configuración de infraestructura
- `deployment_automator`: Automatización de despliegues

---

## 4. Frontend Developer

### Especificación Técnica

**Clase**: `FrontendDeveloper(Specialist)`

**Departamento**: Engineering

**Responsabilidades Específicas**:
1. Implementar interfaces de usuario
2. Asegurar accesibilidad
3. Optimizar performance frontend
4. Implementar componentes reutilizables

**Métodos Públicos**:

```python
class FrontendDeveloper(Specialist):
    async def implement_ui(
        self,
        design_spec: UIDesign
    ) -> Implementation:
        """
        Implementa UI según especificación de diseño.
        """
    
    async def ensure_accessibility(
        self,
        code: str
    ) -> AccessibilityReport:
        """
        Verifica y mejora accesibilidad.
        """
```

**Herramientas**:
- `code_generator`: Generación de código frontend
- `accessibility_checker`: Verificación de accesibilidad
- `performance_analyzer`: Análisis de performance

---

## 5. Product Strategist

### Especificación Técnica

**Clase**: `ProductStrategist(Specialist)`

**Departamento**: Product

**Responsabilidades Específicas**:
1. Priorizar features según valor
2. Crear roadmaps
3. Analizar mercado y competencia
4. Definir estrategia de producto

**Métodos Públicos**:

```python
class ProductStrategist(Specialist):
    async def prioritize_features(
        self,
        features: List[Feature],
        context: dict
    ) -> PrioritizedFeatures:
        """
        Prioriza features usando frameworks (RICE, Value vs Effort, etc.).
        """
    
    async def create_roadmap(
        self,
        goals: List[str],
        timeline: dict
    ) -> Roadmap:
        """
        Crea roadmap de producto.
        """
```

**Herramientas**:
- `prioritization_framework`: Frameworks de priorización
- `market_analyzer`: Análisis de mercado
- `roadmap_generator`: Generación de roadmaps

---

## 6. Feedback Synthesizer

### Especificación Técnica

**Clase**: `FeedbackSynthesizer(Specialist)`

**Departamento**: Product

**Responsabilidades Específicas**:
1. Recolectar feedback de múltiples fuentes
2. Analizar y sintetizar feedback
3. Identificar patrones y tendencias
4. Proponer mejoras basadas en feedback

**Métodos Públicos**:

```python
class FeedbackSynthesizer(Specialist):
    async def collect_feedback(
        self,
        sources: List[FeedbackSource]
    ) -> CollectedFeedback:
        """
        Recolecta feedback de múltiples fuentes.
        """
    
    async def synthesize(
        self,
        feedback: CollectedFeedback
    ) -> FeedbackSynthesis:
        """
        Sintetiza feedback en insights accionables.
        """
```

**Herramientas**:
- `feedback_collector`: Recolección de feedback
- `sentiment_analyzer`: Análisis de sentimiento
- `pattern_detector`: Detección de patrones

---

## 7. UX Researcher

### Especificación Técnica

**Clase**: `UXResearcher(Specialist)`

**Departamento**: Design

**Responsabilidades Específicas**:
1. Realizar investigación de usuarios
2. Crear user personas
3. Analizar user journeys
4. Proponer mejoras de UX

**Métodos Públicos**:

```python
class UXResearcher(Specialist):
    async def research_users(
        self,
        research_questions: List[str]
    ) -> UserResearch:
        """
        Realiza investigación de usuarios.
        """
    
    async def create_personas(
        self,
        user_data: dict
    ) -> List[Persona]:
        """
        Crea user personas.
        """
```

**Herramientas**:
- `user_research_tool`: Herramientas de investigación
- `persona_generator`: Generación de personas
- `journey_mapper`: Mapeo de user journeys

---

## 8. UI Designer

### Especificación Técnica

**Clase**: `UIDesigner(Specialist)`

**Departamento**: Design

**Responsabilidades Específicas**:
1. Crear diseños de interfaz
2. Generar especificaciones de diseño
3. Asegurar consistencia visual
4. Crear componentes de diseño

**Métodos Públicos**:

```python
class UIDesigner(Specialist):
    async def create_design(
        self,
        requirements: DesignRequirements
    ) -> UIDesign:
        """
        Crea diseño de interfaz.
        """
    
    async def generate_specs(
        self,
        design: UIDesign
    ) -> DesignSpecs:
        """
        Genera especificaciones técnicas de diseño.
        """
```

**Herramientas**:
- `design_generator`: Generación de diseños
- `spec_generator`: Generación de especificaciones
- `consistency_checker`: Verificación de consistencia

---

## 9. Marketing Strategist

### Especificación Técnica

**Clase**: `MarketingStrategist(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Definir estrategias de marketing a largo plazo
2. Analizar mercado y competencia
3. Identificar oportunidades de mercado
4. Crear planes de marketing integrados
5. Coordinar campañas multi-canal
6. Definir KPIs y métricas de éxito

**Métodos Públicos**:

```python
class MarketingStrategist(Specialist):
    async def create_marketing_strategy(
        self,
        business_goals: List[str],
        target_audience: dict,
        budget: dict
    ) -> MarketingStrategy:
        """
        Crea estrategia de marketing completa.
        
        Returns:
            MarketingStrategy con:
                - objectives: List[str]
                - target_segments: List[Segment]
                - channels: List[Channel]
                - campaigns: List[Campaign]
                - kpis: List[KPI]
                - timeline: Timeline
        """
    
    async def analyze_competition(
        self,
        competitors: List[str]
    ) -> CompetitiveAnalysis:
        """
        Analiza competencia y posicionamiento.
        """
    
    async def identify_opportunities(
        self,
        market_data: dict
    ) -> List[Opportunity]:
        """
        Identifica oportunidades de mercado.
        """
    
    async def create_campaign_plan(
        self,
        campaign_objective: str,
        budget: float,
        timeline: dict
    ) -> CampaignPlan:
        """
        Crea plan detallado de campaña.
        """
```

**Herramientas**:
- `market_analyzer`: Análisis de mercado
- `competitor_analyzer`: Análisis de competencia
- `strategy_framework`: Frameworks de estrategia (SWOT, 4Ps, etc.)
- `kpi_tracker`: Seguimiento de KPIs
- `campaign_planner`: Planificación de campañas

**Configuración**:

```yaml
marketing_strategist:
  name: "Marketing Strategist"
  department: "marketing"
  model: "gpt-4"
  instructions: |
    You are a Marketing Strategist specializing in long-term marketing strategy.
    You create comprehensive marketing plans, analyze markets, and identify opportunities.
    
    Focus on:
    - Strategic thinking and planning
    - Market analysis and competitive intelligence
    - Multi-channel campaign coordination
    - KPI definition and measurement
    - Alignment with business objectives
  tools:
    - market_analyzer
    - competitor_analyzer
    - strategy_framework
    - kpi_tracker
    - campaign_planner
```

---

## 10. Brand Guardian

### Especificación Técnica

**Clase**: `BrandGuardian(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Proteger y mantener identidad de marca
2. Asegurar coherencia visual y verbal
3. Revisar todos los contenidos para cumplimiento de marca
4. Gestionar brand guidelines
5. Detectar y corregir inconsistencias de marca
6. Mantener biblioteca de assets de marca

**Métodos Públicos**:

```python
class BrandGuardian(Specialist):
    async def review_brand_compliance(
        self,
        content: Any,
        content_type: str  # "text" | "visual" | "audio" | "video"
    ) -> BrandComplianceReport:
        """
        Revisa contenido para cumplimiento de marca.
        
        Returns:
            BrandComplianceReport con:
                - compliant: bool
                - issues: List[BrandIssue]
                - suggestions: List[str]
                - score: float (0-1)
        """
    
    async def check_visual_consistency(
        self,
        design: UIDesign,
        brand_guidelines: BrandGuidelines
    ) -> ConsistencyReport:
        """
        Verifica consistencia visual con brand guidelines.
        """
    
    async def check_verbal_consistency(
        self,
        text: str,
        brand_voice: BrandVoice
    ) -> VoiceComplianceReport:
        """
        Verifica consistencia de tono y voz de marca.
        """
    
    async def update_brand_guidelines(
        self,
        updates: dict
    ) -> BrandGuidelines:
        """
        Actualiza brand guidelines (requiere aprobación de El DT).
        """
    
    async def get_brand_assets(
        self,
        asset_type: str
    ) -> List[BrandAsset]:
        """
        Obtiene assets de marca disponibles.
        """
```

**Herramientas**:
- `brand_guidelines_manager`: Gestión de brand guidelines
- `visual_consistency_checker`: Verificación visual
- `voice_analyzer`: Análisis de tono y voz
- `asset_library`: Biblioteca de assets
- `compliance_scanner`: Escaneo de cumplimiento

**Configuración**:

```yaml
brand_guardian:
  name: "Brand Guardian"
  department: "marketing"
  model: "gpt-4"
  instructions: |
    You are a Brand Guardian responsible for protecting and maintaining brand identity.
    You ensure all content is consistent with brand guidelines.
    
    Your responsibilities:
    - Review all content for brand compliance
    - Maintain brand guidelines and voice
    - Detect and correct brand inconsistencies
    - Manage brand asset library
    
    Rules:
    - Be strict but constructive
    - Always reference brand guidelines
    - Provide actionable feedback
    - Escalate major brand violations to El DT
  tools:
    - brand_guidelines_manager
    - visual_consistency_checker
    - voice_analyzer
    - asset_library
    - compliance_scanner
  access_mcp: ["brand_assets"]  # Acceso a MCP de brand assets
```

---

## 11. Content Creator

### Especificación Técnica

**Clase**: `ContentCreator(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Crear contenido para múltiples canales (blog, social, email, etc.)
2. Adaptar contenido a diferentes audiencias
3. Optimizar contenido para SEO
4. Gestionar calendario de contenido
5. Crear contenido alineado con brand guidelines
6. Colaborar con Brand Guardian para revisión

**Métodos Públicos**:

```python
class ContentCreator(Specialist):
    async def create_content(
        self,
        brief: ContentBrief
    ) -> Content:
        """
        Crea contenido según brief.
        
        ContentBrief incluye:
            - channel: str (blog, social, email, etc.)
            - audience: str
            - topic: str
            - tone: str
            - length: str
            - brand_guidelines: dict
        
        Returns Content con:
            - content: str
            - metadata: dict
            - seo_optimized: bool
        """
    
    async def optimize_seo(
        self,
        content: str,
        keywords: List[str]
    ) -> SEOOptimizedContent:
        """
        Optimiza contenido para SEO.
        """
    
    async def adapt_content(
        self,
        content: str,
        target_channel: str,
        target_audience: str
    ) -> Content:
        """
        Adapta contenido para diferentes canales/audiencias.
        """
    
    async def create_content_calendar(
        self,
        timeframe: dict,
        themes: List[str]
    ) -> ContentCalendar:
        """
        Crea calendario de contenido.
        """
```

**Herramientas**:
- `content_generator`: Generación de contenido
- `seo_optimizer`: Optimización SEO
- `calendar_manager`: Gestión de calendario
- `channel_adapter`: Adaptación por canal
- `brand_assets`: Acceso a assets de marca (vía MCP)

**Configuración**:

```yaml
content_creator:
  name: "Content Creator"
  department: "marketing"
  model: "gpt-4"
  instructions: |
    You are a Content Creator specializing in multi-channel content creation.
    You create engaging, SEO-optimized content aligned with brand guidelines.
    
    Focus on:
    - High-quality, engaging content
    - SEO optimization
    - Brand consistency
    - Audience adaptation
    - Multi-channel expertise
  tools:
    - content_generator
    - seo_optimizer
    - calendar_manager
    - channel_adapter
  access_mcp: ["brand_assets"]
```

---

## 12. Storytelling Specialist

### Especificación Técnica

**Clase**: `StorytellingSpecialist(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Crear narrativas convincentes
2. Desarrollar storylines para productos/campañas
3. Adaptar historias a diferentes formatos
4. Crear conexión emocional con audiencia
5. Colaborar con Brand Guardian para coherencia
6. Desarrollar arcos narrativos

**Métodos Públicos**:

```python
class StorytellingSpecialist(Specialist):
    async def create_story(
        self,
        brief: StoryBrief
    ) -> Story:
        """
        Crea una narrativa completa.
        
        StoryBrief incluye:
            - protagonist: str
            - conflict: str
            - resolution: str
            - target_audience: str
            - format: str (article, video, presentation, etc.)
        
        Returns Story con:
            - narrative: str
            - story_arc: StoryArc
            - emotional_hooks: List[str]
            - call_to_action: str
        """
    
    async def develop_storyline(
        self,
        product: dict,
        audience: dict
    ) -> Storyline:
        """
        Desarrolla storyline para producto/campaña.
        """
    
    async def create_narrative_arc(
        self,
        story_elements: dict
    ) -> NarrativeArc:
        """
        Crea arco narrativo estructurado.
        """
    
    async def adapt_story_format(
        self,
        story: Story,
        target_format: str
    ) -> Story:
        """
        Adapta historia a diferentes formatos.
        """
```

**Herramientas**:
- `story_generator`: Generación de narrativas
- `narrative_framework`: Frameworks narrativos (Hero's Journey, etc.)
- `emotional_analyzer`: Análisis emocional
- `format_adapter`: Adaptación de formatos
- `brand_assets`: Acceso a assets (vía MCP)

**Configuración**:

```yaml
storytelling_specialist:
  name: "Storytelling Specialist"
  department: "marketing"
  model: "gpt-4"
  instructions: |
    You are a Storytelling Specialist who creates compelling narratives.
    You develop storylines that connect emotionally with audiences.
    
    Focus on:
    - Compelling narratives and story arcs
    - Emotional connection
    - Brand-aligned storytelling
    - Multi-format adaptation
    - Clear call-to-action integration
  tools:
    - story_generator
    - narrative_framework
    - emotional_analyzer
    - format_adapter
  access_mcp: ["brand_assets"]
```

---

## 13. Pitch Specialist

### Especificación Técnica

**Clase**: `PitchSpecialist(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Crear pitches para inversores/stakeholders
2. Desarrollar presentaciones convincentes
3. Adaptar pitches a diferentes audiencias
4. Crear materiales de apoyo (decks, one-pagers)
5. Practicar y refinar pitches
6. Integrar storytelling en pitches

**Métodos Públicos**:

```python
class PitchSpecialist(Specialist):
    async def create_pitch(
        self,
        brief: PitchBrief
    ) -> Pitch:
        """
        Crea pitch completo.
        
        PitchBrief incluye:
            - audience: str (investors, customers, partners, etc.)
            - objective: str
            - duration: int (minutos)
            - key_points: List[str]
            - product_info: dict
        
        Returns Pitch con:
            - narrative: str
            - slides: List[Slide]
            - talking_points: List[str]
            - qa_prep: List[QAPair]
        """
    
    async def create_presentation(
        self,
        pitch: Pitch,
        style: str
    ) -> Presentation:
        """
        Crea presentación visual del pitch.
        """
    
    async def create_one_pager(
        self,
        pitch: Pitch
    ) -> OnePager:
        """
        Crea one-pager resumido.
        """
    
    async def prepare_qa(
        self,
        pitch: Pitch
    ) -> QAPreparation:
        """
        Prepara respuestas a preguntas comunes.
        """
    
    async def refine_pitch(
        self,
        pitch: Pitch,
        feedback: dict
    ) -> Pitch:
        """
        Refina pitch basado en feedback.
        """
```

**Herramientas**:
- `pitch_generator`: Generación de pitches
- `presentation_builder`: Construcción de presentaciones
- `storytelling_integrator`: Integración de storytelling
- `qa_preparator`: Preparación de Q&A
- `pitch_analyzer`: Análisis de efectividad

**Configuración**:

```yaml
pitch_specialist:
  name: "Pitch Specialist"
  department: "marketing"
  model: "gpt-4"
  instructions: |
    You are a Pitch Specialist who creates compelling pitches for investors and stakeholders.
    You develop presentations that clearly communicate value propositions.
    
    Focus on:
    - Clear value proposition
    - Compelling narratives
    - Audience adaptation
    - Strong presentations
    - Q&A preparation
  tools:
    - pitch_generator
    - presentation_builder
    - storytelling_integrator
    - qa_preparator
    - pitch_analyzer
  access_mcp: ["brand_assets"]
```

---

## 14. Growth Hacker

### Especificación Técnica

**Clase**: `GrowthHacker(Specialist)`

**Departamento**: Marketing

**Responsabilidades Específicas**:
1. Diseñar experimentos de crecimiento
2. Analizar métricas de crecimiento
3. Identificar oportunidades de crecimiento
4. Optimizar funnel de conversión

**Métodos Públicos**:

```python
class GrowthHacker(Specialist):
    async def design_experiment(
        self,
        hypothesis: str
    ) -> Experiment:
        """
        Diseña experimento de crecimiento.
        """
    
    async def analyze_metrics(
        self,
        metrics: dict
    ) -> GrowthAnalysis:
        """
        Analiza métricas de crecimiento.
        """
```

**Herramientas**:
- `experiment_designer`: Diseño de experimentos
- `metrics_analyzer`: Análisis de métricas
- `funnel_optimizer`: Optimización de funnel

---

## 11. QA Tester

### Especificación Técnica

**Clase**: `QATester(Specialist)`

**Departamento**: Testing

**Responsabilidades Específicas**:
1. Crear casos de prueba
2. Ejecutar pruebas automatizadas
3. Reportar bugs
4. Verificar calidad de código

**Métodos Públicos**:

```python
class QATester(Specialist):
    async def create_test_cases(
        self,
        feature: Feature
    ) -> List[TestCase]:
        """
        Crea casos de prueba para una feature.
        """
    
    async def run_tests(
        self,
        test_cases: List[TestCase]
    ) -> TestResults:
        """
        Ejecuta pruebas y reporta resultados.
        """
```

**Herramientas**:
- `test_generator`: Generación de tests
- `test_runner`: Ejecución de tests
- `bug_reporter`: Reporte de bugs

---

## 12. Operations Maintainer

### Especificación Técnica

**Clase**: `OperationsMaintainer(Specialist)`

**Departamento**: Operations

**Responsabilidades Específicas**:
1. Mantener infraestructura
2. Monitorear sistemas
3. Gestionar incidentes
4. Optimizar recursos

**Métodos Públicos**:

```python
class OperationsMaintainer(Specialist):
    async def monitor_systems(
        self
    ) -> SystemStatus:
        """
        Monitorea estado de sistemas.
        """
    
    async def handle_incident(
        self,
        incident: Incident
    ) -> IncidentResolution:
        """
        Maneja incidentes.
        """
```

**Herramientas**:
- `monitoring_tool`: Monitoreo de sistemas
- `incident_manager`: Gestión de incidentes
- `resource_optimizer`: Optimización de recursos

---

## 13. Researcher (Genérico)

### Especificación Técnica

**Clase**: `Researcher(Specialist)`

**Departamento**: Research

**Responsabilidades Específicas**:
1. Buscar información en web
2. Analizar documentos
3. Sintetizar información
4. Proporcionar fuentes

**Métodos Públicos**:

```python
class Researcher(Specialist):
    async def research(
        self,
        query: str,
        context: Optional[str] = None
    ) -> ResearchResult:
        """
        Realiza investigación sobre un tema.
        """
    
    async def analyze_document(
        self,
        document: str
    ) -> DocumentAnalysis:
        """
        Analiza un documento.
        """
```

**Herramientas**:
- `web_search`: Búsqueda web
- `document_parser`: Parser de documentos
- `text_extractor`: Extracción de texto

---

## 14. MemorySystem

### Especificación Técnica

**Mismo que en v1.0** - Ver [SPECIFICATIONS.md](SPECIFICATIONS.md#5-memorysystem-sistema-de-memoria)

---

## 15. Tool Registry

### Especificación Técnica

**Expandido respecto a v1.0** - Ahora incluye herramientas para todos los agentes.

**Herramientas por Departamento**:

**Engineering**:
- code_analyzer
- api_designer
- database_designer
- pipeline_generator
- infrastructure_tool
- code_generator
- performance_analyzer

**Product**:
- prioritization_framework
- market_analyzer
- roadmap_generator
- feedback_collector
- sentiment_analyzer

**Design**:
- user_research_tool
- persona_generator
- design_generator
- spec_generator

**Marketing**:
- content_generator
- seo_optimizer
- experiment_designer
- metrics_analyzer

**Testing**:
- test_generator
- test_runner
- bug_reporter

**Operations**:
- monitoring_tool
- incident_manager
- resource_optimizer

**Research** (compartidas):
- web_search
- document_parser
- text_extractor

---

## Resumen de Agentes

| # | Agente | Departamento | Responsabilidad Principal |
|---|--------|--------------|---------------------------|
| 1 | El DT | Coordinación | Gestión de tareas y coordinación de agentes (con MCP) |
| 2 | Backend Architect | Engineering | Diseño de arquitectura backend |
| 3 | DevOps Automator | Engineering | Automatización CI/CD e infraestructura |
| 4 | Frontend Developer | Engineering | Implementación de UI |
| 5 | Product Strategist | Product | Priorización y estrategia de producto |
| 6 | Feedback Synthesizer | Product | Síntesis de feedback de usuarios |
| 7 | UX Researcher | Design | Investigación de usuarios |
| 8 | UI Designer | Design | Diseño de interfaces |
| 9 | Marketing Strategist | Marketing | Estrategia de marketing a largo plazo |
| 10 | Brand Guardian | Marketing | Protección y cuidado de marca |
| 11 | Content Creator | Marketing | Creación de contenido multi-canal |
| 12 | Storytelling Specialist | Marketing | Creación de narrativas convincentes |
| 13 | Pitch Specialist | Marketing | Creación de pitches y presentaciones |
| 14 | Growth Hacker | Marketing | Experimentación y crecimiento |
| 15 | QA Tester | Testing | Pruebas y aseguramiento de calidad |
| 16 | Operations Maintainer | Operations | Mantenimiento de infraestructura |
| 17 | Researcher | Research | Investigación genérica |

**Total: 17 agentes + 1 MemorySystem + 1 Tool Registry + 1 MCP Server = 20 componentes**

---

## Límites y Restricciones del MVP

### Límites Técnicos

- **Máximo de tareas por proyecto**: 100 (configurable)
- **Máximo de subtareas por tarea**: 10
- **Timeout por tarea**: 10 minutos
- **Máximo de agentes concurrentes**: 5
- **Score mínimo de calidad**: 0.7

### Modelos LLM

- **Modelo por defecto**: GPT-4
- **Modelos soportados**: GPT-4, GPT-3.5-turbo, Claude (configurable)

---

## Criterios de Éxito del MVP

### Funcionalidad

- ✅ El DT puede parsear PRD y generar tareas
- ✅ El DT puede asignar tareas a agentes especializados
- ✅ Todos los agentes pueden ejecutar tareas de su dominio
- ✅ MemorySystem funciona correctamente
- ✅ Tool Registry tiene herramientas para todos los agentes

### Calidad

- ✅ Cobertura de tests: > 80%
- ✅ Documentación: 100% de APIs públicas
- ✅ Type hints: 100% del código

---

**Última actualización**: Enero 2025  
**Versión**: 2.0 (MVP expandido)  
**Estado**: Especificación Final
