# Observabilidad y Monitoreo: Agents_Army

## Visión General

Este documento define la estrategia completa de observabilidad, monitoreo, logging y alertas para **Agents_Army**.

## Componentes de Observabilidad

### 1. Métricas (Metrics)

### 2. Logging

### 3. Tracing

### 4. Alertas

## Métricas

### Métricas del Sistema

```python
class SystemMetrics:
    # Métricas de sistema
    cpu_usage: Gauge
    memory_usage: Gauge
    disk_usage: Gauge
    network_io: Counter
    
    # Métricas de requests
    request_rate: Counter
    request_latency: Histogram
    request_errors: Counter
    
    # Métricas de agentes
    agent_tasks_completed: Counter
    agent_tasks_failed: Counter
    agent_execution_time: Histogram
    agent_quality_scores: Histogram
    
    # Métricas de El DT
    dt_decisions_autonomous: Counter
    dt_decisions_escalated: Counter
    dt_confidence_scores: Histogram
    dt_decision_time: Histogram
    
    # Métricas de costos
    llm_tokens_used: Counter
    llm_api_calls: Counter
    total_cost: Counter
```

### Implementación

```python
from prometheus_client import Counter, Gauge, Histogram

class MetricsCollector:
    def __init__(self):
        # Métricas de agentes
        self.agent_tasks = Counter(
            'agent_tasks_total',
            'Total tasks executed by agent',
            ['agent_role', 'status']
        )
        
        self.agent_latency = Histogram(
            'agent_execution_seconds',
            'Agent execution time',
            ['agent_role'],
            buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0]
        )
        
        # Métricas de El DT
        self.dt_decisions = Counter(
            'dt_decisions_total',
            'Total decisions by El DT',
            ['decision_type', 'autonomous']
        )
        
        # Métricas de costos
        self.llm_cost = Counter(
            'llm_cost_total',
            'Total LLM API cost',
            ['model', 'provider']
        )
    
    def record_agent_task(
        self,
        agent_role: str,
        status: str,
        duration: float
    ):
        """Registra ejecución de tarea de agente."""
        self.agent_tasks.labels(
            agent_role=agent_role,
            status=status
        ).inc()
        
        self.agent_latency.labels(
            agent_role=agent_role
        ).observe(duration)
    
    def record_dt_decision(
        self,
        decision_type: str,
        autonomous: bool
    ):
        """Registra decisión de El DT."""
        self.dt_decisions.labels(
            decision_type=decision_type,
            autonomous=str(autonomous)
        ).inc()
```

## Logging

### Estructura de Logs

```python
import structlog

logger = structlog.get_logger()

# Log estructurado
logger.info(
    "task_completed",
    task_id="task_123",
    agent="researcher",
    duration=2.5,
    status="success",
    quality_score=0.9
)
```

### Niveles de Log

```yaml
logging:
  levels:
    DEBUG: "Development only"
    INFO: "Normal operations"
    WARNING: "Unexpected but handled"
    ERROR: "Errors that need attention"
    CRITICAL: "System failures"
  
  structured: true
  format: "json"
  
  destinations:
    - console
    - file: "logs/agents_army.log"
    - remote: "loki"  # o ELK stack
```

### Logging por Componente

```python
class ComponentLogger:
    def __init__(self, component: str):
        self.logger = structlog.get_logger(component=component)
    
    def log_agent_action(
        self,
        agent: Agent,
        action: str,
        **kwargs
    ):
        """Log de acción de agente."""
        self.logger.info(
            "agent_action",
            agent_role=agent.role,
            agent_id=agent.id,
            action=action,
            **kwargs
        )
    
    def log_dt_decision(
        self,
        decision: Decision,
        situation: Situation
    ):
        """Log de decisión del DT."""
        self.logger.info(
            "dt_decision",
            decision_type=decision.action,
            autonomous=decision.autonomous,
            confidence=decision.confidence,
            risk=decision.risk,
            situation_id=situation.id
        )
```

