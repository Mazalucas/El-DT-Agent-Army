# Autonomía de El DT: Decisión y Acción Autónoma

## Visión General

Este documento define en detalle cómo **El DT** toma decisiones autónomas, elige acciones y actúa sin intervención humana, basándose en reglas, contexto histórico, métricas de confianza y evaluación de riesgo.

## Principios de Autonomía

### Niveles de Autonomía

El DT opera en 4 niveles de autonomía:

1. **Totalmente Autónomo** (Nivel 4)
   - Actúa sin consultar
   - Solo para tareas de bajo riesgo y alta confianza
   - Registra acciones para auditoría

2. **Autónomo con Validación** (Nivel 3)
   - Actúa pero valida resultado antes de finalizar
   - Para tareas de riesgo medio

3. **Consulta Recomendada** (Nivel 2)
   - Sugiere acción pero espera aprobación
   - Para tareas de riesgo medio-alto

4. **Escalamiento Obligatorio** (Nivel 1)
   - Siempre consulta a humano
   - Para tareas críticas o de alto riesgo

## Motor de Decisión Autónoma

### DTAutonomyEngine

```python
class DTAutonomyEngine:
    """
    Motor que permite a El DT decidir y actuar autónomamente.
    """
    
    def __init__(
        self,
        rules: Rules,
        history: DecisionHistory,
        metrics: MetricsCollector
    ):
        self.rules = rules
        self.history = history
        self.metrics = metrics
        self.confidence_calculator = ConfidenceCalculator()
        self.risk_assessor = RiskAssessor()
        self.learning_engine = LearningEngine()
        self.adaptive_thresholds = AdaptiveThresholds()
    
    async def decide_and_act(
        self,
        situation: Situation
    ) -> ActionResult:
        """
        Proceso completo de decisión y acción autónoma.
        
        Flujo:
        1. Analizar situación
        2. Calcular confianza
        3. Evaluar riesgo
        4. Consultar historial
        5. Aplicar reglas
        6. Decidir nivel de autonomía
        7. Ejecutar acción
        8. Aprender del resultado
        """
        # 1. Análisis de situación
        analysis = await self.analyze_situation(situation)
        
        # 2. Cálculo de confianza
        confidence = await self.calculate_confidence(situation, analysis)
        
        # 3. Evaluación de riesgo
        risk = await self.assess_risk(situation, analysis)
        
        # 4. Consulta de historial
        similar_decisions = self.history.find_similar(situation)
        
        # 5. Aplicación de reglas
        rules_check = self.rules.check(situation, analysis)
        
        # 6. Decisión
        decision = self.make_decision(
            confidence=confidence,
            risk=risk,
            rules_check=rules_check,
            history=similar_decisions,
            thresholds=self.adaptive_thresholds
        )
        
        # 7. Ejecución
        if decision.autonomous:
            result = await self.execute_autonomously(decision)
            
            # 8. Aprendizaje
            await self.learn_from_result(situation, decision, result)
            
            return result
        else:
            return await self.escalate_to_human(situation, decision)
```

### Análisis de Situación

```python
class SituationAnalyzer:
    async def analyze(
        self,
        situation: Situation
    ) -> SituationAnalysis:
        """
        Analiza la situación completa.
        """
        return SituationAnalysis(
            task_type=situation.task.type,
            complexity=self.assess_complexity(situation.task),
            agents_available=self.get_available_agents(situation),
            dependencies=self.check_dependencies(situation.task),
            resources_required=self.estimate_resources(situation),
            time_available=self.calculate_time_available(situation),
            context=self.get_relevant_context(situation)
        )
```

### Cálculo de Confianza

