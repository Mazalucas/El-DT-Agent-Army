"""Metrics collection for Agents_Army."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class MetricsCollector:
    """
    Collects and aggregates metrics from agents and system.

    Tracks LLM calls, task execution, agent performance, and system health.
    """

    def __init__(self):
        """Initialize MetricsCollector."""
        self.metrics: Dict[str, Any] = defaultdict(lambda: {"count": 0, "total": 0.0})
        self.llm_calls: List[Dict[str, Any]] = []
        self.task_events: List[Dict[str, Any]] = []
        self.agent_actions: List[Dict[str, Any]] = []
        self.start_time = datetime.now()

    def record_llm_call(
        self,
        agent_id: str,
        model: str,
        tokens: int,
        duration: float,
        success: bool = True,
    ) -> None:
        """
        Record an LLM call.

        Args:
            agent_id: Agent ID
            model: LLM model
            tokens: Tokens used (input + output)
            duration: Call duration in seconds
            success: Whether call succeeded
        """
        call_data = {
            "agent_id": agent_id,
            "model": model,
            "tokens": tokens,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now().isoformat(),
        }

        self.llm_calls.append(call_data)

        # Update aggregated metrics
        key = f"llm_calls.{model}"
        self.metrics[key]["count"] += 1
        self.metrics[key]["total"] += tokens

        self.metrics["llm_calls.total"]["count"] += 1
        self.metrics["llm_calls.total"]["total"] += tokens

        if success:
            self.metrics["llm_calls.success"]["count"] += 1
        else:
            self.metrics["llm_calls.failed"]["count"] += 1

    def record_task_event(
        self,
        task_id: str,
        event: str,
        agent_id: Optional[str] = None,
        duration: Optional[float] = None,
    ) -> None:
        """
        Record a task event.

        Args:
            task_id: Task ID
            event: Event type (created, assigned, completed, failed)
            agent_id: Optional agent ID
            duration: Optional task duration
        """
        event_data = {
            "task_id": task_id,
            "event": event,
            "agent_id": agent_id,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }

        self.task_events.append(event_data)

        # Update metrics
        key = f"tasks.{event}"
        self.metrics[key]["count"] += 1

        if duration:
            self.metrics[key]["total"] += duration

    def record_agent_action(
        self,
        agent_id: str,
        action: str,
        duration: Optional[float] = None,
    ) -> None:
        """
        Record an agent action.

        Args:
            agent_id: Agent ID
            action: Action performed
            duration: Optional action duration
        """
        action_data = {
            "agent_id": agent_id,
            "action": action,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }

        self.agent_actions.append(action_data)

        # Update metrics
        key = f"agent_actions.{action}"
        self.metrics[key]["count"] += 1

        if duration:
            self.metrics[key]["total"] += duration

    def get_metrics(self, time_window: Optional[timedelta] = None) -> Dict[str, Any]:
        """
        Get aggregated metrics.

        Args:
            time_window: Optional time window to filter metrics

        Returns:
            Dictionary of metrics
        """
        if time_window:
            cutoff = datetime.now() - time_window
            filtered_llm = [
                c for c in self.llm_calls if datetime.fromisoformat(c["timestamp"]) >= cutoff
            ]
            filtered_tasks = [
                t for t in self.task_events if datetime.fromisoformat(t["timestamp"]) >= cutoff
            ]
        else:
            filtered_llm = self.llm_calls
            filtered_tasks = self.task_events

        # Calculate statistics
        total_llm_calls = len(filtered_llm)
        successful_llm_calls = sum(1 for c in filtered_llm if c.get("success", True))
        total_tokens = sum(c.get("tokens", 0) for c in filtered_llm)
        avg_duration = (
            sum(c.get("duration", 0) for c in filtered_llm) / total_llm_calls
            if total_llm_calls > 0
            else 0
        )

        total_tasks = len(filtered_tasks)
        completed_tasks = sum(1 for t in filtered_tasks if t.get("event") == "completed")

        return {
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "llm_calls": {
                "total": total_llm_calls,
                "successful": successful_llm_calls,
                "failed": total_llm_calls - successful_llm_calls,
                "total_tokens": total_tokens,
                "avg_duration": avg_duration,
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "completion_rate": (completed_tasks / total_tasks if total_tasks > 0 else 0),
            },
            "agent_actions": {
                "total": len(self.agent_actions),
            },
            "raw_metrics": dict(self.metrics),
        }

    def get_agent_metrics(self, agent_id: str) -> Dict[str, Any]:
        """
        Get metrics for a specific agent.

        Args:
            agent_id: Agent ID

        Returns:
            Agent-specific metrics
        """
        agent_llm_calls = [c for c in self.llm_calls if c["agent_id"] == agent_id]
        agent_tasks = [t for t in self.task_events if t.get("agent_id") == agent_id]
        agent_actions = [a for a in self.agent_actions if a["agent_id"] == agent_id]

        return {
            "agent_id": agent_id,
            "llm_calls": len(agent_llm_calls),
            "tasks": len(agent_tasks),
            "actions": len(agent_actions),
            "total_tokens": sum(c.get("tokens", 0) for c in agent_llm_calls),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.llm_calls.clear()
        self.task_events.clear()
        self.agent_actions.clear()
        self.start_time = datetime.now()