## Tracing

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

tracer = trace.get_tracer(__name__)

class TracedAgent:
    async def execute(
        self,
        task: Task
    ) -> TaskResult:
        """Ejecuta tarea con tracing."""
        with tracer.start_as_current_span(
            "agent.execute",
            attributes={
                "agent.role": self.role,
                "task.id": task.id,
                "task.type": task.type
            }
        ) as span:
            try:
                result = await self._execute_internal(task)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
```

### Trace Context Propagation

```python
class TraceContext:
    def inject_trace_context(
        self,
        message: AgentMessage
    ) -> None:
        """Inyecta contexto de trace en mensaje."""
        context = trace.get_current_span().get_span_context()
        message.metadata["trace_id"] = format(context.trace_id, "032x")
        message.metadata["span_id"] = format(context.span_id, "016x")
    
    def extract_trace_context(
        self,
        message: AgentMessage
    ) -> SpanContext:
        """Extrae contexto de trace de mensaje."""
        trace_id = int(message.metadata.get("trace_id", "0"), 16)
        span_id = int(message.metadata.get("span_id", "0"), 16)
        return SpanContext(trace_id, span_id)
```

## Dashboards

### Dashboard Principal

```yaml
dashboard:
  name: "Agents_Army Overview"
  panels:
    - title: "System Health"
      metrics:
        - cpu_usage
        - memory_usage
        - request_rate
        - error_rate
    
    - title: "Agent Performance"
      metrics:
        - agent_tasks_completed
        - agent_tasks_failed
        - agent_execution_time
        - agent_quality_scores
    
    - title: "El DT Decisions"
      metrics:
        - dt_decisions_autonomous
        - dt_decisions_escalated
        - dt_confidence_scores
        - dt_decision_time
    
    - title: "Costs"
      metrics:
        - llm_tokens_used
        - llm_api_calls
        - total_cost
        - cost_per_task
```

### Dashboard por Agente

```yaml
agent_dashboard:
  metrics:
    - tasks_completed
    - tasks_failed
    - average_quality
    - average_time
    - tools_used
    - errors_by_type
  
  visualizations:
    - "Tasks over time"
    - "Quality score distribution"
    - "Error rate trend"
    - "Tool usage"
```

## Alertas

### Configuración de Alertas

```yaml
alerts:
  - name: "high_error_rate"
    condition: "error_rate > 5%"
    duration: "5m"
    severity: "warning"
    action:
      - "notify_team"
      - "log_incident"
  
  - name: "agent_failure_rate"
    condition: "agent_failure_rate > 10%"
    duration: "10m"
    severity: "critical"
    action:
      - "alert_dt"
      - "escalate_to_admin"
      - "create_incident"
  
  - name: "high_latency"
    condition: "p95_latency > 5s"
    duration: "5m"
    severity: "warning"
    action:
      - "notify_team"
      - "investigate"
  
  - name: "cost_threshold"
    condition: "daily_cost > $100"
    severity: "warning"
    action:
      - "notify_admin"
      - "review_usage"
  
  - name: "dt_low_confidence"
    condition: "dt_avg_confidence < 0.6"
    duration: "15m"
    severity: "info"
    action:
      - "log_for_review"
```

### Implementación

```python
class AlertManager:
    def __init__(self):
        self.alerts = []
        self.notifiers = []
    
    async def check_alerts(self):
        """Verifica condiciones de alertas."""
        for alert in self.alerts:
            if await self.evaluate_condition(alert.condition):
                await self.trigger_alert(alert)
    
    async def trigger_alert(
        self,
        alert: Alert
    ):
        """Dispara una alerta."""
        # Registrar
        await self.log_alert(alert)
        
        # Notificar
        for notifier in self.notifiers:
            await notifier.notify(alert)
        
        # Acciones
        for action in alert.actions:
            await self.execute_action(action, alert)
```

## Health Checks

### Health Check Endpoints

```python
# agents_army/health.py
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health")
async def health():
    """Health check básico."""
    return {"status": "healthy"}

