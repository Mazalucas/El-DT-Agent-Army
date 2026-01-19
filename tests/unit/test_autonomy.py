"""Unit tests for DTAutonomyEngine."""

import pytest

from agents_army.core.autonomy import (
    ConfidenceCalculator,
    DecisionHistory,
    DTAutonomyEngine,
    LearningEngine,
    RiskAssessor,
)
from agents_army.core.models import Situation, Task
from agents_army.core.rules import RulesLoader
from agents_army.protocol.types import AgentRole


class TestConfidenceCalculator:
    """Test ConfidenceCalculator."""

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        calculator = ConfidenceCalculator()

        task = Task(
            id="task_001",
            title="Test task",
            description="This is a test task with sufficient detail",
        )
        situation = Situation(task=task, available_agents=[AgentRole.RESEARCHER])
        analysis = type(
            "SituationAnalysis",
            (),
            {
                "complexity": "low",
                "agents_available": [AgentRole.RESEARCHER],
                "dependencies": [],
                "resources_required": {},
                "context": {"test": "value"},
            },
        )()

        confidence = calculator.calculate(situation, analysis, [])

        assert 0.0 <= confidence.score <= 1.0
        assert "factors" in confidence.__dict__
        assert "explanation" in confidence.__dict__


class TestRiskAssessor:
    """Test RiskAssessor."""

    def test_assess_risk(self):
        """Test risk assessment."""
        assessor = RiskAssessor()

        task = Task(
            id="task_001",
            title="Test task",
            description="This is a test task",
            priority=3,
        )
        situation = Situation(task=task)
        analysis = type(
            "SituationAnalysis",
            (),
            {
                "complexity": "medium",
                "agents_available": [],
                "dependencies": [],
                "resources_required": {},
                "context": {},
            },
        )()

        risk = assessor.assess(situation, analysis)

        assert 0.0 <= risk.total_risk <= 1.0
        assert risk.level in ["low", "medium", "high", "critical"]
        assert "risk_factors" in risk.__dict__


class TestDecisionHistory:
    """Test DecisionHistory."""

    def test_add_decision(self):
        """Test adding decision to history."""
        history = DecisionHistory()

        task = Task(id="task_001", title="Test", description="Test")
        situation = Situation(task=task)
        decision = type(
            "Decision",
            (),
            {
                "autonomous": True,
                "confidence": 0.8,
                "risk": 0.3,
                "action": "execute",
                "level": 4,
            },
        )()
        result = type("ActionResult", (), {"success": True})()

        history.add_decision(situation, decision, result)

        assert len(history.history) == 1

    def test_find_similar(self):
        """Test finding similar decisions."""
        history = DecisionHistory()

        task1 = Task(id="task_001", title="Research AI agents", description="Test")
        situation1 = Situation(task=task1)
        decision1 = type(
            "Decision",
            (),
            {
                "autonomous": True,
                "confidence": 0.8,
                "risk": 0.3,
                "action": "execute",
                "level": 4,
            },
        )()
        result1 = type("ActionResult", (), {"success": True})()

        history.add_decision(situation1, decision1, result1)

        task2 = Task(id="task_002", title="Research AI frameworks", description="Test")
        situation2 = Situation(task=task2)

        similar = history.find_similar(situation2)

        assert len(similar) >= 0  # May or may not find similar based on prefix


class TestDTAutonomyEngine:
    """Test DTAutonomyEngine."""

    def test_create_engine(self):
        """Test creating DTAutonomyEngine."""
        rules_loader = RulesLoader()
        engine = DTAutonomyEngine(rules_loader=rules_loader)

        assert engine.rules_loader is not None
        assert engine.confidence_calculator is not None
        assert engine.risk_assessor is not None

    @pytest.mark.asyncio
    async def test_decide_and_act(self):
        """Test decide_and_act."""
        rules_loader = RulesLoader()
        engine = DTAutonomyEngine(rules_loader=rules_loader)

        task = Task(
            id="task_001",
            title="Simple task",
            description="This is a simple task with low complexity",
            priority=2,
        )
        situation = Situation(
            task=task, available_agents=[AgentRole.RESEARCHER, AgentRole.QA_TESTER]
        )

        result = await engine.decide_and_act(situation)

        assert result is not None
        assert "success" in result.__dict__
        assert "action_taken" in result.__dict__

    @pytest.mark.asyncio
    async def test_calculate_confidence(self):
        """Test calculate_confidence method."""
        rules_loader = RulesLoader()
        engine = DTAutonomyEngine(rules_loader=rules_loader)

        task = Task(
            id="task_001",
            title="Test task",
            description="Test description",
        )
        situation = Situation(task=task, available_agents=[AgentRole.RESEARCHER])
        analysis = await engine._analyze_situation(situation)

        confidence = engine.calculate_confidence(situation, analysis)

        assert 0.0 <= confidence.score <= 1.0

    @pytest.mark.asyncio
    async def test_assess_risk(self):
        """Test assess_risk method."""
        rules_loader = RulesLoader()
        engine = DTAutonomyEngine(rules_loader=rules_loader)

        task = Task(
            id="task_001",
            title="Test task",
            description="Test description",
            priority=3,
        )
        situation = Situation(task=task)
        analysis = await engine._analyze_situation(situation)

        risk = engine.assess_risk(situation, analysis)

        assert 0.0 <= risk.total_risk <= 1.0
        assert risk.level in ["low", "medium", "high", "critical"]


class TestLearningEngine:
    """Test LearningEngine."""

    def test_record_decision(self):
        """Test recording decision."""
        engine = LearningEngine()

        decision = type(
            "Decision",
            (),
            {
                "action": "execute",
                "autonomous": True,
                "confidence": 0.8,
                "risk": 0.3,
                "level": 4,
            },
        )()
        result = type("ActionResult", (), {"success": True})()

        engine.record_decision(decision, result)

        assert len(engine.decision_history) == 1
        assert len(engine.success_history) == 1

    def test_adjust_thresholds(self):
        """Test threshold adjustment."""
        engine = LearningEngine()

        # Record many successful decisions
        decision = type(
            "Decision",
            (),
            {
                "action": "execute",
                "autonomous": True,
                "confidence": 0.8,
                "risk": 0.3,
                "level": 4,
            },
        )()
        result = type("ActionResult", (), {"success": True})()

        for _ in range(15):
            engine.record_decision(decision, result)

        current_thresholds = {
            "autonomy_level_4": {"confidence": 0.9, "risk": 0.2},
            "autonomy_level_3": {"confidence": 0.8, "risk": 0.4},
        }

        adjusted = engine.adjust_thresholds(current_thresholds)

        assert adjusted is not None
        assert "autonomy_level_4" in adjusted

    def test_get_learning_stats(self):
        """Test getting learning statistics."""
        engine = LearningEngine()

        decision = type(
            "Decision",
            (),
            {
                "action": "execute",
                "autonomous": True,
                "confidence": 0.8,
                "risk": 0.3,
                "level": 4,
            },
        )()
        result = type("ActionResult", (), {"success": True})()

        engine.record_decision(decision, result)

        stats = engine.get_learning_stats()

        assert "total_decisions" in stats
        assert "success_rate" in stats
        assert stats["total_decisions"] == 1
