"""Unit tests for ConfigLoader."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from agents_army.core.config import ConfigLoader
from agents_army.protocol.types import AgentRole


class TestConfigLoader:
    """Test ConfigLoader class."""

    def test_load_yaml_config(self):
        """Test loading YAML configuration."""
        config_data = {
            "agents": {
                "researcher": {
                    "name": "Researcher",
                    "goal": "Research topics",
                    "backstory": "You are a researcher",
                    "model": "gpt-4",
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            config = ConfigLoader.load_from_file(temp_path)
            assert "agents" in config
            assert "researcher" in config["agents"]
        finally:
            Path(temp_path).unlink()

    def test_load_json_config(self):
        """Test loading JSON configuration."""
        config_data = {
            "agents": {
                "researcher": {
                    "name": "Researcher",
                    "goal": "Research topics",
                    "backstory": "You are a researcher",
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            config = ConfigLoader.load_from_file(temp_path)
            assert "agents" in config
        finally:
            Path(temp_path).unlink()

    def test_create_agent_config(self):
        """Test creating AgentConfig from dictionary."""
        config_dict = {
            "name": "Test Researcher",
            "goal": "Research topics",
            "backstory": "You are a researcher",
            "instructions": "Always cite sources",
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "max_tokens": 2000,
            "verbose": False,
            "allow_delegation": True,
            "max_iterations": 5,
            "department": "Research",
        }

        agent_config = ConfigLoader.create_agent_config(config_dict, AgentRole.RESEARCHER)

        assert agent_config.name == "Test Researcher"
        assert agent_config.role == AgentRole.RESEARCHER
        assert agent_config.goal == "Research topics"
        assert agent_config.backstory == "You are a researcher"
        assert agent_config.instructions == "Always cite sources"
        assert agent_config.model == "gpt-3.5-turbo"
        assert agent_config.temperature == 0.8
        assert agent_config.max_tokens == 2000
        assert agent_config.verbose is False
        assert agent_config.allow_delegation is True
        assert agent_config.max_iterations == 5
        assert agent_config.department == "Research"

    def test_load_agents_from_config(self):
        """Test loading multiple agents from config."""
        config_data = {
            "agents": {
                "researcher": {
                    "name": "Researcher",
                    "goal": "Research topics",
                    "backstory": "You are a researcher",
                },
                "writer": {
                    "name": "Writer",
                    "goal": "Write content",
                    "backstory": "You are a writer",
                },
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            agent_configs = ConfigLoader.load_agents_from_config(temp_path)

            assert AgentRole.RESEARCHER in agent_configs
            assert AgentRole.WRITER in agent_configs
            assert agent_configs[AgentRole.RESEARCHER].name == "Researcher"
            assert agent_configs[AgentRole.WRITER].name == "Writer"
        finally:
            Path(temp_path).unlink()

    def test_load_nonexistent_file(self):
        """Test loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader.load_from_file("nonexistent.yaml")

    def test_load_unsupported_format(self):
        """Test loading unsupported format raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                ConfigLoader.load_from_file(temp_path)
        finally:
            Path(temp_path).unlink()
