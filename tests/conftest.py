"""Pytest configuration and shared fixtures."""

import pytest
from typing import AsyncGenerator

# Configure asyncio
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def sample_config() -> dict:
    """Sample configuration for testing."""
    return {
        "project": {
            "name": "Test Project",
            "version": "1.0.0"
        },
        "agents": {
            "dt": {
                "enabled": True,
                "model": "gpt-4",
                "autonomy_level": "high"
            }
        }
    }


@pytest.fixture
async def mock_llm():
    """Mock LLM for testing."""
    class MockLLM:
        def __init__(self):
            self.call_count = 0
            self.responses = {}
        
        async def generate(self, prompt: str, **kwargs) -> str:
            self.call_count += 1
            return self.responses.get(prompt, f"Mock response to: {prompt[:50]}...")
        
        def set_response(self, prompt: str, response: str):
            self.responses[prompt] = response
    
    return MockLLM()
