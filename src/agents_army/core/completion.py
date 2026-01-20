"""Completion criteria for determining task completion."""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from agents_army.core.models import Task, TaskResult


@dataclass
class CompletionCriteria:
    """Criteria for determining if a task is complete."""

    tests_must_pass: bool = False
    linter_must_pass: bool = False
    build_must_succeed: bool = False
    agent_exit_signal: bool = False
    completion_indicators: int = 0
    min_completion_indicators: int = 2
    min_file_changes: int = 1
    validation_runner: Optional[Any] = None  # ValidationRunner instance

    def is_complete(
        self, task_result: TaskResult, agent_output: str, file_changes: List[str] = None
    ) -> bool:
        """
        Check if task is complete based on criteria.

        Args:
            task_result: Result from task execution
            agent_output: Output from agent
            file_changes: List of changed files (optional)

        Returns:
            True if task is complete, False otherwise
        """
        if file_changes is None:
            file_changes = []

        # Check file changes minimum
        if len(file_changes) < self.min_file_changes:
            return False

        # Extract exit signal from agent output
        exit_signal = self.extract_exit_signal(agent_output)

        # Count completion indicators
        indicators = self.count_completion_indicators(agent_output)

        # Check if we have minimum indicators
        if indicators < self.min_completion_indicators:
            return False

        # Check exit signal requirement
        if self.agent_exit_signal and not exit_signal:
            return False

        # Check tests if required
        if self.tests_must_pass:
            if not self.check_tests():
                return False

        # Check linter if required
        if self.linter_must_pass:
            if not self.check_linter():
                return False

        # Check build if required
        if self.build_must_succeed:
            if not self.check_build():
                return False

        # All criteria met
        return True

    def check_tests(self) -> bool:
        """
        Check if tests pass.

        Returns:
            True if tests pass, False otherwise
        """
        if not self.validation_runner:
            # If no validation runner, assume tests pass
            return True

        try:
            test_results = self.validation_runner.run_tests()
            return test_results.passed
        except Exception:
            # If validation fails, assume tests don't pass
            return False

    def check_linter(self) -> bool:
        """
        Check if linter passes.

        Returns:
            True if linter passes, False otherwise
        """
        if not self.validation_runner:
            # If no validation runner, assume linter passes
            return True

        try:
            linter_results = self.validation_runner.run_linter()
            return linter_results.passed
        except Exception:
            # If validation fails, assume linter doesn't pass
            return False

    def check_build(self) -> bool:
        """
        Check if build succeeds.

        Returns:
            True if build succeeds, False otherwise
        """
        if not self.validation_runner:
            # If no validation runner, assume build succeeds
            return True

        try:
            build_results = self.validation_runner.run_build()
            return build_results.succeeded
        except Exception:
            # If validation fails, assume build doesn't succeed
            return False

    def extract_exit_signal(self, agent_output: str) -> bool:
        """
        Extract EXIT_SIGNAL from agent output.

        Looks for patterns like:
        - EXIT_SIGNAL: true
        - EXIT_SIGNAL: True
        - RALPH_STATUS: { EXIT_SIGNAL: true }

        Args:
            agent_output: Output from agent

        Returns:
            True if exit signal found, False otherwise
        """
        if not agent_output:
            return False

        output_lower = agent_output.lower()

        # Check for explicit EXIT_SIGNAL
        if "exit_signal" in output_lower:
            # Look for EXIT_SIGNAL: true pattern
            pattern = r"exit_signal\s*[:=]\s*(true|1|yes)"
            if re.search(pattern, output_lower):
                return True

        # Check for RALPH_STATUS block
        ralph_pattern = r"ralph_status[:\s]*\{[^}]*exit_signal[:\s]*(true|1|yes)"
        if re.search(ralph_pattern, output_lower, re.IGNORECASE):
            return True

        return False

    def count_completion_indicators(self, agent_output: str) -> int:
        """
        Count completion indicators in agent output.

        Looks for phrases like:
        - "complete", "completed", "done", "finished"
        - "all tasks done", "project complete"
        - "ready for review", "ready to deploy"

        Args:
            agent_output: Output from agent

        Returns:
            Number of completion indicators found
        """
        if not agent_output:
            return 0

        output_lower = agent_output.lower()
        count = 0

        # Strong completion phrases
        strong_phrases = [
            "all tasks complete",
            "all tasks completed",
            "project complete",
            "project completed",
            "everything is done",
            "all done",
            "fully complete",
            "completely finished",
            "ready for review",
            "ready to deploy",
            "ready for production",
        ]

        for phrase in strong_phrases:
            if phrase in output_lower:
                count += 2  # Strong indicators count as 2

        # Medium completion phrases
        medium_phrases = [
            "complete",
            "completed",
            "done",
            "finished",
            "ready",
            "successful",
            "successfully",
        ]

        for phrase in medium_phrases:
            # Count standalone words, not substrings
            pattern = r"\b" + re.escape(phrase) + r"\b"
            matches = len(re.findall(pattern, output_lower))
            count += matches

        # Check for explicit completion blocks
        if "completion:" in output_lower or "status: complete" in output_lower:
            count += 1

        return count


