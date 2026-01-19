# Gestión de Costos: Agents_Army

## Visión General

Este documento define la estrategia de gestión de costos para **Agents_Army**, incluyendo tracking, optimización, presupuestos y alertas.

## Componentes de Costo

### 1. Costos de LLM

```python
class LLMCostCalculator:
    """Calcula costos de llamadas a LLMs."""
    
    PRICING = {
        "gpt-4": {
            "input": 0.03 / 1000,  # $0.03 por 1K tokens
            "output": 0.06 / 1000   # $0.06 por 1K tokens
        },
        "gpt-3.5-turbo": {
            "input": 0.0015 / 1000,
            "output": 0.002 / 1000
        },
        "claude-3-opus": {
            "input": 0.015 / 1000,
            "output": 0.075 / 1000
        }
    }
    
    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calcula costo de una llamada."""
        pricing = self.PRICING.get(model, {})
        input_cost = (input_tokens / 1000) * pricing.get("input", 0)
        output_cost = (output_tokens / 1000) * pricing.get("output", 0)
        return input_cost + output_cost
```

### 2. Costos de APIs Externas

```python
class APICostTracker:
    """Track costos de APIs externas."""
    
    def track_api_call(
        self,
        api_name: str,
        cost: float,
        metadata: dict = None
    ):
        """Registra costo de llamada a API."""
        self.cost_counter.labels(api=api_name).inc(cost)
        
        if metadata:
            self.record_metadata(api_name, metadata)
```

### 3. Costos de Infraestructura

```python
class InfrastructureCost:
    """Calcula costos de infraestructura."""
    
    def calculate_compute_cost(
        self,
        cpu_hours: float,
        memory_gb_hours: float
    ) -> float:
        """Calcula costo de compute."""
        cpu_cost = cpu_hours * 0.10  # $0.10 por CPU-hora
        memory_cost = memory_gb_hours * 0.01  # $0.01 por GB-hora
        return cpu_cost + memory_cost
    
    def calculate_storage_cost(
        self,
        storage_gb: float
    ) -> float:
        """Calcula costo de almacenamiento."""
        return storage_gb * 0.023  # $0.023 por GB/mes
```

## Tracking de Costos

### Cost Tracker

```python
class CostTracker:
    """Sistema central de tracking de costos."""
    
    def __init__(self):
        self.llm_tracker = LLMCostCalculator()
        self.api_tracker = APICostTracker()
        self.infra_tracker = InfrastructureCost()
        self.daily_budget = 100.0  # $100 por día
    
    async def track_task_cost(
        self,
        task: Task,
        execution: Execution
    ) -> CostBreakdown:
        """Track costo completo de una tarea."""
        costs = {
            "llm": 0.0,
            "apis": 0.0,
            "infrastructure": 0.0,
            "total": 0.0
        }
        
        # Costo de LLM
        for llm_call in execution.llm_calls:
            cost = self.llm_tracker.calculate_cost(
                llm_call.model,
                llm_call.input_tokens,
                llm_call.output_tokens
            )
            costs["llm"] += cost
        
        # Costo de APIs
        for api_call in execution.api_calls:
            costs["apis"] += api_call.cost
        
        # Costo de infraestructura
        costs["infrastructure"] = self.infra_tracker.calculate_compute_cost(
            execution.cpu_hours,
            execution.memory_gb_hours
        )
        
        costs["total"] = sum(costs.values())
        
        # Registrar
        await self.record_cost(task.id, costs)
        
        # Verificar presupuesto
        await self.check_budget(costs["total"])
        
        return CostBreakdown(**costs)
    
    async def check_budget(
        self,
        cost: float
    ) -> BudgetCheck:
        """Verifica si excede presupuesto."""
        daily_cost = await self.get_daily_cost()
        
        if daily_cost + cost > self.daily_budget:
            return BudgetCheck(
                within_budget=False,
                remaining=self.daily_budget - daily_cost,
                required=cost,
                action="alert"
            )
        
        return BudgetCheck(
            within_budget=True,
            remaining=self.daily_budget - daily_cost - cost
        )
```

## Estimación de Costos

### Cost Estimator

```python
class CostEstimator:
    """Estima costos antes de ejecutar."""
    
    async def estimate_task_cost(
        self,
        task: Task,
        agent: Agent
    ) -> CostEstimate:
        """Estima costo de una tarea."""
        # Basado en historial
        similar_tasks = await self.find_similar_tasks(task)
        
        if similar_tasks:
            avg_cost = sum(t.cost for t in similar_tasks) / len(similar_tasks)
            return CostEstimate(
                estimated=avg_cost,
                confidence=0.8,
                based_on="historical_data"
            )
        
        # Estimación basada en complejidad
        complexity_factor = self.assess_complexity(task)
        base_cost = 0.10  # $0.10 base
        
        estimated = base_cost * complexity_factor
        
        return CostEstimate(
            estimated=estimated,
            confidence=0.5,
            based_on="complexity_analysis"
        )
    
    async def estimate_project_cost(
        self,
        project: Project
    ) -> ProjectCostEstimate:
        """Estima costo completo de un proyecto."""
        tasks = await project.get_all_tasks()
        
        total_estimate = 0.0
        estimates = []
        
        for task in tasks:
            estimate = await self.estimate_task_cost(task, None)
            estimates.append(estimate)
            total_estimate += estimate.estimated
        
        return ProjectCostEstimate(
            total=total_estimate,
            per_task=estimates,
            confidence=self.calculate_confidence(estimates)
        )
```

