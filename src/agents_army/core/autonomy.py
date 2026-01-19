"""DTAutonomyEngine - Autonomous decision making for El DT."""

from typing import Any, Dict, List, Optional

from agents_army.core.models import (
    ActionResult,
    ConfidenceScore,
    Decision,
    RiskAssessment,
    Situation,
    SituationAnalysis,
    Task,
)
from agents_army.core.rules import RulesLoader
from agents_army.protocol.types import AgentRole


class ConfidenceCalculator:
    """Calculates confidence scores for autonomous decisions."""

    def calculate(
        self,
        situation: Situation,
        analysis: SituationAnalysis,
        history: List[Dict[str, Any]],
    ) -> ConfidenceScore:
        """
        Calculate confidence score (0-1) based on multiple factors.

        Args:
            situation: Current situation
            analysis: Situation analysis
            history: Historical decisions

        Returns:
            ConfidenceScore
        """
        factors = {
            "historical_success": self._calculate_historical_success(history, situation),
            "agent_reliability": self._calculate_agent_reliability(
                analysis.agents_available
            ),
            "complexity_factor": self._complexity_to_confidence(analysis.complexity),
            "task_clarity": self._assess_task_clarity(situation.task),
            "resource_availability": self._assess_resources(
                analysis.resources_required
            ),
            "context_quality": self._assess_context_quality(analysis.context),
        }

        weights = {
            "historical_success": 0.3,
            "agent_reliability": 0.25,
            "complexity_factor": 0.15,
            "task_clarity": 0.1,
            "resource_availability": 0.1,
            "context_quality": 0.1,
        }

        confidence = sum(factors[key] * weights[key] for key in factors)

        return ConfidenceScore(
            score=min(max(confidence, 0.0), 1.0),
            factors=factors,
            explanation=self._generate_explanation(factors, weights),
        )

    def _calculate_historical_success(
        self, history: List[Dict[str, Any]], situation: Situation
    ) -> float:
        """Calculate historical success rate for similar situations."""
        if not history:
            return 0.5  # Default if no history

        similar = [
            h
            for h in history
            if h.get("task_type") == situation.task.title[:20]  # Simple similarity
        ]
        if not similar:
            return 0.5

        successful = sum(1 for h in similar if h.get("success", False))
        return successful / len(similar) if similar else 0.5

    def _calculate_agent_reliability(self, agents: List[AgentRole]) -> float:
        """Calculate reliability of available agents."""
        if not agents:
            return 0.3

        # Simple reliability scoring (can be enhanced with actual metrics)
        reliability_scores = {
            AgentRole.DT: 0.9,
            AgentRole.BACKEND_ARCHITECT: 0.85,
            AgentRole.RESEARCHER: 0.8,
            AgentRole.MARKETING_STRATEGIST: 0.8,
            AgentRole.QA_TESTER: 0.85,
        }

        scores = [
            reliability_scores.get(agent, 0.7) for agent in agents
        ]
        return sum(scores) / len(scores) if scores else 0.5

    def _complexity_to_confidence(self, complexity: str) -> float:
        """Convert complexity to confidence factor."""
        complexity_map = {"low": 0.9, "medium": 0.6, "high": 0.3}
        return complexity_map.get(complexity.lower(), 0.5)

    def _assess_task_clarity(self, task: Task) -> float:
        """Assess task clarity."""
        # Simple heuristic: longer description = clearer
        desc_length = len(task.description)
        if desc_length > 200:
            return 0.9
        elif desc_length > 100:
            return 0.7
        elif desc_length > 50:
            return 0.5
        else:
            return 0.3

    def _assess_resources(self, resources: Dict[str, Any]) -> float:
        """Assess resource availability."""
        # Simple check: if resources dict is empty, assume available
        return 0.8 if not resources else 0.6

    def _assess_context_quality(self, context: Dict[str, Any]) -> float:
        """Assess quality of available context."""
        # More context = higher quality
        return min(len(context) / 10.0, 1.0) if context else 0.3

    def _generate_explanation(
        self, factors: Dict[str, float], weights: Dict[str, float]
    ) -> str:
        """Generate explanation for confidence score."""
        top_factors = sorted(
            factors.items(), key=lambda x: x[1] * weights.get(x[0], 0), reverse=True
        )[:3]
        return f"Confidence based on: {', '.join([f'{k}={v:.2f}' for k, v in top_factors])}"


