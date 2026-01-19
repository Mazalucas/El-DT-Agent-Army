"""Rules system for El DT."""

from pathlib import Path
from typing import Any, Dict, List, Optional


class RulesLoader:
    """Loader for rules from files."""

    @staticmethod
    def load_rules_file(file_path: str) -> str:
        """
        Load rules from a markdown file.

        Args:
            file_path: Path to rules file

        Returns:
            Rules content as string
        """
        path = Path(file_path)
        if not path.exists():
            return ""

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def load_all_rules(project_path: str) -> Dict[str, str]:
        """
        Load all rules from .taskmaster/rules directory.

        Args:
            project_path: Path to .taskmaster directory

        Returns:
            Dictionary mapping rule file names to content
        """
        rules_dir = Path(project_path) / "rules"
        if not rules_dir.exists():
            return {}

        rules = {}
        for rule_file in rules_dir.glob("*.md"):
            rules[rule_file.stem] = RulesLoader.load_rules_file(str(rule_file))

        return rules

    @staticmethod
    def load_mandatory_rules(project_path: str) -> str:
        """
        Load mandatory rules.

        Args:
            project_path: Path to .taskmaster directory

        Returns:
            Mandatory rules content
        """
        mandatory_file = Path(project_path) / "rules" / "mandatory_rules.md"
        return RulesLoader.load_rules_file(str(mandatory_file))


class RulesChecker:
    """Checker for rules compliance."""

    def __init__(self, rules: Dict[str, str]):
        """
        Initialize rules checker.

        Args:
            rules: Dictionary of rule names to content
        """
        self.rules = rules

    def check_action(self, action: str, context: Dict[str, Any]) -> bool:
        """
        Check if an action is allowed by rules.

        Args:
            action: Action to check
            context: Context for the action

        Returns:
            True if action is allowed
        """
        # Basic implementation - can be enhanced with more sophisticated parsing
        mandatory_rules = self.rules.get("mandatory_rules", "")
        dt_rules = self.rules.get("dt_rules", "")

        # Check for explicit prohibitions
        if "❌" in mandatory_rules and action in mandatory_rules:
            return False

        # Check for explicit permissions
        if "✅" in dt_rules and action in dt_rules:
            return True

        # Default: allow if not explicitly prohibited
        return True

    def get_autonomy_level(
        self, action: str, context: Dict[str, Any]
    ) -> str:
        """
        Get required autonomy level for an action.

        Args:
            action: Action to check
            context: Context for the action

        Returns:
            Autonomy level: "full" | "validated" | "consult" | "none"
        """
        # Basic implementation
        if self.check_action(action, context):
            # Check risk level from context
            risk = context.get("risk_level", 0.5)
            confidence = context.get("confidence", 0.5)

            if risk < 0.3 and confidence > 0.8:
                return "full"
            elif risk < 0.5 and confidence > 0.7:
                return "validated"
            elif risk < 0.7:
                return "consult"
            else:
                return "none"

        return "none"
