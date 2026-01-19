"""Budget alerts for cost management."""

from typing import Callable, List, Optional


class BudgetAlerts:
    """
    Manages budget alerts and notifications.
    
    Triggers alerts when budget thresholds are exceeded.
    """

    def __init__(
        self,
        budget: float,
        warning_threshold: float = 0.8,  # Warn at 80% of budget
    ):
        """
        Initialize BudgetAlerts.

        Args:
            budget: Total budget limit
            warning_threshold: Warning threshold (0.0 - 1.0)
        """
        self.budget = budget
        self.warning_threshold = warning_threshold
        self.warning_sent = False
        self.alert_sent = False
        self.alert_handlers: List[Callable[[float, float], None]] = []

    def register_handler(self, handler: Callable[[float, float], None]) -> None:
        """
        Register an alert handler.

        Args:
            handler: Function that takes (current_cost, budget) as arguments
        """
        self.alert_handlers.append(handler)

    def trigger_alert(self, current_cost: float, budget: float) -> None:
        """
        Trigger budget alert.

        Args:
            current_cost: Current total cost
            budget: Budget limit
        """
        if current_cost >= budget:
            if not self.alert_sent:
                self.alert_sent = True
                for handler in self.alert_handlers:
                    handler(current_cost, budget)
        elif current_cost >= budget * self.warning_threshold:
            if not self.warning_sent:
                self.warning_sent = True
                for handler in self.alert_handlers:
                    handler(current_cost, budget)

    def reset(self) -> None:
        """Reset alert state."""
        self.warning_sent = False
        self.alert_sent = False
