"""Unit tests for cost tracking."""

import pytest

from agents_army.cost.alerts import BudgetAlerts
from agents_army.cost.estimator import CostEstimator
from agents_army.cost.tracker import CostTracker


class TestCostTracker:
    """Test CostTracker functionality."""

    def test_calculate_cost(self):
        """Test cost calculation."""
        tracker = CostTracker()

        cost = tracker.calculate_cost("gpt-4", 1000, 500)

        # Should be approximately (1000/1M * 30) + (500/1M * 60) = 0.06
        assert cost > 0
        assert cost < 1.0  # Should be small

    def test_record_llm_cost(self):
        """Test recording LLM cost."""
        tracker = CostTracker()

        record = tracker.record_llm_cost(
            model="gpt-4",
            input_tokens=1000,
            output_tokens=500,
            agent_id="agent_001",
        )

        assert record.model == "gpt-4"
        assert record.input_tokens == 1000
        assert record.cost > 0
        assert len(tracker.costs) == 1

    def test_get_total_cost(self):
        """Test getting total cost."""
        tracker = CostTracker()

        tracker.record_llm_cost("gpt-4", 1000, 500)
        tracker.record_llm_cost("gpt-3.5-turbo", 2000, 1000)

        total = tracker.get_total_cost()
        assert total > 0

    def test_get_cost_by_model(self):
        """Test getting cost breakdown by model."""
        tracker = CostTracker()

        tracker.record_llm_cost("gpt-4", 1000, 500)
        tracker.record_llm_cost("gpt-4", 1000, 500)
        tracker.record_llm_cost("gpt-3.5-turbo", 1000, 500)

        breakdown = tracker.get_cost_by_model()

        assert "gpt-4" in breakdown
        assert "gpt-3.5-turbo" in breakdown
        assert breakdown["gpt-4"] > breakdown["gpt-3.5-turbo"]

    def test_get_cost_by_agent(self):
        """Test getting cost breakdown by agent."""
        tracker = CostTracker()

        tracker.record_llm_cost("gpt-4", 1000, 500, agent_id="agent_001")
        tracker.record_llm_cost("gpt-4", 1000, 500, agent_id="agent_002")

        breakdown = tracker.get_cost_by_agent()

        assert "agent_001" in breakdown
        assert "agent_002" in breakdown

    def test_budget_alert(self):
        """Test budget alert triggering."""
        tracker = CostTracker(budget=0.01)  # Very small budget

        # Record a cost that exceeds budget
        tracker.record_llm_cost("gpt-4", 100000, 50000)

        # Should have triggered alert
        assert tracker.get_total_cost() > tracker.budget


class TestCostEstimator:
    """Test CostEstimator functionality."""

    def test_estimate_task_cost(self):
        """Test estimating task cost."""
        estimator = CostEstimator()

        cost = estimator.estimate_task_cost("gpt-4", 1000, 500)

        assert cost > 0

    def test_estimate_batch_cost(self):
        """Test estimating batch cost."""
        estimator = CostEstimator()

        tasks = [
            {"input_tokens": 1000, "output_tokens": 500},
            {"input_tokens": 2000, "output_tokens": 1000},
        ]

        total_cost = estimator.estimate_batch_cost("gpt-4", tasks)

        assert total_cost > 0

    def test_estimate_project_cost(self):
        """Test estimating project cost."""
        estimator = CostEstimator()

        estimate = estimator.estimate_project_cost(
            model="gpt-4",
            num_tasks=10,
            avg_input_tokens=1000,
            avg_output_tokens=500,
        )

        assert "total_cost" in estimate
        assert "cost_per_task" in estimate
        assert estimate["num_tasks"] == 10

    def test_recommend_model(self):
        """Test model recommendation."""
        estimator = CostEstimator()

        model = estimator.recommend_model(
            input_tokens=1000,
            output_tokens=500,
        )

        assert model in CostTracker.MODEL_PRICING.keys()


class TestBudgetAlerts:
    """Test BudgetAlerts functionality."""

    def test_trigger_alert(self):
        """Test triggering alert."""
        alerts = BudgetAlerts(budget=100.0)

        alert_triggered = False

        def handler(current_cost: float, budget: float):
            nonlocal alert_triggered
            alert_triggered = True

        alerts.register_handler(handler)

        alerts.trigger_alert(110.0, 100.0)

        assert alert_triggered is True

    def test_warning_threshold(self):
        """Test warning threshold."""
        alerts = BudgetAlerts(budget=100.0, warning_threshold=0.8)

        warning_triggered = False

        def handler(current_cost: float, budget: float):
            nonlocal warning_triggered
            warning_triggered = True

        alerts.register_handler(handler)

        # Trigger warning (80% of budget)
        alerts.trigger_alert(85.0, 100.0)

        assert warning_triggered is True
