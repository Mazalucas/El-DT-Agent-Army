"""Task scheduler for intelligent task scheduling and prioritization."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from agents_army.core.models import Task


class TaskScheduler:
    """
    Intelligent task scheduler that optimizes task execution order.
    
    Considers dependencies, priorities, resource availability,
    and deadlines to create optimal execution schedules.
    """

    def __init__(self):
        """Initialize TaskScheduler."""
        pass

    def schedule_tasks(
        self,
        tasks: List[Task],
        available_agents: Optional[List[str]] = None,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> List[Task]:
        """
        Schedule tasks in optimal execution order.

        Args:
            tasks: List of tasks to schedule
            available_agents: Optional list of available agent roles
            constraints: Optional scheduling constraints

        Returns:
            List of tasks in scheduled order
        """
        # Build dependency graph
        task_map = {task.id: task for task in tasks}
        ready_tasks = [t for t in tasks if t.is_ready()]
        scheduled = []
        scheduled_ids = set()

        # Sort ready tasks by priority (highest first)
        ready_tasks.sort(key=lambda t: t.priority, reverse=True)

        # Schedule ready tasks first
        while ready_tasks:
            task = ready_tasks.pop(0)
            if task.id not in scheduled_ids:
                scheduled.append(task)
                scheduled_ids.add(task.id)

                # Check if any dependent tasks are now ready
                for other_task in tasks:
                    if (
                        task.id in other_task.dependencies
                        and other_task.id not in scheduled_ids
                    ):
                        other_task.remove_dependency(task.id)
                        if other_task.is_ready():
                            ready_tasks.append(other_task)
                            ready_tasks.sort(
                                key=lambda t: t.priority, reverse=True
                            )

        # Add any remaining tasks (may have circular dependencies)
        for task in tasks:
            if task.id not in scheduled_ids:
                scheduled.append(task)

        return scheduled

    def estimate_duration(self, task: Task) -> timedelta:
        """
        Estimate task duration.

        Args:
            task: Task to estimate

        Returns:
            Estimated duration
        """
        # Simple heuristic based on description length and complexity
        description_length = len(task.description)
        num_dependencies = len(task.dependencies)

        # Base duration: 1 hour
        base_hours = 1.0

        # Add time based on description length
        base_hours += description_length / 1000  # ~1 hour per 1000 chars

        # Add time for dependencies
        base_hours += num_dependencies * 0.5

        # Adjust by priority (higher priority = more time allocated)
        priority_multiplier = task.priority / 3.0
        base_hours *= priority_multiplier

        return timedelta(hours=min(base_hours, 24))  # Cap at 24 hours

    def find_critical_path(self, tasks: List[Task]) -> List[str]:
        """
        Find critical path through task dependencies.

        Args:
            tasks: List of tasks

        Returns:
            List of task IDs in critical path
        """
        task_map = {task.id: task for task in tasks}
        in_degree = {task.id: len(task.dependencies) for task in tasks}
        critical_path = []

        # Find tasks with no dependencies (start nodes)
        queue = [task.id for task in tasks if len(task.dependencies) == 0]

        while queue:
            current_id = queue.pop(0)
            critical_path.append(current_id)

            # Find tasks that depend on current task
            for task in tasks:
                if current_id in task.dependencies:
                    in_degree[task.id] -= 1
                    if in_degree[task.id] == 0:
                        queue.append(task.id)

        return critical_path

    def optimize_schedule(
        self,
        tasks: List[Task],
        deadline: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Optimize task schedule considering deadlines.

        Args:
            tasks: List of tasks
            deadline: Optional deadline

        Returns:
            Optimization result with schedule and metrics
        """
        scheduled = self.schedule_tasks(tasks)
        critical_path = self.find_critical_path(tasks)

        total_duration = timedelta()
        for task_id in critical_path:
            task = next(t for t in tasks if t.id == task_id)
            total_duration += self.estimate_duration(task)

        on_time = True
        if deadline:
            estimated_completion = datetime.now() + total_duration
            on_time = estimated_completion <= deadline

        return {
            "schedule": scheduled,
            "critical_path": critical_path,
            "estimated_duration": total_duration,
            "on_time": on_time,
            "tasks_count": len(tasks),
            "ready_tasks": len([t for t in tasks if t.is_ready()]),
        }
