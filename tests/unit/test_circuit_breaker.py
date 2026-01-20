"""Tests for TaskCircuitBreaker."""

import tempfile

import pytest

from agents_army.core.circuit_breaker import (
    CircuitBreakerResult,
    CircuitState,
    TaskCircuitBreaker,
)
from agents_army.core.progress_tracker import TaskProgressTracker
from agents_army.core.task_storage import TaskStorage


class TestTaskCircuitBreaker:
    """Tests for TaskCircuitBreaker class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def progress_tracker(self, temp_dir):
        """Create TaskProgressTracker instance."""
        storage = TaskStorage(temp_dir)
        return TaskProgressTracker(storage)

    @pytest.fixture
    def circuit_breaker(self):
        """Create TaskCircuitBreaker instance."""
        return TaskCircuitBreaker(
            no_progress_threshold=3,
            same_error_threshold=5,
        )

    def test_check_should_continue_normal(self, circuit_breaker, progress_tracker):
        """Test normal operation (circuit closed)."""
        # Record some progress
        progress_tracker.record_iteration(
            task_id="test_task",
            iteration=1,
            file_changes=["file1.py"],
            test_results={"passed": True},
            agent_output="",
            errors=[],
        )
        
        result = circuit_breaker.check_should_continue(
            "test_task", 2, progress_tracker
        )
        
        assert result.should_continue is True
        assert result.state == CircuitState.CLOSED.value

    def test_check_should_continue_no_progress(self, circuit_breaker, progress_tracker):
        """Test circuit opening due to no progress."""
        # Record iterations without progress
        for i in range(1, 4):
            progress_tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],  # No changes
                test_results={"passed": False},
                agent_output="",
                errors=[],
            )
        
        result = circuit_breaker.check_should_continue(
            "test_task", 4, progress_tracker
        )
        
        assert result.should_continue is False
        assert result.state == CircuitState.OPEN.value
        assert "no progress" in result.reason.lower()

    def test_check_should_continue_repeated_errors(self, circuit_breaker, progress_tracker):
        """Test circuit opening due to repeated errors."""
        # Record iterations with same error
        for i in range(1, 6):
            progress_tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],
                test_results={"passed": False},
                agent_output="",
                errors=["Same error"],
            )
        
        result = circuit_breaker.check_should_continue(
            "test_task", 6, progress_tracker
        )
        
        # Should open due to repeated errors
        assert result.should_continue is False

    def test_is_open(self, circuit_breaker, progress_tracker):
        """Test checking if circuit is open."""
        assert circuit_breaker.is_open("test_task") is False
        
        # Open circuit
        for i in range(1, 4):
            progress_tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],
                test_results={},
                agent_output="",
                errors=[],
            )
        
        circuit_breaker.check_should_continue("test_task", 4, progress_tracker)
        
        assert circuit_breaker.is_open("test_task") is True

    def test_reset(self, circuit_breaker, progress_tracker):
        """Test resetting circuit breaker."""
        # Open circuit
        for i in range(1, 4):
            progress_tracker.record_iteration(
                task_id="test_task",
                iteration=i,
                file_changes=[],
                test_results={},
                agent_output="",
                errors=[],
            )
        
        circuit_breaker.check_should_continue("test_task", 4, progress_tracker)
        assert circuit_breaker.is_open("test_task") is True
        
        # Reset
        circuit_breaker.reset("test_task")
        assert circuit_breaker.is_open("test_task") is False

    def test_strict_mode(self):
        """Test strict mode uses stricter thresholds."""
        normal_breaker = TaskCircuitBreaker(strict_mode=False)
        strict_breaker = TaskCircuitBreaker(strict_mode=True)
        
        # Strict mode should have lower thresholds
        assert strict_breaker.no_progress_threshold <= normal_breaker.no_progress_threshold
        assert strict_breaker.same_error_threshold <= normal_breaker.same_error_threshold

    def test_record_iteration(self, circuit_breaker):
        """Test recording iteration."""
        circuit_breaker.record_iteration(
            "test_task",
            has_progress=True,
            errors=[],
        )
        
        # Should not raise exception
        assert True