```python
class ConfidenceCalculator:
    def calculate(
        self,
        situation: Situation,
        analysis: SituationAnalysis,
        history: List[Decision]
    ) -> ConfidenceScore:
        """
        Calcula score de confianza (0-1) basándose en múltiples factores.
        """
        factors = {
            # Historial de decisiones similares
            "historical_success": self.calculate_historical_success(
                history, situation
            ),
            
            # Confiabilidad de agentes involucrados
            "agent_reliability": self.calculate_agent_reliability(
                analysis.agents_available
            ),
            
            # Complejidad de la tarea
            "complexity_factor": self.complexity_to_confidence(
                analysis.complexity
            ),
            
            # Claridad de la tarea
            "task_clarity": self.assess_task_clarity(situation.task),
            
            # Recursos disponibles
            "resource_availability": self.assess_resources(
                analysis.resources_required
            ),
            
            # Contexto disponible
            "context_quality": self.assess_context_quality(
                analysis.context
            )
        }
        
        # Ponderación de factores
        weights = {
            "historical_success": 0.3,
            "agent_reliability": 0.25,
            "complexity_factor": 0.15,
            "task_clarity": 0.1,
            "resource_availability": 0.1,
            "context_quality": 0.1
        }
        
        confidence = sum(
            factors[key] * weights[key]
            for key in factors
        )
        
        return ConfidenceScore(
            score=confidence,
            factors=factors,
            explanation=self.generate_explanation(factors, weights)
        )
```

### Evaluación de Riesgo

```python
class RiskAssessor:
    def assess(
        self,
        situation: Situation,
        analysis: SituationAnalysis
    ) -> RiskAssessment:
        """
        Evalúa el riesgo de actuar autónomamente.
        """
        risk_factors = {
            # Riesgo de negocio
            "business_impact": self.assess_business_impact(situation),
            
            # Riesgo técnico
            "technical_risk": self.assess_technical_risk(analysis),
            
            # Riesgo de datos
            "data_risk": self.assess_data_risk(situation),
            
            # Riesgo de marca
            "brand_risk": self.assess_brand_risk(situation),
            
            # Riesgo financiero
            "financial_risk": self.assess_financial_risk(situation),
            
            # Riesgo legal
            "legal_risk": self.assess_legal_risk(situation)
        }
        
        # Calcular riesgo total
        total_risk = max(risk_factors.values())  # Usar máximo (peor caso)
        
        return RiskAssessment(
            level=self.categorize_risk(total_risk),
            factors=risk_factors,
            total_score=total_risk,
            mitigation_suggestions=self.suggest_mitigations(risk_factors)
        )
    
    def categorize_risk(self, score: float) -> RiskLevel:
        """
        Categoriza nivel de riesgo.
        """
        if score < 0.3:
            return RiskLevel.LOW
        elif score < 0.6:
            return RiskLevel.MEDIUM
        elif score < 0.8:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
```

### Toma de Decisión

```python
class DecisionMaker:
    def make_decision(
        self,
        confidence: ConfidenceScore,
        risk: RiskAssessment,
        rules_check: RulesCheck,
        history: List[Decision],
        thresholds: AdaptiveThresholds
    ) -> Decision:
        """
        Toma decisión final basándose en todos los factores.
        """
        # Verificar reglas obligatorias primero
        if not rules_check.passed:
            return Decision(
                action=Action.ESCALATE_TO_HUMAN,
                autonomous=False,
                reason=f"Violates mandatory rules: {rules_check.violations}",
                confidence=0.0
            )
        
        # Matriz de decisión
        decision_matrix = {
            # Alta confianza + Bajo riesgo → Autónomo
            (confidence.score > thresholds.autonomous, risk.level == RiskLevel.LOW):
                Decision(
                    action=Action.EXECUTE_AUTONOMOUSLY,
                    autonomous=True,
                    level=AutonomyLevel.FULL,
                    confidence=confidence.score
                ),
            
            # Alta confianza + Riesgo medio → Autónomo con validación
            (confidence.score > thresholds.autonomous, risk.level == RiskLevel.MEDIUM):
                Decision(
                    action=Action.EXECUTE_WITH_VALIDATION,
                    autonomous=True,
                    level=AutonomyLevel.VALIDATED,
                    requires_validation=True,
                    confidence=confidence.score
                ),
            
            # Confianza media + Bajo riesgo → Autónomo con validación
            (confidence.score > thresholds.validated, risk.level == RiskLevel.LOW):
                Decision(
                    action=Action.EXECUTE_WITH_VALIDATION,
                    autonomous=True,
                    level=AutonomyLevel.VALIDATED,
                    requires_validation=True,
                    confidence=confidence.score
                ),
            
            # Riesgo alto → Siempre escalar
            (risk.level >= RiskLevel.HIGH, True):
                Decision(
                    action=Action.ESCALATE_TO_HUMAN,
                    autonomous=False,
                    level=AutonomyLevel.NONE,
                    reason=f"High risk: {risk.factors}",
                    confidence=confidence.score
                ),
            
            # Confianza baja → Escalar
            (confidence.score < thresholds.minimum, True):
                Decision(
                    action=Action.ESCALATE_TO_HUMAN,
                    autonomous=False,
                    level=AutonomyLevel.NONE,
                    reason=f"Low confidence: {confidence.score:.2f}",
                    confidence=confidence.score
                )
        }
        
        # Aplicar matriz
        for condition, decision in decision_matrix.items():
            if self.evaluate_condition(condition, confidence, risk):
                return decision
        
        # Default: Escalar
        return Decision(
            action=Action.ESCALATE_TO_HUMAN,
            autonomous=False,
            level=AutonomyLevel.NONE,
            reason="Default: insufficient confidence or high risk",
            confidence=confidence.score
        )
```

