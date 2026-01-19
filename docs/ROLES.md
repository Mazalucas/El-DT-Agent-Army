# Roles de Agentes: Definición y Responsabilidades

## Visión General

Este documento define los roles disponibles en el sistema **Agents_Army**, sus responsabilidades, permisos, límites y patrones de interacción.

## Roles Principales

### 1. Coordinator (Coordinador)

**Descripción**: Agente central que orquesta el flujo de trabajo, descompone tareas y coordina la comunicación entre agentes.

**Responsabilidades**:
- Recibir objetivos globales del usuario o sistema
- Descomponer tareas complejas en subtareas manejables
- Asignar tareas a agentes especializados según sus capacidades
- Supervisar el progreso de las tareas
- Sintetizar resultados de múltiples agentes
- Gestionar el flujo de comunicación entre agentes
- Tomar decisiones sobre reintentos y fallbacks

**Permisos**:
- ✅ Crear y asignar tareas a cualquier agente
- ✅ Reasignar tareas entre agentes
- ✅ Consultar estado de cualquier agente
- ✅ Acceder a memoria para contexto histórico
- ✅ Solicitar validación de outputs
- ✅ Escalar a supervisor humano cuando sea necesario
- ✅ Modificar prioridades de tareas

**Límites**:
- ❌ No ejecuta tareas especializadas directamente
- ❌ No puede modificar reglas del sistema
- ❌ No puede acceder a datos sensibles sin autorización
- ❌ No puede omitir validaciones obligatorias

**Interacciones Típicas**:
```
User → Coordinator → Specialist → Coordinator → Validator → Coordinator → User
```

**Configuración Ejemplo**:
```yaml
coordinator:
  name: "Main Coordinator"
  capabilities:
    - task_decomposition
    - agent_coordination
    - result_synthesis
  max_concurrent_tasks: 10
  timeout: 300s
```

---

### 2. Specialist (Especialista)

**Descripción**: Agente genérico especializado en un dominio específico. Puede tener múltiples variantes (Researcher, Writer, Analyst, etc.).

**Responsabilidades**:
- Ejecutar tareas dentro de su dominio de especialización
- Utilizar herramientas específicas de su dominio
- Proporcionar resultados de alta calidad
- Reportar progreso y actualizaciones de estado
- Manejar errores dentro de su capacidad

**Permisos**:
- ✅ Ejecutar tareas asignadas por el coordinador
- ✅ Acceder a herramientas de su dominio
- ✅ Consultar memoria para contexto relevante
- ✅ Solicitar ayuda a otros especialistas (vía coordinador)
- ✅ Reportar errores y problemas

**Límites**:
- ❌ No puede asignar tareas a otros agentes
- ❌ No puede modificar reglas o políticas
- ❌ No puede acceder a herramientas fuera de su dominio
- ❌ No puede omitir validaciones

**Variantes de Especialista**:

#### 2.1 Researcher (Investigador)

**Dominio**: Investigación y búsqueda de información

**Herramientas**:
- Búsqueda web
- Consulta de bases de datos
- Análisis de documentos
- Extracción de información

**Outputs Típicos**:
- Resúmenes de investigación
- Listas de fuentes
- Análisis comparativos
- Datos estructurados

#### 2.2 Writer (Escritor)

**Dominio**: Generación y edición de contenido

**Herramientas**:
- Generación de texto
- Edición y revisión
- Formateo de contenido
- Traducción

**Outputs Típicos**:
- Documentos completos
- Contenido formateado
- Textos editados
- Traducciones

#### 2.3 Analyst (Analista)

**Dominio**: Análisis de datos y generación de insights

**Herramientas**:
- Procesamiento de datos
- Análisis estadístico
- Visualización
- Generación de reportes

**Outputs Típicos**:
- Análisis estadísticos
- Gráficos y visualizaciones
- Reportes ejecutivos
- Recomendaciones

**Configuración Ejemplo**:
```yaml
specialist:
  type: "researcher"
  name: "Research Specialist"
  capabilities:
    - web_search
    - document_analysis
    - information_extraction
  tools:
    - search_engine_api
    - document_parser
  max_tokens: 4000
  timeout: 180s
```

---

### 3. Validator (Validador / Observador)

**Descripción**: Agente responsable de verificar la calidad, precisión y cumplimiento de políticas de los outputs.

**Responsabilidades**:
- Validar outputs según estándares definidos
- Verificar cumplimiento de políticas éticas
- Detectar errores y problemas de calidad
- Proporcionar feedback constructivo
- Aprobar o rechazar outputs
- Mantener logs de validación

**Permisos**:
- ✅ Acceder a todos los outputs para validación
- ✅ Consultar reglas y políticas
- ✅ Rechazar outputs que no cumplan estándares
- ✅ Solicitar correcciones
- ✅ Acceder a contexto histórico para validación

**Límites**:
- ❌ No puede modificar outputs directamente
- ❌ No puede ejecutar tareas
- ❌ No puede omitir validaciones por conveniencia
- ❌ No puede acceder a datos sensibles sin necesidad

**Criterios de Validación**:
1. **Formato**: Cumple con el formato esperado
2. **Calidad**: Score mínimo de calidad (0.7)
3. **Políticas**: No viola políticas éticas o de seguridad
4. **Completitud**: Contiene toda la información requerida
5. **Precisión**: Información verificable y precisa

**Configuración Ejemplo**:
```yaml
validator:
  name: "Quality Validator"
  validation_rules:
    - format_check
    - quality_check
    - policy_check
    - completeness_check
  min_quality_score: 0.7
  strict_mode: true
```