class RiskAssessor:
    """Assesses risk for autonomous decisions."""

    def assess(
        self, situation: Situation, analysis: SituationAnalysis
    ) -> RiskAssessment:
        """
        Assess risk of acting autonomously.

        Args:
            situation: Current situation
            analysis: Situation analysis

        Returns:
            RiskAssessment
        """
        risk_factors = {
            "business_impact": self._assess_business_impact(situation),
            "technical_risk": self._assess_technical_risk(analysis),
            "data_risk": self._assess_data_risk(situation),
            "brand_risk": self._assess_brand_risk(situation),
            "financial_risk": self._assess_financial_risk(situation),
            "legal_risk": self._assess_legal_risk(situation),
        }

        total_risk = max(risk_factors.values())  # Use maximum (worst case)

        level = "low"
        if total_risk >= 0.8:
            level = "critical"
        elif total_risk >= 0.6:
            level = "high"
        elif total_risk >= 0.4:
            level = "medium"

        return RiskAssessment(
            total_risk=total_risk,
            risk_factors=risk_factors,
            level=level,
            explanation=self._generate_risk_explanation(risk_factors, total_risk),
        )

    def _assess_business_impact(self, situation: Situation) -> float:
        """Assess business impact risk."""
        # High priority tasks = higher business impact
        priority_map = {5: 0.8, 4: 0.6, 3: 0.4, 2: 0.2, 1: 0.1}
        return priority_map.get(situation.task.priority, 0.3)

    def _assess_technical_risk(self, analysis: SituationAnalysis) -> float:
        """Assess technical risk."""
        complexity_map = {"high": 0.7, "medium": 0.4, "low": 0.2}
        return complexity_map.get(analysis.complexity.lower(), 0.3)

    def _assess_data_risk(self, situation: Situation) -> float:
        """Assess data risk."""
        # Check if task involves sensitive data
        sensitive_keywords = ["password", "token", "key", "secret", "personal"]
        desc_lower = situation.task.description.lower()
        if any(kw in desc_lower for kw in sensitive_keywords):
            return 0.8
        return 0.2

    def _assess_brand_risk(self, situation: Situation) -> float:
        """Assess brand risk."""
        # Marketing-related tasks have higher brand risk
        marketing_tags = ["marketing", "brand", "content", "social"]
        if any(tag in situation.task.tags for tag in marketing_tags):
            return 0.6
        return 0.2

    def _assess_financial_risk(self, situation: Situation) -> float:
        """Assess financial risk."""
        # Check metadata for financial indicators
        if situation.task.metadata.get("cost", 0) > 1000:
            return 0.7
        return 0.2

    def _assess_legal_risk(self, situation: Situation) -> float:
        """Assess legal risk."""
        legal_keywords = ["legal", "compliance", "gdpr", "privacy", "terms"]
        desc_lower = situation.task.description.lower()
        if any(kw in desc_lower for kw in legal_keywords):
            return 0.8
        return 0.1

    def _generate_risk_explanation(
        self, risk_factors: Dict[str, float], total_risk: float
    ) -> str:
        """Generate explanation for risk assessment."""
        top_risks = sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)[:3]
        return f"Risk level: {total_risk:.2f}. Top risks: {', '.join([f'{k}={v:.2f}' for k, v in top_risks])}"


