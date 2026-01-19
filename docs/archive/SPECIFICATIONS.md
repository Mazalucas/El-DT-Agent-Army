# Especificaciones Técnicas Detalladas: Agents_Army v1.0 (DEPRECATED)

> ⚠️ **NOTA**: Esta versión está deprecada. Ver **[SPECIFICATIONS_V2.md](SPECIFICATIONS_V2.md)** para la versión actualizada con:
> - El DT (Director Técnico) basado en taskmaster
> - 13 agentes especializados organizados por departamentos
> - Estructura expandida inspirada en contains-studio/agents

## Visión General

Este documento define **específicamente** qué vamos a construir: cuántos agentes, cuáles, qué funcionalidad exacta, qué profundidad de implementación, y todas las definiciones técnicas necesarias.

**⚠️ Esta versión está obsoleta. Por favor, consulta [SPECIFICATIONS_V2.md](SPECIFICATIONS_V2.md)**

## Alcance del MVP (Versión 1.0)

### Agentes a Implementar

**Total: 5 agentes + 1 sistema de memoria**

1. **Coordinator** (1 agente)
2. **Researcher** (1 agente especialista)
3. **Writer** (1 agente especialista)
4. **Validator** (1 agente)
5. **MemorySystem** (1 sistema, no es agente pero actúa como tal)
6. **Tool Registry** (infraestructura, no agente)

**NO incluimos en MVP:**
- Analyst (para v2.0)
- Supervisor humano (interfaz manual, fuera del scope del framework)
- Otros especialistas (extensibles después)

---

## 1. Coordinator (Coordinador)

### Especificación Técnica

**Clase**: `Coordinator(Agent)`

**Responsabilidades Específicas**:
1. Recibir tareas del usuario/sistema
2. Descomponer tareas complejas en máximo 5 subtareas
3. Asignar subtareas a agentes especializados
4. Supervisar progreso (timeout: 5 minutos por subtarea)
5. Sintetizar resultados de múltiples agentes
6. Gestionar reintentos (máximo 2 reintentos por subtarea)

**Métodos Públicos**:

```python
class Coordinator(Agent):
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4",
        max_subtasks: int = 5,
        subtask_timeout: int = 300,  # segundos
        max_retries: int = 2
    ) -> None
    
    async def execute_task(
        self, 
        task: Task
    ) -> TaskResult:
        """
        Ejecuta una tarea completa.
        
        Args:
            task: Task con:
                - id: str
                - description: str
                - type: str
                - parameters: dict
                - expected_output: dict (opcional)
        
        Returns:
            TaskResult con:
                - task_id: str
                - status: "completed" | "failed" | "partial"
                - result: Any
                - subtasks: List[SubTaskResult]
                - metadata: dict
        """
    
    async def decompose_task(
        self, 
        task: Task
    ) -> List[SubTask]:
        """
        Divide una tarea en subtareas.
        
        Returns:
            Lista de SubTask con:
                - id: str
                - parent_task_id: str
                - description: str
                - assigned_agent: AgentRole
                - dependencies: List[str] (ids de subtareas previas)
                - priority: int (1-5)
        """
    
    async def assign_subtask(
        self,
        subtask: SubTask,
        agent: Agent
    ) -> SubTaskResult:
        """
        Asigna una subtarea a un agente.
        """
    
    async def synthesize_results(
        self,
        subtask_results: List[SubTaskResult]
    ) -> TaskResult:
        """
        Combina resultados de múltiples subtareas.
        """
```

**Configuración**:

```yaml
coordinator:
  name: "Main Coordinator"
  model: "gpt-4"
  instructions: |
    You are a task coordinator. Your job is to:
    1. Break down complex tasks into manageable subtasks
    2. Assign subtasks to appropriate specialist agents
    3. Monitor progress and handle errors
    4. Synthesize results from multiple agents
    
    Rules:
    - Maximum 5 subtasks per task
    - Each subtask must have clear dependencies
    - Always validate results before synthesis
  max_subtasks: 5
  subtask_timeout: 300
  max_retries: 2
  tools: []  # Coordinator no usa herramientas directamente
```

**Profundidad de Implementación**:
- ✅ Descomposición básica usando LLM
- ✅ Asignación basada en tipo de tarea
- ✅ Manejo de errores y reintentos
- ✅ Síntesis de resultados
- ❌ Planificación avanzada (para v2.0)
- ❌ Optimización de asignaciones (para v2.0)