### Ejecución Autónoma

```python
class AutonomousExecutor:
    async def execute(
        self,
        decision: Decision,
        situation: Situation
    ) -> ActionResult:
        """
        Ejecuta acción de forma autónoma.
        """
        # Log de decisión
        await self.log_decision(decision, situation)
        
        # Ejecutar según tipo de acción
        if decision.action == Action.EXECUTE_AUTONOMOUSLY:
            result = await self.execute_fully_autonomous(situation)
        elif decision.action == Action.EXECUTE_WITH_VALIDATION:
            result = await self.execute_with_validation(situation)
        else:
            raise ValueError(f"Invalid action: {decision.action}")
        
        # Validar resultado
        validation = await self.validate_result(result, situation)
        
        if not validation.passed:
            # Si falla validación, escalar
            return await self.handle_validation_failure(
                result, validation, situation
            )
        
        # Registrar éxito
        await self.record_success(decision, situation, result)
        
        return ActionResult(
            success=True,
            result=result,
            autonomous=True,
            decision=decision
        )
```

### Sistema de Aprendizaje

```python
class LearningEngine:
    async def learn(
        self,
        situation: Situation,
        decision: Decision,
        result: ActionResult
    ) -> None:
        """
        Aprende de cada decisión y resultado.
        """
        # Almacenar en historial
        await self.history.store(
            situation=situation,
            decision=decision,
            result=result
        )
        
        # Actualizar métricas de agentes
        if result.success:
            await self.update_agent_metrics(
                situation.agents,
                positive=True
            )
        else:
            await self.update_agent_metrics(
                situation.agents,
                positive=False
            )
        
        # Ajustar umbrales adaptativos
        if result.success and decision.autonomous:
            # Si fue exitoso, podemos ser más autónomos en el futuro
            await self.adjust_thresholds(
                direction="increase_autonomy",
                factor=0.01  # Aumento pequeño
            )
        elif not result.success and decision.autonomous:
            # Si falló, ser más conservador
            await self.adjust_thresholds(
                direction="decrease_autonomy",
                factor=0.05  # Disminución mayor
            )
    
    async def adjust_thresholds(
        self,
        direction: str,
        factor: float
    ) -> None:
        """
        Ajusta umbrales adaptativamente.
        """
        if direction == "increase_autonomy":
            self.thresholds.autonomous = max(
                0.5,  # Mínimo
                self.thresholds.autonomous - factor
            )
        else:
            self.thresholds.autonomous = min(
                0.95,  # Máximo
                self.thresholds.autonomous + factor
            )
```

## Umbrales Adaptativos

```python
@dataclass
class AdaptiveThresholds:
    """
    Umbrales que se ajustan según performance.
    """
    autonomous: float = 0.8      # Confianza mínima para acción autónoma
    validated: float = 0.7        # Confianza mínima para acción con validación
    minimum: float = 0.5          # Confianza mínima para cualquier acción
    risk_high: float = 0.6        # Riesgo máximo para acción autónoma
    risk_medium: float = 0.4      # Riesgo máximo para acción con validación
    
    def adjust_based_on_performance(
        self,
        success_rate: float,
        recent_decisions: List[Decision]
    ) -> None:
        """
        Ajusta umbrales basándose en performance reciente.
        """
        if success_rate > 0.9:
            # Muy exitoso → Puede ser más autónomo
            self.autonomous = max(0.7, self.autonomous - 0.05)
        elif success_rate < 0.7:
            # Poco exitoso → Ser más conservador
            self.autonomous = min(0.9, self.autonomous + 0.1)
```