---

### 4. Memory (Sistema de Memoria)

**Descripción**: Agente responsable de gestionar el contexto persistente y la memoria del sistema.

**Responsabilidades**:
- Almacenar información relevante de interacciones
- Recuperar contexto histórico cuando sea necesario
- Gestionar políticas de retención y expiración
- Proporcionar búsqueda semántica de memoria
- Mantener índices y metadatos
- Limpiar información obsoleta

**Permisos**:
- ✅ Almacenar cualquier información autorizada
- ✅ Consultar y recuperar información almacenada
- ✅ Gestionar políticas de retención
- ✅ Indexar y organizar información

**Límites**:
- ❌ No puede modificar registros históricos
- ❌ No puede eliminar información antes de su TTL
- ❌ No puede acceder a información sin autorización
- ❌ No puede almacenar información sensible sin cifrado

**Tipos de Memoria**:
1. **Memoria de Sesión**: Contexto de la conversación actual
2. **Memoria de Tarea**: Información relevante para tareas específicas
3. **Memoria de Usuario**: Preferencias y contexto del usuario
4. **Memoria de Sistema**: Decisiones y patrones aprendidos

**Configuración Ejemplo**:
```yaml
memory:
  name: "Memory System"
  storage_backend: "vector_db"
  retention_policies:
    session: "1h"
    task: "7d"
    user: "30d"
    system: "90d"
  max_context_size: 10000
  enable_semantic_search: true
```

---

### 5. Tool (Herramienta Externa)

**Descripción**: Componente determinístico que ejecuta funciones específicas (APIs, cálculos, servicios externos).

**Responsabilidades**:
- Ejecutar funciones específicas bajo contrato
- Proporcionar resultados determinísticos
- Manejar errores de ejecución
- Reportar estado y disponibilidad

**Permisos**:
- ✅ Ejecutar su función específica
- ✅ Acceder a recursos necesarios (APIs, bases de datos)
- ✅ Reportar errores y limitaciones

**Límites**:
- ❌ No toma decisiones autónomas
- ❌ No puede modificar su comportamiento sin actualización
- ❌ No puede acceder a información fuera de su alcance

**Ejemplos de Herramientas**:
- API de búsqueda web
- Calculadora
- Generador de imágenes
- Traductor
- Base de datos

**Configuración Ejemplo**:
```yaml
tool:
  name: "Web Search API"
  type: "external_api"
  endpoint: "https://api.example.com/search"
  authentication:
    type: "api_key"
    env_var: "SEARCH_API_KEY"
  rate_limit: 100
  timeout: 30s
```

---

### 6. Supervisor (Supervisor Humano)

**Descripción**: Punto de contacto humano para supervisión, aprobación y escalamiento.

**Responsabilidades**:
- Revisar outputs críticos
- Aprobar acciones sensibles
- Intervenir en casos de error o ambigüedad
- Proporcionar feedback y correcciones
- Configurar políticas y reglas

**Permisos**:
- ✅ Revisar cualquier output
- ✅ Aprobar o rechazar acciones
- ✅ Modificar políticas y reglas
- ✅ Interrumpir ejecuciones
- ✅ Acceder a todos los logs

**Límites**:
- Requiere intervención manual (no autónomo)
- Debe seguir protocolos de seguridad

**Casos de Uso**:
- Aprobación de acciones críticas
- Revisión de contenido sensible
- Resolución de conflictos
- Configuración inicial

---

## Matriz de Interacciones

| De \ A | Coordinator | Specialist | Validator | Memory | Tool | Supervisor |
|--------|------------|------------|-----------|--------|------|------------|
| **Coordinator** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Specialist** | ✅ | ⚠️* | ❌ | ✅ | ✅ | ❌ |
| **Validator** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Memory** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Tool** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Supervisor** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

*Especialistas pueden comunicarse entre sí solo vía coordinador

## Patrones de Colaboración

### Patrón 1: Tarea Simple
```
Coordinator → Specialist → Coordinator → Validator → Coordinator
```

### Patrón 2: Tarea Compleja
```
Coordinator → Researcher → Coordinator → Writer → Coordinator → Validator → Coordinator
```

### Patrón 3: Tarea con Memoria
```
Coordinator → Memory (query) → Coordinator → Specialist → Coordinator → Memory (store) → Coordinator
```

### Patrón 4: Tarea con Error
```
Coordinator → Specialist → Error → Coordinator → Specialist (retry) → Coordinator → Validator
```

### Patrón 5: Escalamiento Humano
```
Coordinator → Specialist → Coordinator → Validator → Rejection → Coordinator → Supervisor → Approval → Coordinator
```

## Definición de Nuevos Roles

Para agregar un nuevo rol al sistema:

1. **Definir Responsabilidades**: ¿Qué hace este rol?
2. **Establecer Permisos**: ¿Qué puede hacer?
3. **Definir Límites**: ¿Qué no puede hacer?
4. **Especificar Interacciones**: ¿Con quién interactúa?
5. **Crear Configuración**: Definir parámetros y capacidades
6. **Documentar**: Agregar a este documento

**Template**:
```yaml
new_role:
  name: "Role Name"
  description: "Brief description"
  responsibilities:
    - "Responsibility 1"
    - "Responsibility 2"
  permissions:
    - "Permission 1"
    - "Permission 2"
  limits:
    - "Limit 1"
    - "Limit 2"
  interactions:
    - "Can interact with X"
    - "Cannot interact with Y"
  configuration:
    param1: "value1"
    param2: "value2"
```