@router.get("/ready")
async def ready():
    """Readiness check."""
    system = AgentSystem.get_instance()
    
    checks = {
        "agents": system.agents_ready(),
        "memory": system.memory_ready(),
        "tools": system.tools_ready(),
        "dt": system.dt_ready()
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        return Response(
            status_code=503,
            content={"status": "not_ready", "checks": checks}
        )

@router.get("/live")
async def live():
    """Liveness check."""
    return {"status": "alive", "pid": os.getpid()}
```

## Performance Monitoring

### APM (Application Performance Monitoring)

```python
class APM:
    def track_agent_performance(
        self,
        agent: Agent,
        task: Task,
        result: TaskResult
    ):
        """Track performance de agente."""
        metrics = {
            "duration": result.duration,
            "tokens_used": result.tokens_used,
            "quality_score": result.quality_score,
            "cost": result.cost
        }
        
        self.record_metrics(
            f"agent.{agent.role}",
            metrics
        )
```

## Cost Tracking

### Tracking de Costos

```python
class CostTracker:
    def track_llm_usage(
        self,
        model: str,
        provider: str,
        tokens: int,
        cost: float
    ):
        """Track uso de LLM."""
        self.cost_counter.labels(
            model=model,
            provider=provider
        ).inc(cost)
        
        self.tokens_counter.labels(
            model=model,
            provider=provider
        ).inc(tokens)
    
    def get_daily_cost(self) -> float:
        """Obtiene costo diario."""
        return self.cost_counter.sum()
    
    def estimate_task_cost(
        self,
        task: Task
    ) -> float:
        """Estima costo de una tarea."""
        # Basado en historial
        similar_tasks = self.find_similar_tasks(task)
        avg_cost = sum(t.cost for t in similar_tasks) / len(similar_tasks)
        return avg_cost
```

## Log Aggregation

### Configuración

```yaml
log_aggregation:
  backend: "loki"  # o ELK stack
  
  retention:
    development: "7d"
    staging: "30d"
    production: "90d"
  
  indexing:
    fields:
      - "agent_role"
      - "task_id"
      - "status"
      - "timestamp"
  
  queries:
    - "Find all errors from researcher agent"
    - "Tasks that took > 10s"
    - "DT decisions that were escalated"
```

## Observabilidad de El DT

### Métricas Específicas

```python
class DTMetrics:
    def track_decision(
        self,
        decision: Decision,
        situation: Situation
    ):
        """Track decisión del DT."""
        self.decisions_total.inc()
        
        if decision.autonomous:
            self.autonomous_decisions.inc()
        else:
            self.escalated_decisions.inc()
        
        self.confidence_histogram.observe(decision.confidence)
        self.risk_gauge.set(decision.risk.value)
    
    def track_learning(
        self,
        adjustment: ThresholdAdjustment
    ):
        """Track ajuste de umbrales."""
        self.threshold_adjustments.inc()
        self.current_threshold.set(adjustment.new_value)
```

## Integración con Herramientas

### Prometheus

```python
# Exponer métricas en formato Prometheus
from prometheus_client import make_asgi_app

metrics_app = make_asgi_app()

# En FastAPI
app.mount("/metrics", metrics_app)
```

### Grafana

```yaml
grafana:
  dashboards:
    - "agents_army_overview.json"
    - "agent_performance.json"
    - "dt_decisions.json"
    - "costs.json"
  
  datasources:
    - prometheus
    - loki
    - jaeger
```

## Checklist de Observabilidad

### Setup
- [ ] Métricas configuradas
- [ ] Logging estructurado
- [ ] Tracing habilitado
- [ ] Dashboards creados
- [ ] Alertas configuradas

### Operación
- [ ] Métricas se recopilan
- [ ] Logs se agregan
- [ ] Traces se capturan
- [ ] Alertas funcionan
- [ ] Dashboards actualizados

---

**Última actualización**: Enero 2025  
**Estado**: Estrategia Definida
