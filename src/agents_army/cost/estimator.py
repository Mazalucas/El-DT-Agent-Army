"""Cost estimation for LLM usage."""

from typing import Dict, List, Optional

from agents_army.cost.tracker import CostTracker


class CostEstimator:
    """
    Estimates costs for planned LLM usage.

    Helps predict costs before execution.
    """

    def __init__(self, cost_tracker: Optional[CostTracker] = None):
        """
        Initialize CostEstimator.

        Args:
            cost_tracker: Optional cost tracker for historical data
        """
        self.cost_tracker = cost_tracker or CostTracker()

    def estimate_task_cost(
        self,
        model: str,
        estimated_input_tokens: int,
        estimated_output_tokens: int,
    ) -> float:
        """
        Estimate cost for a task.

        Args:
            model: Model to use
            estimated_input_tokens: Estimated input tokens
            estimated_output_tokens: Estimated output tokens

        Returns:
            Estimated cost in USD
        """
        return self.cost_tracker.calculate_cost(
            model, estimated_input_tokens, estimated_output_tokens
        )

    def estimate_batch_cost(
        self,
        model: str,
        tasks: List[Dict[str, int]],
    ) -> float:
        """
        Estimate cost for a batch of tasks.

        Args:
            model: Model to use
            tasks: List of tasks with input_tokens and output_tokens

        Returns:
            Total estimated cost
        """
        total_cost = 0.0
        for task in tasks:
            input_tokens = task.get("input_tokens", 0)
            output_tokens = task.get("output_tokens", 0)
            total_cost += self.cost_tracker.calculate_cost(model, input_tokens, output_tokens)
        return total_cost

    def estimate_project_cost(
        self,
        model: str,
        num_tasks: int,
        avg_input_tokens: int = 1000,
        avg_output_tokens: int = 500,
    ) -> Dict[str, float]:
        """
        Estimate cost for entire project.

        Args:
            model: Model to use
            num_tasks: Number of tasks
            avg_input_tokens: Average input tokens per task
            avg_output_tokens: Average output tokens per task

        Returns:
            Dictionary with cost breakdown
        """
        cost_per_task = self.cost_tracker.calculate_cost(model, avg_input_tokens, avg_output_tokens)
        total_cost = cost_per_task * num_tasks

        return {
            "cost_per_task": cost_per_task,
            "total_cost": total_cost,
            "num_tasks": num_tasks,
            "model": model,
        }

    def recommend_model(
        self,
        input_tokens: int,
        output_tokens: int,
        budget: Optional[float] = None,
    ) -> str:
        """
        Recommend model based on cost and budget.

        Args:
            input_tokens: Expected input tokens
            output_tokens: Expected output tokens
            budget: Optional budget constraint

        Returns:
            Recommended model name
        """
        best_model = None
        best_cost = float("inf")

        for model in CostTracker.MODEL_PRICING.keys():
            cost = self.cost_tracker.calculate_cost(model, input_tokens, output_tokens)

            if budget and cost > budget:
                continue

            if cost < best_cost:
                best_cost = cost
                best_model = model

        return best_model or "gpt-3.5-turbo"  # Default fallback
