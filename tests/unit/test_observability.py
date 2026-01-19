"""Unit tests for observability components."""

import pytest

from agents_army.observability.logging import StructuredLogger
from agents_army.observability.metrics import MetricsCollector


class TestStructuredLogger:
    """Test StructuredLogger functionality."""

    def test_create_logger(self):
        """Test creating logger."""
        logger = StructuredLogger("test_logger")

        assert logger.logger.name == "test_logger"

    def test_log_agent_action(self):
        """Test logging agent action."""
        logger = StructuredLogger("test_logger")

        # Should not raise exception
        logger.log_agent_action(
            agent_id="agent_001",
            action="process_task",
            metadata={"task_id": "task_001"},
        )

    def test_log_llm_call(self):
        """Test logging LLM call."""
        logger = StructuredLogger("test_logger")

        logger.log_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            prompt_length=100,
            response_length=200,
            duration=1.5,
            success=True,
        )

        logger.log_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            prompt_length=100,
            response_length=0,
            duration=0.5,
            success=False,
            error="Rate limit exceeded",
        )

    def test_log_task_event(self):
        """Test logging task event."""
        logger = StructuredLogger("test_logger")

        logger.log_task_event(
            task_id="task_001",
            event="created",
            agent_id="agent_001",
        )

        logger.log_task_event(
            task_id="task_001",
            event="completed",
            agent_id="agent_001",
            metadata={"duration": 10.5},
        )

    def test_log_system_event(self):
        """Test logging system event."""
        logger = StructuredLogger("test_logger")

        logger.log_system_event(
            "System started",
            metadata={"version": "1.0.0"},
        )


class TestMetricsCollector:
    """Test MetricsCollector functionality."""

    def test_create_collector(self):
        """Test creating metrics collector."""
        collector = MetricsCollector()

        assert len(collector.metrics) == 0
        assert len(collector.llm_calls) == 0

    def test_record_llm_call(self):
        """Test recording LLM call."""
        collector = MetricsCollector()

        collector.record_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            tokens=500,
            duration=1.5,
            success=True,
        )

        assert len(collector.llm_calls) == 1
        assert collector.llm_calls[0]["tokens"] == 500
        assert collector.metrics["llm_calls.total"]["count"] == 1

    def test_record_task_event(self):
        """Test recording task event."""
        collector = MetricsCollector()

        collector.record_task_event(
            task_id="task_001",
            event="created",
            agent_id="agent_001",
        )

        collector.record_task_event(
            task_id="task_001",
            event="completed",
            duration=10.5,
        )

        assert len(collector.task_events) == 2
        assert collector.metrics["tasks.created"]["count"] == 1
        assert collector.metrics["tasks.completed"]["count"] == 1

    def test_record_agent_action(self):
        """Test recording agent action."""
        collector = MetricsCollector()

        collector.record_agent_action(
            agent_id="agent_001",
            action="process_task",
            duration=2.5,
        )

        assert len(collector.agent_actions) == 1
        assert collector.metrics["agent_actions.process_task"]["count"] == 1

    def test_get_metrics(self):
        """Test getting aggregated metrics."""
        collector = MetricsCollector()

        collector.record_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            tokens=500,
            duration=1.5,
            success=True,
        )

        collector.record_task_event(
            task_id="task_001",
            event="completed",
        )

        metrics = collector.get_metrics()

        assert "uptime_seconds" in metrics
        assert "llm_calls" in metrics
        assert "tasks" in metrics
        assert metrics["llm_calls"]["total"] == 1
        assert metrics["tasks"]["total"] == 1

    def test_get_agent_metrics(self):
        """Test getting agent-specific metrics."""
        collector = MetricsCollector()

        collector.record_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            tokens=500,
            duration=1.5,
        )

        collector.record_task_event(
            task_id="task_001",
            event="completed",
            agent_id="agent_001",
        )

        agent_metrics = collector.get_agent_metrics("agent_001")

        assert agent_metrics["agent_id"] == "agent_001"
        assert agent_metrics["llm_calls"] == 1
        assert agent_metrics["tasks"] == 1
        assert agent_metrics["total_tokens"] == 500

    def test_reset(self):
        """Test resetting metrics."""
        collector = MetricsCollector()

        collector.record_llm_call(
            agent_id="agent_001",
            model="gpt-4",
            tokens=500,
            duration=1.5,
        )

        collector.reset()

        assert len(collector.llm_calls) == 0
        assert len(collector.metrics) == 0