---

## 2. Researcher (Investigador)

### Especificación Técnica

**Clase**: `Researcher(Specialist)`

**Responsabilidades Específicas**:
1. Buscar información en web (máximo 5 fuentes)
2. Analizar documentos de texto (máximo 10 páginas)
3. Extraer información relevante
4. Generar resumen estructurado
5. Proporcionar fuentes y referencias

**Métodos Públicos**:

```python
class Researcher(Specialist):
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4",
        max_sources: int = 5,
        max_document_pages: int = 10
    ) -> None
    
    async def execute(
        self,
        task: Task
    ) -> TaskResult:
        """
        Ejecuta tarea de investigación.
        
        Task.parameters debe incluir:
            - query: str (pregunta o tema a investigar)
            - depth: "shallow" | "medium" | "deep" (opcional)
            - sources_required: int (opcional, default 3)
        
        Returns TaskResult con:
            - result.content: str (resumen de investigación)
            - result.sources: List[Source] (fuentes encontradas)
            - result.key_points: List[str] (puntos clave)
            - result.metadata.search_queries: List[str]
            - result.metadata.sources_checked: int
        """
    
    async def search_web(
        self,
        query: str,
        max_results: int = 5
    ) -> List[Source]:
        """
        Busca información en web.
        
        Returns:
            Lista de Source con:
                - url: str
                - title: str
                - snippet: str
                - relevance_score: float (0-1)
        """
    
    async def analyze_document(
        self,
        document: str,
        max_pages: int = 10
    ) -> DocumentAnalysis:
        """
        Analiza un documento de texto.
        
        Returns:
            DocumentAnalysis con:
                - summary: str
                - key_points: List[str]
                - entities: List[str]
                - metadata: dict
        """
```

**Herramientas Disponibles**:
1. `web_search`: Búsqueda web (requiere API key)
2. `document_parser`: Parser de documentos (texto plano, markdown)
3. `text_extractor`: Extracción de texto de documentos

**Configuración**:

```yaml
researcher:
  name: "Research Specialist"
  model: "gpt-4"
  instructions: |
    You are a research specialist. Your job is to:
    1. Search for accurate and relevant information
    2. Analyze documents and extract key information
    3. Provide well-structured summaries with sources
    4. Verify information when possible
    
    Rules:
    - Always cite sources
    - Maximum 5 sources per research task
    - Focus on accuracy over quantity
  max_sources: 5
  max_document_pages: 10
  tools:
    - web_search
    - document_parser
    - text_extractor
  max_tokens: 4000
  timeout: 180
```

**Profundidad de Implementación**:
- ✅ Búsqueda web básica (1 proveedor: SerpAPI o similar)
- ✅ Análisis de texto plano y markdown
- ✅ Extracción de información estructurada
- ✅ Generación de resúmenes
- ❌ Análisis de PDFs complejos (para v2.0)
- ❌ Búsqueda en bases de datos académicas (para v2.0)
- ❌ Verificación de hechos automática (para v2.0)

---

## 3. Writer (Escritor)

### Especificación Técnica

**Clase**: `Writer(Specialist)`

**Responsabilidades Específicas**:
1. Generar contenido basado en contexto
2. Editar y mejorar texto existente
3. Formatear contenido (markdown, HTML básico)
4. Adaptar tono y estilo según instrucciones
5. Generar múltiples versiones si se solicita

**Métodos Públicos**:

```python
class Writer(Specialist):
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4",
        max_length: int = 5000,
        supported_formats: List[str] = ["markdown", "plain"]
    ) -> None
    
    async def execute(
        self,
        task: Task
    ) -> TaskResult:
        """
        Ejecuta tarea de escritura.
        
        Task.parameters debe incluir:
            - content_type: str ("article" | "summary" | "email" | "document")
            - topic: str
            - context: dict (información de investigación, etc.)
            - style: str ("formal" | "casual" | "technical") (opcional)
            - length: str ("short" | "medium" | "long") (opcional)
            - format: str ("markdown" | "plain" | "html") (opcional)
        
        Returns TaskResult con:
            - result.content: str (contenido generado)
            - result.format: str
            - result.word_count: int
            - result.metadata.generation_time: float
        """
    
    async def generate_content(
        self,
        topic: str,
        context: dict,
        style: str = "formal",
        length: str = "medium"
    ) -> str:
        """
        Genera contenido nuevo.
        """
    
    async def edit_content(
        self,
        content: str,
        instructions: str
    ) -> str:
        """
        Edita contenido existente según instrucciones.
        """
    
    async def format_content(
        self,
        content: str,
        target_format: str
    ) -> str:
        """
        Formatea contenido al formato especificado.
        """
```