## Optimización de Costos

### Cost Optimizer

```python
class CostOptimizer:
    """Optimiza costos del sistema."""
    
    async def optimize_model_selection(
        self,
        task: Task
    ) -> str:
        """Selecciona modelo más económico apropiado."""
        # Para tareas simples, usar modelo más barato
        if task.complexity == "low":
            return "gpt-3.5-turbo"
        
        # Para tareas complejas, usar modelo más capaz
        if task.complexity == "high":
            return "gpt-4"
        
        # Default
        return "gpt-4"
    
    async def suggest_optimizations(
        self,
        project: Project
    ) -> List[OptimizationSuggestion]:
        """Sugiere optimizaciones de costo."""
        suggestions = []
        
        # Analizar uso de modelos
        model_usage = await self.analyze_model_usage(project)
        for model, usage in model_usage.items():
            if usage.cost > usage.budget * 0.8:
                suggestions.append(
                    OptimizationSuggestion(
                        type="model_optimization",
                        description=f"Consider using cheaper model for {usage.tasks}",
                        potential_savings=usage.cost * 0.3
                    )
                )
        
        # Analizar cache hits
        cache_stats = await self.get_cache_stats(project)
        if cache_stats.hit_rate < 0.5:
            suggestions.append(
                OptimizationSuggestion(
                    type="cache_optimization",
                    description="Increase cache usage to reduce API calls",
                    potential_savings=cache_stats.miss_cost * 0.5
                )
            )
        
        return suggestions
```

## Presupuestos y Límites

### Budget Manager

```python
class BudgetManager:
    """Gestiona presupuestos y límites."""
    
    def __init__(self):
        self.budgets = {
            "daily": 100.0,
            "weekly": 500.0,
            "monthly": 2000.0,
            "per_project": {}
        }
    
    async def check_budget(
        self,
        cost: float,
        budget_type: str = "daily"
    ) -> BudgetStatus:
        """Verifica presupuesto."""
        budget = self.budgets.get(budget_type, 0)
        current = await self.get_current_spend(budget_type)
        
        if current + cost > budget:
            return BudgetStatus(
                within_budget=False,
                current=current,
                budget=budget,
                remaining=budget - current,
                action="block"  # o "alert"
            )
        
        return BudgetStatus(
            within_budget=True,
            current=current,
            budget=budget,
            remaining=budget - current - cost
        )
    
    async def enforce_budget(
        self,
        task: Task
    ) -> bool:
        """Aplica límites de presupuesto."""
        estimate = await self.cost_estimator.estimate_task_cost(task, None)
        budget_check = await self.check_budget(estimate.estimated)
        
        if not budget_check.within_budget:
            if budget_check.action == "block":
                raise BudgetExceededError(
                    f"Budget exceeded: {budget_check.current} / {budget_check.budget}"
                )
            elif budget_check.action == "alert":
                await self.send_budget_alert(budget_check)
        
        return budget_check.within_budget
```

## Alertas de Costo

### Cost Alerts

```yaml
cost_alerts:
  - name: "daily_budget_80_percent"
    condition: "daily_cost > daily_budget * 0.8"
    severity: "warning"
    action: "notify_admin"
  
  - name: "daily_budget_exceeded"
    condition: "daily_cost > daily_budget"
    severity: "critical"
    action:
      - "notify_admin"
      - "block_new_tasks"
      - "escalate"
  
  - name: "unusual_cost_spike"
    condition: "hourly_cost > avg_hourly_cost * 2"
    severity: "warning"
    action: "investigate"
  
  - name: "project_budget_exceeded"
    condition: "project_cost > project_budget"
    severity: "critical"
    action:
      - "notify_project_owner"
      - "pause_project"
```

## Reporting

### Cost Reports

```python
class CostReporter:
    """Genera reportes de costos."""
    
    async def generate_daily_report(
        self,
        date: datetime = None
    ) -> DailyCostReport:
        """Genera reporte diario."""
        if date is None:
            date = datetime.now()
        
        costs = await self.get_daily_costs(date)
        
        return DailyCostReport(
            date=date,
            total=costs.total,
            breakdown=costs.breakdown,
            by_agent=costs.by_agent,
            by_project=costs.by_project,
            trends=costs.trends
        )
    
    async def generate_project_report(
        self,
        project: Project
    ) -> ProjectCostReport:
        """Genera reporte de proyecto."""
        costs = await self.get_project_costs(project)
        
        return ProjectCostReport(
            project=project.name,
            total=costs.total,
            estimated=costs.estimated,
            variance=costs.total - costs.estimated,
            breakdown=costs.breakdown,
            recommendations=costs.recommendations
        )
```

## Configuración

```yaml
cost_management:
  budgets:
    daily: 100.0
    weekly: 500.0
    monthly: 2000.0
  
  optimization:
    enabled: true
    auto_select_cheaper_model: true
    cache_enabled: true
    cache_ttl: "1h"
  
  alerts:
    enabled: true
    thresholds:
      warning: 0.8
      critical: 1.0
  
  reporting:
    frequency: "daily"
    recipients: ["admin@example.com"]
```

---

**Última actualización**: Enero 2025  
**Estado**: Estrategia Definida
