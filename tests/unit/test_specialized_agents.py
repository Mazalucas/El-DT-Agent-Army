"""Unit tests for specialized agents."""

import pytest

from agents_army.agents.backend_architect import BackendArchitect
from agents_army.agents.marketing_strategist import MarketingStrategist
from agents_army.agents.qa_tester import QATester
from agents_army.agents.researcher import Researcher
from agents_army.core.agent import LLMProvider
from agents_army.protocol.message import AgentMessage
from agents_army.protocol.types import AgentRole, MessageType


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    async def generate(self, prompt: str, **kwargs):
        """Generate mock response."""
        return "Mock response"


class TestResearcher:
    """Test Researcher agent."""

    def test_create_researcher(self):
        """Test creating Researcher agent."""
        researcher = Researcher(llm_provider=MockLLMProvider())

        assert researcher.name == "Researcher"
        assert researcher.role == AgentRole.RESEARCHER
        assert researcher.config.department == "Research"

    @pytest.mark.asyncio
    async def test_research(self):
        """Test research functionality."""
        researcher = Researcher(llm_provider=MockLLMProvider())

        result = await researcher.research("AI agents", "Context here")

        assert "query" in result
        assert result["query"] == "AI agents"
        assert "result" in result

    @pytest.mark.asyncio
    async def test_analyze_document(self):
        """Test document analysis."""
        researcher = Researcher(llm_provider=MockLLMProvider())

        result = await researcher.analyze_document("Test document content")

        assert "analysis" in result
        assert "document_length" in result

    @pytest.mark.asyncio
    async def test_handle_research_message(self):
        """Test handling research message."""
        researcher = Researcher(llm_provider=MockLLMProvider())

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.RESEARCHER,
            type=MessageType.TASK_REQUEST,
            payload={"query": "Test query", "task_id": "task_001"},
        )

        response = await researcher.handle_message(message)

        assert response is not None
        assert response.type == MessageType.TASK_RESPONSE
        assert "result" in response.payload


class TestBackendArchitect:
    """Test BackendArchitect agent."""

    def test_create_backend_architect(self):
        """Test creating BackendArchitect agent."""
        architect = BackendArchitect(llm_provider=MockLLMProvider())

        assert architect.name == "Backend Architect"
        assert architect.role == AgentRole.BACKEND_ARCHITECT
        assert architect.config.department == "Engineering"

    @pytest.mark.asyncio
    async def test_design_architecture(self):
        """Test architecture design."""
        architect = BackendArchitect(llm_provider=MockLLMProvider())

        requirements = {"type": "web_app", "users": 10000}
        result = await architect.design_architecture(requirements)

        assert "design" in result
        assert "requirements" in result

    @pytest.mark.asyncio
    async def test_handle_architecture_message(self):
        """Test handling architecture design message."""
        architect = BackendArchitect(llm_provider=MockLLMProvider())

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.BACKEND_ARCHITECT,
            type=MessageType.TASK_REQUEST,
            payload={"requirements": {"type": "api"}, "task_id": "task_001"},
        )

        response = await architect.handle_message(message)

        assert response is not None
        assert response.type == MessageType.TASK_RESPONSE


class TestMarketingStrategist:
    """Test MarketingStrategist agent."""

    def test_create_marketing_strategist(self):
        """Test creating MarketingStrategist agent."""
        strategist = MarketingStrategist(llm_provider=MockLLMProvider())

        assert strategist.name == "Marketing Strategist"
        assert strategist.role == AgentRole.MARKETING_STRATEGIST
        assert strategist.config.department == "Marketing"
        assert strategist.config.allow_delegation is True

    @pytest.mark.asyncio
    async def test_develop_strategy(self):
        """Test strategy development."""
        strategist = MarketingStrategist(llm_provider=MockLLMProvider())

        context = {"product": "App", "target": "Millennials"}
        result = await strategist.develop_strategy(context)

        assert "strategy" in result
        assert "context" in result

    @pytest.mark.asyncio
    async def test_handle_strategy_message(self):
        """Test handling strategy message."""
        strategist = MarketingStrategist(llm_provider=MockLLMProvider())

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.MARKETING_STRATEGIST,
            type=MessageType.TASK_REQUEST,
            payload={"context": {"product": "App"}, "task_id": "task_001"},
        )

        response = await strategist.handle_message(message)

        assert response is not None
        assert response.type == MessageType.TASK_RESPONSE


class TestQATester:
    """Test QATester agent."""

    def test_create_qa_tester(self):
        """Test creating QATester agent."""
        tester = QATester(llm_provider=MockLLMProvider())

        assert tester.name == "QA Tester"
        assert tester.role == AgentRole.QA_TESTER
        assert tester.config.department == "Testing"

    @pytest.mark.asyncio
    async def test_create_test_plan(self):
        """Test test plan creation."""
        tester = QATester(llm_provider=MockLLMProvider())

        feature_spec = {"name": "Login", "requirements": ["Auth", "Validation"]}
        result = await tester.create_test_plan(feature_spec)

        assert "test_plan" in result
        assert "feature" in result

    @pytest.mark.asyncio
    async def test_validate_output(self):
        """Test output validation."""
        tester = QATester(llm_provider=MockLLMProvider())

        result = await tester.validate_output("actual", "expected")

        assert "passed" in result
        assert "validation" in result

    @pytest.mark.asyncio
    async def test_handle_validation_message(self):
        """Test handling validation message."""
        tester = QATester(llm_provider=MockLLMProvider())

        message = AgentMessage(
            from_role=AgentRole.DT,
            to_role=AgentRole.QA_TESTER,
            type=MessageType.TASK_REQUEST,
            payload={
                "output": "result",
                "expected": "result",
                "task_id": "task_001",
            },
        )

        response = await tester.handle_message(message)

        assert response is not None
        assert response.type == MessageType.TASK_RESPONSE