## Ejemplos de Decisión Autónoma

### Ejemplo 1: Tarea Simple de Baja Confianza

```python
situation = Situation(
    task=Task(
        type="research",
        description="Buscar información sobre X",
        complexity="low"
    ),
    agents=[Researcher],
    context={"project": "test"}
)

# Análisis
confidence = 0.85  # Alta confianza
risk = RiskLevel.LOW  # Bajo riesgo
rules_check = RulesCheck(passed=True)

# Decisión
decision = Decision(
    action=Action.EXECUTE_AUTONOMOUSLY,
    autonomous=True,
    level=AutonomyLevel.FULL
)

# El DT actúa sin consultar
```

### Ejemplo 2: Tarea Compleja de Riesgo Medio

```python
situation = Situation(
    task=Task(
        type="marketing_strategy",
        description="Crear estrategia de marketing para Q1",
        complexity="high"
    ),
    agents=[MarketingStrategist, BrandGuardian],
    context={"budget": 100000}
)

# Análisis
confidence = 0.75  # Confianza media-alta
risk = RiskLevel.MEDIUM  # Riesgo medio
rules_check = RulesCheck(passed=True)

# Decisión
decision = Decision(
    action=Action.EXECUTE_WITH_VALIDATION,
    autonomous=True,
    level=AutonomyLevel.VALIDATED,
    requires_validation=True
)

# El DT actúa pero valida resultado antes de aprobar
```

### Ejemplo 3: Tarea Crítica de Alto Riesgo

```python
situation = Situation(
    task=Task(
        type="brand_change",
        description="Cambiar identidad visual de marca",
        complexity="high"
    ),
    agents=[BrandGuardian, UI Designer],
    context={"impact": "major"}
)

# Análisis
confidence = 0.65  # Confianza media
risk = RiskLevel.HIGH  # Alto riesgo
rules_check = RulesCheck(passed=True)

# Decisión
decision = Decision(
    action=Action.ESCALATE_TO_HUMAN,
    autonomous=False,
    level=AutonomyLevel.NONE,
    reason="High risk: major brand change"
)

# El DT NO actúa, escala a humano
```

## Configuración de Autonomía

```yaml
dt:
  autonomy:
    enabled: true
    default_level: "validated"  # full | validated | consult | none
    
    thresholds:
      autonomous: 0.8
      validated: 0.7
      minimum: 0.5
    
    risk_limits:
      autonomous_max: 0.3
      validated_max: 0.5
    
    learning:
      enabled: true
      adjustment_rate: 0.01
      min_threshold: 0.5
      max_threshold: 0.95
    
    always_escalate:
      - "major_brand_changes"
      - "legal_decisions"
      - "budget_over_100k"
      - "data_deletion"
    
    always_autonomous:
      - "simple_research"
      - "content_formatting"
      - "task_status_updates"
```

## Logging y Auditoría

```python
class DecisionLogger:
    async def log_decision(
        self,
        decision: Decision,
        situation: Situation,
        result: Optional[ActionResult] = None
    ) -> None:
        """
        Registra todas las decisiones para auditoría.
        """
        log_entry = DecisionLog(
            timestamp=datetime.now(),
            situation_id=situation.id,
            decision=decision,
            confidence=decision.confidence,
            risk=decision.risk,
            autonomous=decision.autonomous,
            result=result,
            reasoning=decision.reasoning
        )
        
        await self.store(log_entry)
```

## Métricas de Autonomía

```python
@dataclass
class AutonomyMetrics:
    total_decisions: int
    autonomous_decisions: int
    validated_decisions: int
    escalated_decisions: int
    success_rate_autonomous: float
    success_rate_validated: float
    average_confidence: float
    average_risk: float
    threshold_adjustments: int
```

## Próximos Pasos

1. **Implementar DTAutonomyEngine** completo
2. **Crear sistema de confianza** robusto
3. **Implementar evaluación de riesgo** detallada
4. **Sistema de aprendizaje** básico
5. **Logging y auditoría** completo
6. **Tests** de autonomía

---

**Última actualización**: Enero 2025  
**Estado**: Especificación Detallada