class DecisionHistory:
    """Stores and retrieves decision history."""

    def __init__(self):
        """Initialize decision history."""
        self.history: List[Dict[str, Any]] = []

    def add_decision(
        self,
        situation: Situation,
        decision: Decision,
        result: ActionResult,
    ) -> None:
        """Add a decision to history."""
        self.history.append(
            {
                "task_type": situation.task.title,
                "task_id": situation.task.id,
                "decision": decision.action,
                "autonomous": decision.autonomous,
                "success": result.success,
                "confidence": decision.confidence,
                "risk": decision.risk,
                "timestamp": situation.task.created_at.isoformat(),
            }
        )

    def find_similar(self, situation: Situation) -> List[Dict[str, Any]]:
        """Find similar decisions in history."""
        # Simple similarity: same task title prefix
        prefix = situation.task.title[:20]
        return [
            h
            for h in self.history
            if h.get("task_type", "").startswith(prefix)
        ]


class DTAutonomyEngine:
    """
    Engine that enables El DT to make autonomous decisions and act.

    Based on rules, confidence scores, risk assessment, and learning.
    """

    def __init__(
        self,
        rules_loader: RulesLoader,
        history: Optional[DecisionHistory] = None,
    ):
        """
        Initialize DTAutonomyEngine.

        Args:
            rules_loader: Rules loader for checking rules
            history: Optional decision history
        """
        self.rules_loader = rules_loader
        self.history = history or DecisionHistory()
        self.confidence_calculator = ConfidenceCalculator()
        self.risk_assessor = RiskAssessor()
        self.adaptive_thresholds = {
            "confidence_min": 0.7,
            "risk_max": 0.5,
            "autonomy_level_4": {"confidence": 0.9, "risk": 0.2},
            "autonomy_level_3": {"confidence": 0.8, "risk": 0.4},
            "autonomy_level_2": {"confidence": 0.6, "risk": 0.6},
        }

    async def decide_and_act(
        self, situation: Situation
    ) -> ActionResult:
        """
        Complete process of decision and autonomous action.

        Flow:
        1. Analyze situation
        2. Calculate confidence
        3. Assess risk
        4. Consult history
        5. Apply rules
        6. Decide autonomy level
        7. Execute action
        8. Learn from result

        Args:
            situation: Situation requiring decision

        Returns:
            ActionResult
        """
        # 1. Analyze situation
        analysis = await self._analyze_situation(situation)

        # 2. Calculate confidence
        similar_decisions = self.history.find_similar(situation)
        confidence = self.confidence_calculator.calculate(
            situation, analysis, similar_decisions
        )

        # 3. Assess risk
        risk = self.risk_assessor.assess(situation, analysis)

        # 4. Apply rules
        rules_check = self._check_rules(situation, analysis)

        # 5. Make decision
        decision = self._make_decision(confidence, risk, rules_check, analysis)

        # 6. Execute or escalate
        if decision.autonomous:
            result = await self._execute_autonomously(situation, decision)
            # 7. Learn from result
            await self._learn_from_result(situation, decision, result)
            return result
        else:
            return await self._escalate_to_human(situation, decision)

    async def _analyze_situation(
        self, situation: Situation
    ) -> SituationAnalysis:
        """Analyze the situation."""
        complexity = self._assess_complexity(situation.task)
        dependencies = situation.task.dependencies.copy()

        return SituationAnalysis(
            task_type=situation.task.title,
            complexity=complexity,
            agents_available=situation.available_agents,
            dependencies=dependencies,
            resources_required={},
            time_available=None,
            context=situation.context,
        )

    def _assess_complexity(self, task: Task) -> str:
        """Assess task complexity."""
        desc_length = len(task.description)
        dep_count = len(task.dependencies)

        if desc_length > 500 or dep_count > 3:
            return "high"
        elif desc_length > 200 or dep_count > 1:
            return "medium"
        else:
            return "low"

    def _check_rules(
        self, situation: Situation, analysis: SituationAnalysis
    ) -> Dict[str, Any]:
        """Check rules for this situation."""
        # Simple rule check (can be enhanced with actual RulesChecker)
        return {
            "allowed": True,
            "restrictions": [],
            "mandatory_approval": False,
        }

    def _make_decision(
        self,
        confidence: ConfidenceScore,
        risk: RiskAssessment,
        rules_check: Dict[str, Any],
        analysis: SituationAnalysis,
    ) -> Decision:
        """Make decision about autonomy level."""
        if not rules_check.get("allowed", True):
            return Decision(
                autonomous=False,
                confidence=confidence.score,
                risk=risk.total_risk,
                action="blocked",
                reasoning="Rules do not allow this action",
                escalation_reason="Rule violation",
                level=1,
            )

        # Determine autonomy level based on thresholds
        if (
            confidence.score >= self.adaptive_thresholds["autonomy_level_4"]["confidence"]
            and risk.total_risk <= self.adaptive_thresholds["autonomy_level_4"]["risk"]
        ):
            level = 4
            autonomous = True
            action = "execute_autonomously"
            reasoning = "High confidence, low risk - fully autonomous"
        elif (
            confidence.score >= self.adaptive_thresholds["autonomy_level_3"]["confidence"]
            and risk.total_risk <= self.adaptive_thresholds["autonomy_level_3"]["risk"]
        ):
            level = 3
            autonomous = True
            action = "execute_with_validation"
            reasoning = "Good confidence, moderate risk - autonomous with validation"
        elif (
            confidence.score >= self.adaptive_thresholds["autonomy_level_2"]["confidence"]
            and risk.total_risk <= self.adaptive_thresholds["autonomy_level_2"]["risk"]
        ):
            level = 2
            autonomous = False
            action = "recommend_action"
            reasoning = "Moderate confidence - recommend action"
            escalation_reason = "Confidence below threshold"
        else:
            level = 1
            autonomous = False
            action = "escalate"
            reasoning = "Low confidence or high risk - escalate to human"
            escalation_reason = (
                f"Confidence: {confidence.score:.2f}, Risk: {risk.total_risk:.2f}"
            )

        return Decision(
            autonomous=autonomous,
            confidence=confidence.score,
            risk=risk.total_risk,
            action=action,
            reasoning=reasoning,
            escalation_reason=escalation_reason,
            level=level,
        )

    async def _execute_autonomously(
        self, situation: Situation, decision: Decision
    ) -> ActionResult:
        """Execute autonomous action."""
        # This would typically delegate to El DT's actual execution methods
        # For now, return a success result
        return ActionResult(
            success=True,
            action_taken=decision.action,
            result={"task_id": situation.task.id, "decision": decision.action},
            escalated=False,
        )

    async def _escalate_to_human(
        self, situation: Situation, decision: Decision
    ) -> ActionResult:
        """Escalate to human."""
        return ActionResult(
            success=False,
            action_taken="escalated",
            result={"task_id": situation.task.id},
            escalated=True,
            escalation_reason=decision.escalation_reason or "Low confidence or high risk",
        )

    async def _learn_from_result(
        self,
        situation: Situation,
        decision: Decision,
        result: ActionResult,
    ) -> None:
        """Learn from decision result and adjust thresholds."""
        # Add to history
        self.history.add_decision(situation, decision, result)

        # Simple learning: adjust thresholds based on success rate
        if result.success:
            # Successful autonomous action - can be slightly more aggressive
            if decision.level == 4:
                # Already at max autonomy, no change needed
                pass
            elif decision.confidence > 0.8:
                # High confidence success - can lower threshold slightly
                self.adaptive_thresholds["autonomy_level_4"]["confidence"] = max(
                    0.85, self.adaptive_thresholds["autonomy_level_4"]["confidence"] - 0.02
                )
        else:
            # Failed autonomous action - be more conservative
            if decision.level >= 3:
                # Increase threshold for level 3 and 4
                self.adaptive_thresholds["autonomy_level_3"]["confidence"] = min(
                    0.95, self.adaptive_thresholds["autonomy_level_3"]["confidence"] + 0.02
                )
                self.adaptive_thresholds["autonomy_level_4"]["confidence"] = min(
                    0.95, self.adaptive_thresholds["autonomy_level_4"]["confidence"] + 0.02
                )

    def calculate_confidence(
        self, situation: Situation, analysis: SituationAnalysis
    ) -> ConfidenceScore:
        """
        Calculate confidence score.

        Args:
            situation: Current situation
            analysis: Situation analysis

        Returns:
            ConfidenceScore
        """
        similar_decisions = self.history.find_similar(situation)
        return self.confidence_calculator.calculate(
            situation, analysis, similar_decisions
        )

    def assess_risk(
        self, situation: Situation, analysis: SituationAnalysis
    ) -> RiskAssessment:
        """
        Assess risk.

        Args:
            situation: Current situation
            analysis: Situation analysis

        Returns:
            RiskAssessment
        """
        return self.risk_assessor.assess(situation, analysis)

    def make_decision(
        self,
        confidence: ConfidenceScore,
        risk: RiskAssessment,
        rules_check: Dict[str, Any],
        analysis: SituationAnalysis,
    ) -> Decision:
        """
        Make decision about autonomy.

        Args:
            confidence: Confidence score
            risk: Risk assessment
            rules_check: Rules check result
            analysis: Situation analysis

        Returns:
            Decision
        """
        return self._make_decision(confidence, risk, rules_check, analysis)

    async def execute_autonomously(
        self, situation: Situation, decision: Decision
    ) -> ActionResult:
        """
        Execute autonomous action.

        Args:
            situation: Current situation
            decision: Decision to execute

        Returns:
            ActionResult
        """
        return await self._execute_autonomously(situation, decision)


