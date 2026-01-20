"""Task decomposer for breaking down complex tasks into subtasks."""

import uuid
from typing import Any, Dict, List, Optional

from agents_army.core.agent import LLMProvider
from agents_army.core.models import Task


class TaskDecomposer:
    """
    Decomposes complex tasks into smaller, manageable subtasks.

    Uses LLM to intelligently break down tasks based on complexity,
    dependencies, and best practices.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        """
        Initialize TaskDecomposer.

        Args:
            llm_provider: Optional LLM provider for task decomposition
        """
        self.llm_provider = llm_provider

    async def decompose(
        self,
        task: Task,
        max_subtasks: int = 5,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Task]:
        """
        Decompose a complex task into subtasks.

        Args:
            task: Task to decompose
            max_subtasks: Maximum number of subtasks to create
            context: Optional context for decomposition

        Returns:
            List of subtasks
        """
        if not self.llm_provider:
            # Simple decomposition without LLM
            return self._simple_decompose(task, max_subtasks)

        prompt = f"""Decompose the following task into {max_subtasks} or fewer subtasks:

Task: {task.title}
Description: {task.description}
Priority: {task.priority}
Tags: {', '.join(task.tags)}

"""
        if context:
            prompt += f"Context: {context}\n"

        prompt += """
Provide a JSON array of subtasks, each with:
- title: Short title
- description: Detailed description
- priority: Priority level (1-5)
- tags: List of relevant tags
- dependencies: List of other subtask titles this depends on

Return only valid JSON array.
"""

        try:
            response = await self.llm_provider.generate(prompt)
            # Parse JSON response
            import json
            import re

            # Extract JSON from response
            json_match = re.search(r"\[.*\]", response, re.DOTALL)
            if json_match:
                subtasks_data = json.loads(json_match.group())
            else:
                # Fallback to simple decomposition
                return self._simple_decompose(task, max_subtasks)

            subtasks = []
            for i, subtask_data in enumerate(subtasks_data[:max_subtasks]):
                subtask = Task(
                    id=f"{task.id}_subtask_{i+1}",
                    title=subtask_data.get("title", f"Subtask {i+1}"),
                    description=subtask_data.get("description", ""),
                    priority=subtask_data.get("priority", task.priority),
                    tags=subtask_data.get("tags", task.tags.copy()),
                    dependencies=subtask_data.get("dependencies", []),
                    metadata={"parent_task": task.id},
                )
                subtasks.append(subtask)

            return subtasks

        except Exception:
            # Fallback to simple decomposition
            return self._simple_decompose(task, max_subtasks)

    def _simple_decompose(self, task: Task, max_subtasks: int = 5) -> List[Task]:
        """
        Simple decomposition without LLM.

        Args:
            task: Task to decompose
            max_subtasks: Maximum number of subtasks

        Returns:
            List of subtasks
        """
        # Simple heuristic: split by sentences or key phrases
        description_parts = task.description.split(". ")
        num_subtasks = min(len(description_parts), max_subtasks)

        subtasks = []
        for i in range(num_subtasks):
            part = description_parts[i] if i < len(description_parts) else f"Part {i+1}"
            subtask = Task(
                id=f"{task.id}_subtask_{i+1}",
                title=f"{task.title} - Part {i+1}",
                description=part,
                priority=task.priority,
                tags=task.tags.copy(),
                metadata={"parent_task": task.id},
            )
            subtasks.append(subtask)

        return subtasks

    def estimate_complexity(self, task: Task) -> str:
        """
        Estimate task complexity.

        Args:
            task: Task to analyze

        Returns:
            Complexity level: "low" | "medium" | "high"
        """
        # Simple heuristic based on description length and dependencies
        description_length = len(task.description)
        num_dependencies = len(task.dependencies)

        if description_length > 500 or num_dependencies > 3:
            return "high"
        elif description_length > 200 or num_dependencies > 1:
            return "medium"
        else:
            return "low"