class CompletionCriteriaFactory:
    """Factory for creating completion criteria based on task type."""

    @staticmethod
    def create_for_task(task: Task, autonomy_level: int) -> CompletionCriteria:
        """
        Create completion criteria for a task based on its type and autonomy level.

        Args:
            task: Task to create criteria for
            autonomy_level: Autonomy level (1-4)

        Returns:
            CompletionCriteria instance
        """
        task_type = CompletionCriteriaFactory._detect_task_type(task)

        if task_type == "code_implementation":
            return CompletionCriteria(
                tests_must_pass=True,
                linter_must_pass=True,
                build_must_succeed=True,
                agent_exit_signal=True,
                min_completion_indicators=2 if autonomy_level >= 4 else 3,
            )

        elif task_type == "documentation":
            return CompletionCriteria(
                tests_must_pass=False,
                linter_must_pass=True,  # Only formatting
                build_must_succeed=False,
                agent_exit_signal=True,
                min_completion_indicators=1,
            )

        elif task_type == "research":
            return CompletionCriteria(
                tests_must_pass=False,
                linter_must_pass=False,
                build_must_succeed=False,
                agent_exit_signal=True,
                min_completion_indicators=2,
            )

        # Default for general tasks
        return CompletionCriteria(
            tests_must_pass=False,
            linter_must_pass=False,
            build_must_succeed=False,
            agent_exit_signal=True,
            min_completion_indicators=2,
        )

    @staticmethod
    def _detect_task_type(task: Task) -> str:
        """
        Detect task type from description and tags.

        Args:
            task: Task to analyze

        Returns:
            Task type string
        """
        desc_lower = task.description.lower()
        tags_lower = [t.lower() for t in task.tags]

        # Check tags first (more reliable)
        if "documentation" in tags_lower or "docs" in tags_lower:
            return "documentation"
        if "code" in tags_lower or "implementation" in tags_lower:
            return "code_implementation"
        if "research" in tags_lower:
            return "research"

        # Check for documentation keywords (must check before code keywords)
        # Look for documentation context first
        doc_keywords = ["documentation", "document", "write", "readme", "guide", "tutorial", "docs"]
        doc_contexts = ["write", "create", "draft", "prepare"]
        
        # If description contains doc keywords AND doc contexts, it's documentation
        has_doc_keyword = any(keyword in desc_lower for keyword in doc_keywords)
        has_doc_context = any(context in desc_lower for context in doc_contexts)
        
        if has_doc_keyword or (has_doc_context and ("guide" in desc_lower or "readme" in desc_lower or "tutorial" in desc_lower)):
            return "documentation"

        # Check for research keywords
        research_keywords = ["research", "investigate", "analyze", "study", "explore"]
        if any(keyword in desc_lower for keyword in research_keywords):
            return "research"

        # Check for code implementation keywords (after checking docs)
        code_keywords = ["implement", "code", "function", "class", "endpoint"]
        # Check "api" only if it's clearly implementation, not documentation
        if "api" in desc_lower:
            # If it says "write documentation for API" or similar, it's documentation
            if "documentation" in desc_lower or "document" in desc_lower or "guide" in desc_lower:
                return "documentation"
            # Otherwise, if it has implementation keywords, it's code
            if any(keyword in desc_lower for keyword in ["implement", "code", "function", "class", "endpoint"]):
                return "code_implementation"
        elif any(keyword in desc_lower for keyword in code_keywords):
            return "code_implementation"

        return "general"