class LearningEngine:
    """Learning engine for adaptive threshold adjustment."""

    def __init__(self):
        """Initialize learning engine."""
        self.success_history: List[bool] = []
        self.decision_history: List[Dict[str, Any]] = []

    def record_decision(
        self,
        decision: Decision,
        result: ActionResult,
    ) -> None:
        """Record a decision and its result."""
        self.decision_history.append(
            {
                "decision": decision.action,
                "autonomous": decision.autonomous,
                "confidence": decision.confidence,
                "risk": decision.risk,
                "level": decision.level,
                "success": result.success,
            }
        )
        self.success_history.append(result.success)

    def adjust_thresholds(
        self, current_thresholds: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adjust thresholds based on learning.

        Args:
            current_thresholds: Current threshold configuration

        Returns:
            Adjusted thresholds
        """
        if len(self.success_history) < 10:
            return current_thresholds  # Not enough data

        recent_success_rate = sum(self.success_history[-20:]) / len(
            self.success_history[-20:]
        )

        adjusted = current_thresholds.copy()

        if recent_success_rate > 0.9:
            # High success rate - can be more aggressive
            adjusted["autonomy_level_4"]["confidence"] = max(
                0.85, adjusted["autonomy_level_4"]["confidence"] - 0.05
            )
            adjusted["autonomy_level_3"]["confidence"] = max(
                0.75, adjusted["autonomy_level_3"]["confidence"] - 0.05
            )
        elif recent_success_rate < 0.7:
            # Low success rate - be more conservative
            adjusted["autonomy_level_4"]["confidence"] = min(
                0.95, adjusted["autonomy_level_4"]["confidence"] + 0.05
            )
            adjusted["autonomy_level_3"]["confidence"] = min(
                0.90, adjusted["autonomy_level_3"]["confidence"] + 0.05
            )

        return adjusted

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics."""
        if not self.success_history:
            return {"total_decisions": 0, "success_rate": 0.0}

        return {
            "total_decisions": len(self.success_history),
            "success_rate": sum(self.success_history) / len(self.success_history),
            "recent_success_rate": (
                sum(self.success_history[-20:]) / len(self.success_history[-20:])
                if len(self.success_history) >= 20
                else sum(self.success_history) / len(self.success_history)
            ),
        }
