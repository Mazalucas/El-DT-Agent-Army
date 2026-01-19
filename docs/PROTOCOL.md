# Protocolo de Agentes: Especificación Técnica

## Visión General

Este documento define el protocolo estándar para comunicación, coordinación y ejecución de tareas entre agentes en el sistema **Agents_Army**.

## Arquitectura del Protocolo

### Componentes Principales

```
┌─────────────────┐
│   Coordinador   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Agente │ │Agente │
│Esp. 1 │ │Esp. 2 │
└───┬───┘ └──┬────┘
    │        │
    └───┬────┘
        │
┌───────▼────────┐
│   Observador   │
└───────┬────────┘
        │
┌───────▼────────┐
│    Memoria     │
└────────────────┘
```

## Especificación de Mensajes

### Esquema Base de Mensaje

```typescript
interface AgentMessage {
  // Identificación
  id: string;                    // UUID único del mensaje
  timestamp: string;              // ISO 8601 timestamp
  correlation_id?: string;        // ID para agrupar mensajes relacionados
  
  // Enrutamiento
  from: AgentRole;                // Rol del agente emisor
  to: AgentRole | AgentRole[];   // Rol(es) del agente receptor
  reply_to?: string;              // ID del mensaje al que responde
  
  // Contenido
  type: MessageType;              // Tipo de mensaje
  payload: Record<string, any>;  // Contenido específico del mensaje
  
  // Metadatos
  metadata: {
    priority: 'low' | 'normal' | 'high' | 'critical';
    retry_count?: number;
    deadline?: string;            // ISO 8601 timestamp
    tags?: string[];
  };
  
  // Seguridad
  signature?: string;             // Firma digital (opcional)
  encryption?: 'none' | 'tls' | 'end-to-end';
}
```

### Tipos de Mensajes

```typescript
type MessageType =
  | 'task_request'      // Solicitud de ejecución de tarea
  | 'task_response'     // Resultado de una tarea
  | 'task_update'       // Actualización de progreso
  | 'error'             // Notificación de error
  | 'status_query'      // Consulta de estado
  | 'status_response'   // Respuesta de estado
  | 'coordination'      // Mensajes de coordinación
  | 'validation_request' // Solicitud de validación
  | 'validation_response' // Resultado de validación
  | 'memory_store'      // Almacenar en memoria
  | 'memory_query'      // Consultar memoria
  | 'memory_response'   // Respuesta de memoria
  | 'heartbeat'         // Latido de salud
  | 'shutdown'          // Solicitud de apagado
  | 'config_update';    // Actualización de configuración
```

### Roles de Agentes

```typescript
type AgentRole =
  | 'coordinator'      // Coordinador principal
  | 'specialist'       // Agente especialista genérico
  | 'researcher'       // Especialista en investigación
  | 'writer'           // Especialista en escritura
  | 'analyst'          // Especialista en análisis
  | 'validator'        // Observador/validador
  | 'memory'           // Sistema de memoria
  | 'tool'             // Herramienta externa
  | 'supervisor';      // Supervisor humano
```

## Protocolos Específicos

### 1. Protocolo de Solicitud de Tarea (Task Request)

**Mensaje de Solicitud:**

```json
{
  "id": "msg_001",
  "timestamp": "2024-01-01T12:00:00Z",
  "from": "coordinator",
  "to": "researcher",
  "type": "task_request",
  "payload": {
    "task_id": "task_001",
    "task_type": "research",
    "description": "Investigar sobre el tema X",
    "parameters": {
      "topic": "X",
      "depth": "medium",
      "sources": 5
    },
    "context": {
      "user_id": "user_123",
      "session_id": "session_456"
    },
    "expected_output": {
      "format": "markdown",
      "sections": ["summary", "details", "sources"]
    },
    "constraints": {
      "max_tokens": 2000,
      "max_time": "PT5M",
      "required_validation": true
    }
  },
  "metadata": {
    "priority": "high",
    "deadline": "2024-01-01T12:05:00Z"
  }
}
```

**Mensaje de Respuesta:**

```json
{
  "id": "msg_002",
  "timestamp": "2024-01-01T12:03:00Z",
  "from": "researcher",
  "to": "coordinator",
  "type": "task_response",
  "reply_to": "msg_001",
  "payload": {
    "task_id": "task_001",
    "status": "completed",
    "result": {
      "content": "...",
      "sources": [...],
      "metadata": {
        "tokens_used": 1500,
        "time_taken": "PT2M30S"
      }
    }
  },
  "metadata": {
    "priority": "normal"
  }
}
```

### 2. Protocolo de Validación

**Mensaje de Solicitud de Validación:**

```json
{
  "id": "msg_003",
  "timestamp": "2024-01-01T12:03:30Z",
  "from": "coordinator",
  "to": "validator",
  "type": "validation_request",
  "payload": {
    "content": "...",
    "validation_rules": [
      "format_check",
      "quality_check",
      "policy_check"
    ],
    "context": {
      "task_id": "task_001",
      "agent": "researcher"
    }
  }
}
```

**Mensaje de Respuesta de Validación:**

