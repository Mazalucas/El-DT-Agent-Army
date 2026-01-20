"""Cost tracking for LLM usage."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from agents_army.cost.alerts import BudgetAlerts


@dataclass
class CostRecord:
    """Record of a cost event."""

    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    agent_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, any] = field(default_factory=dict)


class CostTracker:
    """
    Tracks LLM costs and usage.

    Records cost per model, agent, and time period.
    """

    # Pricing per 1M tokens (approximate, update as needed)
    MODEL_PRICING = {
        "gpt-4": {"input": 30.0, "output": 60.0},  # $30/$60 per 1M tokens
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
    }

    def __init__(self, budget: Optional[float] = None):
        """
        Initialize CostTracker.

        Args:
            budget: Optional budget limit
        """
        self.costs: List[CostRecord] = []
        self.budget = budget
        self.alerts = BudgetAlerts(budget) if budget else None

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for LLM call.

        Args:
            model: Model name
            input_tokens: Input tokens
            output_tokens: Output tokens

        Returns:
            Cost in USD
        """
        pricing = self.MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def record_llm_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, any]] = None,
    ) -> CostRecord:
        """
        Record an LLM cost.

        Args:
            model: Model name
            input_tokens: Input tokens
            output_tokens: Output tokens
            agent_id: Optional agent ID
            metadata: Optional metadata

        Returns:
            Cost record
        """
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        record = CostRecord(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            agent_id=agent_id,
            metadata=metadata or {},
        )

        self.costs.append(record)

        # Check budget
        if self.budget and self.get_total_cost() > self.budget:
            if self.alerts:
                self.alerts.trigger_alert(self.get_total_cost(), self.budget)

        return record

    def get_total_cost(self) -> float:
        """
        Get total cost.

        Returns:
            Total cost in USD
        """
        return sum(record.cost for record in self.costs)

    def get_cost_by_model(self) -> Dict[str, float]:
        """
        Get cost breakdown by model.

        Returns:
            Dictionary mapping model to total cost
        """
        breakdown: Dict[str, float] = {}
        for record in self.costs:
            breakdown[record.model] = breakdown.get(record.model, 0.0) + record.cost
        return breakdown

    def get_cost_by_agent(self) -> Dict[str, float]:
        """
        Get cost breakdown by agent.

        Returns:
            Dictionary mapping agent_id to total cost
        """
        breakdown: Dict[str, float] = {}
        for record in self.costs:
            if record.agent_id:
                breakdown[record.agent_id] = breakdown.get(record.agent_id, 0.0) + record.cost
        return breakdown

    def get_recent_costs(self, hours: int = 24) -> List[CostRecord]:
        """
        Get costs from recent time period.

        Args:
            hours: Number of hours to look back

        Returns:
            List of cost records
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        return [record for record in self.costs if record.timestamp >= cutoff]

    def reset(self) -> None:
        """Reset all cost records."""
        self.costs.clear()