**Herramientas Disponibles**:
1. `text_generator`: Generación de texto (usando LLM)
2. `text_formatter`: Formateo de texto
3. `text_analyzer`: Análisis de texto (conteo de palabras, etc.)

**Configuración**:

```yaml
writer:
  name: "Writing Specialist"
  model: "gpt-4"
  instructions: |
    You are a writing specialist. Your job is to:
    1. Generate high-quality content based on context
    2. Edit and improve existing text
    3. Format content appropriately
    4. Adapt tone and style as needed
    
    Rules:
    - Always follow the requested format
    - Maintain consistency in tone
    - Ensure clarity and readability
    - Maximum 5000 words per piece
  max_length: 5000
  supported_formats:
    - markdown
    - plain
  tools:
    - text_generator
    - text_formatter
    - text_analyzer
  max_tokens: 4000
  timeout: 180
```

**Profundidad de Implementación**:
- ✅ Generación de contenido básica
- ✅ Edición de texto
- ✅ Formateo markdown y texto plano
- ✅ Control de longitud y estilo
- ❌ Generación de HTML complejo (para v2.0)
- ❌ Traducción automática (para v2.0)
- ❌ Generación de múltiples variantes automáticas (para v2.0)

---

## 4. Validator (Validador)

### Especificación Técnica

**Clase**: `Validator(Agent)`

**Responsabilidades Específicas**:
1. Validar formato de outputs
2. Verificar calidad de contenido (score 0-1)
3. Verificar cumplimiento de políticas
4. Detectar errores obvios
5. Proporcionar feedback constructivo

**Métodos Públicos**:

```python
class Validator(Agent):
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4",
        min_quality_score: float = 0.7,
        strict_mode: bool = True
    ) -> None
    
    async def validate(
        self,
        content: Any,
        validation_rules: List[ValidationRule]
    ) -> ValidationResult:
        """
        Valida contenido según reglas.
        
        Args:
            content: Contenido a validar
            validation_rules: Lista de reglas a aplicar:
                - "format_check": Verifica formato
                - "quality_check": Verifica calidad
                - "policy_check": Verifica políticas
                - "completeness_check": Verifica completitud
        
        Returns ValidationResult con:
            - valid: bool
            - score: float (0-1)
            - issues: List[ValidationIssue]
            - recommendations: List[str]
        """
    
    async def check_format(
        self,
        content: Any,
        expected_format: dict
    ) -> FormatCheckResult:
        """
        Verifica que el contenido cumple con el formato esperado.
        """
    
    async def check_quality(
        self,
        content: str
    ) -> QualityScore:
        """
        Evalúa la calidad del contenido.
        
        Returns:
            QualityScore con:
                - score: float (0-1)
                - criteria: dict (clarity, accuracy, completeness, etc.)
        """
    
    async def check_policies(
        self,
        content: str
    ) -> PolicyCheckResult:
        """
        Verifica cumplimiento de políticas.
        
        Returns:
            PolicyCheckResult con:
                - compliant: bool
                - violations: List[PolicyViolation]
        """
```

**Reglas de Validación**:

1. **Format Check**: Verifica estructura, tipos de datos, campos requeridos
2. **Quality Check**: Evalúa claridad, precisión, completitud (score mínimo: 0.7)
3. **Policy Check**: Verifica contenido ofensivo, información sensible, etc.
4. **Completeness Check**: Verifica que toda la información requerida esté presente

**Configuración**:

```yaml
validator:
  name: "Quality Validator"
  model: "gpt-4"
  instructions: |
    You are a quality validator. Your job is to:
    1. Validate outputs against defined standards
    2. Check for quality, accuracy, and completeness
    3. Verify policy compliance
    4. Provide constructive feedback
    
    Rules:
    - Be thorough but fair
    - Minimum quality score: 0.7
    - Reject content that violates policies
    - Provide actionable feedback
  min_quality_score: 0.7
  strict_mode: true
  validation_rules:
    - format_check
    - quality_check
    - policy_check
    - completeness_check
  tools: []  # Validator no usa herramientas externas
```

