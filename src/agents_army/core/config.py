"""Configuration management for agents."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from agents_army.core.agent import AgentConfig
from agents_army.protocol.types import AgentRole


class ConfigLoader:
    """Loader for agent configuration from YAML/JSON files."""

    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]:
        """
        Load configuration from a file.

        Supports both YAML (.yaml, .yml) and JSON (.json) formats.

        Args:
            file_path: Path to configuration file

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in (".yaml", ".yml"):
                return yaml.safe_load(f) or {}
            elif path.suffix == ".json":
                return json.load(f)
            else:
                raise ValueError(
                    f"Unsupported file format: {path.suffix}. "
                    "Supported formats: .yaml, .yml, .json"
                )

    @staticmethod
    def create_agent_config(config_dict: Dict[str, Any], role: AgentRole) -> AgentConfig:
        """
        Create AgentConfig from dictionary.

        Args:
            config_dict: Configuration dictionary
            role: Agent role

        Returns:
            AgentConfig instance
        """
        return AgentConfig(
            name=config_dict.get("name", role.value),
            role=role,
            goal=config_dict.get("goal", ""),
            backstory=config_dict.get("backstory", ""),
            instructions=config_dict.get("instructions"),
            model=config_dict.get("model", "gpt-4"),
            temperature=config_dict.get("temperature", 0.7),
            max_tokens=config_dict.get("max_tokens"),
            verbose=config_dict.get("verbose", True),
            allow_delegation=config_dict.get("allow_delegation", False),
            max_iterations=config_dict.get("max_iterations", 3),
            department=config_dict.get("department"),
        )

    @staticmethod
    def load_agents_from_config(
        config_path: str,
    ) -> Dict[AgentRole, AgentConfig]:
        """
        Load agent configurations from a config file.

        Expected format:
        ```yaml
        agents:
          researcher:
            name: "Researcher"
            goal: "Research topics thoroughly"
            backstory: "You are an expert researcher..."
            model: "gpt-4"
          writer:
            name: "Writer"
            goal: "Write high-quality content"
            ...
        ```

        Args:
            config_path: Path to configuration file

        Returns:
            Dictionary mapping AgentRole to AgentConfig
        """
        config = ConfigLoader.load_from_file(config_path)
        agents_config = config.get("agents", {})

        agent_configs = {}
        for role_str, agent_dict in agents_config.items():
            try:
                role = AgentRole(role_str)
                agent_config = ConfigLoader.create_agent_config(agent_dict, role)
                agent_configs[role] = agent_config
            except ValueError:
                # Skip invalid roles
                continue

        return agent_configs