```json
{
  "id": "msg_004",
  "timestamp": "2024-01-01T12:03:45Z",
  "from": "validator",
  "to": "coordinator",
  "type": "validation_response",
  "reply_to": "msg_003",
  "payload": {
    "valid": true,
    "score": 0.95,
    "issues": [],
    "recommendations": [
      "Consider adding more recent sources"
    ]
  }
}
```

### 3. Protocolo de Memoria

**Almacenar en Memoria:**

```json
{
  "id": "msg_005",
  "timestamp": "2024-01-01T12:04:00Z",
  "from": "coordinator",
  "to": "memory",
  "type": "memory_store",
  "payload": {
    "key": "task_001_result",
    "value": {
      "content": "...",
      "metadata": {...}
    },
    "ttl": "P7D",  // Time to live: 7 días
    "tags": ["research", "topic_x"]
  }
}
```

**Consultar Memoria:**

```json
{
  "id": "msg_006",
  "timestamp": "2024-01-01T12:05:00Z",
  "from": "researcher",
  "to": "memory",
  "type": "memory_query",
  "payload": {
    "query": {
      "type": "semantic_search",
      "text": "investigación sobre X"
    },
    "limit": 5,
    "filters": {
      "tags": ["research"],
      "date_range": {
        "from": "2024-01-01T00:00:00Z"
      }
    }
  }
}
```

### 4. Protocolo de Manejo de Errores

**Mensaje de Error:**

```json
{
  "id": "msg_007",
  "timestamp": "2024-01-01T12:06:00Z",
  "from": "researcher",
  "to": "coordinator",
  "type": "error",
  "payload": {
    "error_type": "execution_error",
    "error_code": "API_TIMEOUT",
    "message": "API request timed out after 30 seconds",
    "context": {
      "task_id": "task_002",
      "attempt": 2,
      "max_retries": 3
    },
    "recoverable": true,
    "suggested_action": "retry_with_backoff"
  },
  "metadata": {
    "priority": "high"
  }
}
```

## Reglas de Comunicación

### 1. Orden y Prioridad

- Los mensajes se procesan por prioridad: `critical` > `high` > `normal` > `low`
- Mensajes con `deadline` tienen prioridad automática
- Los mensajes de `heartbeat` tienen prioridad `low`

### 2. Timeouts y Reintentos

- **Timeout por defecto**: 30 segundos para tareas normales
- **Reintentos**: Máximo 3 intentos con backoff exponencial (1s, 2s, 4s)
- **Deadline**: Si se especifica, el agente debe responder antes del deadline

### 3. Validación de Mensajes

Todos los mensajes deben:
- Tener `id`, `timestamp`, `from`, `to`, `type` válidos
- Cumplir con el esquema JSON definido
- Tener `payload` no vacío (excepto para `heartbeat`)

### 4. Seguridad

- Autenticación mutua entre agentes
- Cifrado TLS para comunicación en red
- Firma digital opcional para mensajes críticos
- Validación de permisos según rol

## Flujos de Trabajo

### Flujo 1: Ejecución de Tarea Simple

```
1. Coordinator → Specialist: task_request
2. Specialist → Coordinator: task_response
3. Coordinator → Validator: validation_request
4. Validator → Coordinator: validation_response
5. Coordinator → Memory: memory_store
6. Coordinator → User: final_response
```

### Flujo 2: Ejecución con Error

```
1. Coordinator → Specialist: task_request
2. Specialist → Coordinator: error (recoverable)
3. Coordinator → Specialist: task_request (retry)
4. Specialist → Coordinator: task_response
5. Coordinator → Validator: validation_request
6. Validator → Coordinator: validation_response
7. Coordinator → Memory: memory_store
```

### Flujo 3: Tarea Compleja (Multi-Agente)

```
1. Coordinator → Researcher: task_request (research)
2. Researcher → Coordinator: task_response
3. Coordinator → Writer: task_request (write, context from research)
4. Writer → Coordinator: task_response
5. Coordinator → Validator: validation_request
6. Validator → Coordinator: validation_response
7. Coordinator → Memory: memory_store
```

## Políticas y Guardrails

### Políticas de Ejecución

1. **Límites de Recursos**:
   - Tiempo máximo por tarea: 5 minutos (configurable)
   - Tokens máximos: 4000 (configurable)
   - Memoria máxima: 100MB por agente

2. **Políticas Éticas**:
   - Rechazo automático de contenido ofensivo
   - Detección de sesgos
   - Cumplimiento de privacidad (GDPR, CCPA)

3. **Políticas de Calidad**:
   - Validación obligatoria para outputs críticos
   - Score mínimo de calidad: 0.7
   - Revisión humana para tareas de alta importancia

### Guardrails Técnicos

- Validación de esquemas JSON
- Sanitización de inputs
- Rate limiting por agente
- Circuit breakers para servicios externos
- Límites de profundidad de recursión

## Versionado

El protocolo sigue versionado semántico:
- **v1.0.0**: Versión inicial
- Cambios mayores: Cambios incompatibles en esquemas
- Cambios menores: Nuevos tipos de mensajes compatibles
- Patches: Correcciones de bugs

Los mensajes incluyen versión del protocolo:
```json
{
  "protocol_version": "1.0.0",
  ...
}
```