**Profundidad de Implementación**:
- ✅ Validación de formato básica
- ✅ Evaluación de calidad usando LLM
- ✅ Detección de políticas básicas (contenido ofensivo)
- ✅ Generación de feedback
- ❌ Validación de hechos automática (para v2.0)
- ❌ Análisis de sesgos avanzado (para v2.0)
- ❌ Validación de código (para v2.0)

---

## 5. MemorySystem (Sistema de Memoria)

### Especificación Técnica

**Clase**: `MemorySystem` (no extiende Agent, pero actúa como servicio)

**Responsabilidades Específicas**:
1. Almacenar información de sesiones
2. Almacenar información de tareas
3. Recuperar contexto histórico
4. Gestionar políticas de retención
5. Búsqueda básica (no semántica en MVP)

**Métodos Públicos**:

```python
class MemorySystem:
    def __init__(
        self,
        backend: MemoryBackend,
        retention_policies: RetentionPolicies
    ) -> None
    
    async def store(
        self,
        key: str,
        value: Any,
        metadata: dict,
        ttl: Optional[timedelta] = None
    ) -> None:
        """
        Almacena información en memoria.
        
        Args:
            key: Identificador único
            value: Valor a almacenar
            metadata: Metadatos (tags, timestamp, etc.)
            ttl: Time to live (opcional, usa política por defecto)
        """
    
    async def retrieve(
        self,
        key: str
    ) -> Optional[MemoryItem]:
        """
        Recupera información por clave.
        """
    
    async def search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """
        Busca información (búsqueda de texto simple en MVP).
        
        Args:
            query: Texto a buscar
            tags: Filtrar por tags (opcional)
            limit: Máximo de resultados
        
        Returns:
            Lista de MemoryItem ordenados por relevancia
        """
    
    async def delete(
        self,
        key: str
    ) -> None:
        """
        Elimina información (solo si TTL expiró o manualmente).
        """
```

**Backends Disponibles en MVP**:
1. **InMemoryBackend**: Para desarrollo/testing (almacena en memoria)
2. **SQLiteBackend**: Para producción simple (almacena en SQLite)

**Configuración**:

```yaml
memory:
  name: "Memory System"
  backend: "sqlite"  # "in_memory" | "sqlite"
  backend_config:
    database_path: "./memory.db"
  retention_policies:
    session: "1h"      # Memoria de sesión: 1 hora
    task: "7d"         # Memoria de tarea: 7 días
    user: "30d"        # Memoria de usuario: 30 días
    system: "90d"      # Memoria de sistema: 90 días
  max_context_size: 10000  # Máximo de caracteres por item
  enable_semantic_search: false  # Para v2.0
```

**Profundidad de Implementación**:
- ✅ Almacenamiento y recuperación básica
- ✅ Búsqueda de texto simple
- ✅ Políticas de retención
- ✅ Backends intercambiables (InMemory, SQLite)
- ❌ Búsqueda semántica (para v2.0)
- ❌ Backends avanzados (Redis, Vector DB) (para v2.0)
- ❌ Compresión de contexto (para v2.0)

---

## 6. Tool Registry (Infraestructura)

### Especificación Técnica

**Clase**: `ToolRegistry`

**Responsabilidades Específicas**:
1. Registrar herramientas disponibles
2. Proporcionar herramientas a agentes
3. Validar parámetros de herramientas
4. Ejecutar herramientas con manejo de errores

**Herramientas Incluidas en MVP**:

1. **web_search**: Búsqueda web
   - Parámetros: `query: str, max_results: int = 5`
   - Retorna: `List[Source]`

2. **document_parser**: Parser de documentos
   - Parámetros: `document: str, format: str = "plain"`
   - Retorna: `ParsedDocument`

3. **text_extractor**: Extracción de texto
   - Parámetros: `content: str`
   - Retorna: `str`

4. **text_generator**: Generación de texto
   - Parámetros: `prompt: str, max_tokens: int = 1000`
   - Retorna: `str`

5. **text_formatter**: Formateo de texto
   - Parámetros: `content: str, format: str`
   - Retorna: `str`

6. **text_analyzer**: Análisis de texto
   - Parámetros: `content: str`
   - Retorna: `TextAnalysis` (word_count, sentences, etc.)

**Métodos Públicos**:

```python
class ToolRegistry:
    def register(self, tool: Tool) -> None:
        """Registra una herramienta."""
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Obtiene una herramienta por nombre."""
    
    def list_tools(self, category: Optional[str] = None) -> List[Tool]:
        """Lista herramientas disponibles."""
    
    async def execute_tool(
        self,
        tool_name: str,
        params: dict
    ) -> Any:
        """
        Ejecuta una herramienta con validación.
        
        Raises:
            ToolNotFoundError: Si la herramienta no existe
            InvalidParametersError: Si los parámetros son inválidos
            ToolExecutionError: Si la ejecución falla
        """
```

**Profundidad de Implementación**:
- ✅ Registry básico funcional
- ✅ Validación de parámetros
- ✅ Manejo de errores
- ✅ 6 herramientas básicas incluidas
- ❌ Herramientas avanzadas (para v2.0)
- ❌ Soporte MCP (para v2.0)
- ❌ Herramientas dinámicas (para v2.0)

---

## Definiciones de Datos

### Task

```python
@dataclass
class Task:
    id: str
    description: str
    type: str  # "research" | "write" | "analyze" | "validate"
    parameters: dict
    expected_output: Optional[dict] = None
    context: Optional[dict] = None
    priority: int = 3  # 1-5
    deadline: Optional[datetime] = None
```

### TaskResult

```python
@dataclass
class TaskResult:
    task_id: str
    status: str  # "completed" | "failed" | "partial" | "pending"
    result: Any
    subtasks: Optional[List[SubTaskResult]] = None
    metadata: dict = field(default_factory=dict)
    error: Optional[str] = None
```

### AgentMessage

```python
@dataclass
class AgentMessage:
    id: str
    timestamp: datetime
    from_role: AgentRole
    to_role: AgentRole
    type: MessageType
    payload: dict
    metadata: dict = field(default_factory=dict)
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
```

### MemoryItem

```python
@dataclass
class MemoryItem:
    key: str
    value: Any
    metadata: dict
    created_at: datetime
    expires_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
```

---

## Límites y Restricciones del MVP

### Límites Técnicos

- **Máximo de subtareas por tarea**: 5
- **Timeout por subtarea**: 5 minutos
- **Máximo de reintentos**: 2
- **Máximo de fuentes en investigación**: 5
- **Máximo de páginas de documento**: 10
- **Máximo de palabras por escrito**: 5000
- **Score mínimo de calidad**: 0.7
- **Tamaño máximo de contexto en memoria**: 10000 caracteres

### Modelos LLM

- **Modelo por defecto**: GPT-4
- **Modelos soportados**: GPT-4, GPT-3.5-turbo (configurable)
- **No incluido en MVP**: Claude, otros modelos (para v2.0)

### Backends

- **Memoria**: InMemory, SQLite
- **No incluido en MVP**: Redis, PostgreSQL, Vector DBs

---

## Criterios de Éxito del MVP

### Funcionalidad

- ✅ Coordinator puede descomponer y asignar tareas
- ✅ Researcher puede buscar y analizar información
- ✅ Writer puede generar contenido
- ✅ Validator puede validar outputs
- ✅ MemorySystem puede almacenar y recuperar información
- ✅ ToolRegistry puede ejecutar herramientas

### Calidad

- ✅ Cobertura de tests: > 80%
- ✅ Documentación: 100% de APIs públicas
- ✅ Type hints: 100% del código
- ✅ Ejemplos funcionando end-to-end

### Performance

- ✅ Latencia de mensajes: < 1 segundo
- ✅ Tiempo de ejecución de tarea simple: < 30 segundos
- ✅ Tiempo de ejecución de tarea compleja: < 5 minutos

---

## Roadmap Post-MVP (v2.0)

### Agentes Adicionales
- Analyst (análisis de datos)
- Translator (traducción)
- CodeReviewer (revisión de código)

### Features Avanzadas
- Búsqueda semántica en memoria
- Soporte MCP completo
- Self-evolution mechanisms
- Distributed execution
- Backends avanzados (Redis, Vector DBs)

---

**Última actualización**: Enero 2025  
**Versión**: 1.0 (MVP)  
**Estado**: Especificación Final
