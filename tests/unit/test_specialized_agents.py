"""Unit tests for specialized agents."""

import pytest

from agents_army.agents.backend_architect import BackendArchitect
from agents_army.agents.brand_guardian import BrandGuardian
from agents_army.agents.content_creator import ContentCreator
from agents_army.agents.devops_automator import DevOpsAutomator
from agents_army.agents.feedback_synthesizer import FeedbackSynthesizer
from agents_army.agents.frontend_developer import FrontendDeveloper
from agents_army.agents.growth_hacker import GrowthHacker
from agents_army.agents.marketing_strategist import MarketingStrategist
from agents_army.agents.operations_maintainer import OperationsMaintainer
from agents_army.agents.pitch_specialist import PitchSpecialist
from agents_army.agents.product_strategist import ProductStrategist
from agents_army.agents.qa_tester import QATester
from agents_army.agents.researcher import Researcher
from agents_army.agents.storytelling_specialist import StorytellingSpecialist
from agents_army.agents.ui_designer import UIDesigner
from agents_army.agents.ux_researcher import UXResearcher
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


class TestDevOpsAutomator:
    """Test DevOpsAutomator agent."""

    def test_create_devops_automator(self):
        """Test creating DevOpsAutomator agent."""
        automator = DevOpsAutomator(llm_provider=MockLLMProvider())

        assert automator.name == "DevOps Automator"
        assert automator.role == AgentRole.DEVOPS_AUTOMATOR
        assert automator.config.department == "Engineering"

    @pytest.mark.asyncio
    async def test_create_cicd_pipeline(self):
        """Test CI/CD pipeline creation."""
        automator = DevOpsAutomator(llm_provider=MockLLMProvider())

        project_config = {"language": "Python", "framework": "FastAPI"}
        result = await automator.create_cicd_pipeline(project_config)

        assert "pipeline" in result
        assert "project_config" in result


class TestFrontendDeveloper:
    """Test FrontendDeveloper agent."""

    def test_create_frontend_developer(self):
        """Test creating FrontendDeveloper agent."""
        developer = FrontendDeveloper(llm_provider=MockLLMProvider())

        assert developer.name == "Frontend Developer"
        assert developer.role == AgentRole.FRONTEND_DEVELOPER
        assert developer.config.department == "Engineering"

    @pytest.mark.asyncio
    async def test_implement_ui(self):
        """Test UI implementation."""
        developer = FrontendDeveloper(llm_provider=MockLLMProvider())

        design_spec = {"layout": "grid", "components": ["header", "footer"]}
        result = await developer.implement_ui(design_spec)

        assert "implementation" in result
        assert "design_spec" in result


class TestProductStrategist:
    """Test ProductStrategist agent."""

    def test_create_product_strategist(self):
        """Test creating ProductStrategist agent."""
        strategist = ProductStrategist(llm_provider=MockLLMProvider())

        assert strategist.name == "Product Strategist"
        assert strategist.role == AgentRole.PRODUCT_STRATEGIST
        assert strategist.config.department == "Product"
        assert strategist.config.allow_delegation is True

    @pytest.mark.asyncio
    async def test_prioritize_features(self):
        """Test feature prioritization."""
        strategist = ProductStrategist(llm_provider=MockLLMProvider())

        features = [{"name": "Feature 1", "value": 5}, {"name": "Feature 2", "value": 3}]
        context = {"budget": 10000, "timeline": "Q1"}
        result = await strategist.prioritize_features(features, context)

        assert "prioritized" in result
        assert "features" in result


class TestFeedbackSynthesizer:
    """Test FeedbackSynthesizer agent."""

    def test_create_feedback_synthesizer(self):
        """Test creating FeedbackSynthesizer agent."""
        synthesizer = FeedbackSynthesizer(llm_provider=MockLLMProvider())

        assert synthesizer.name == "Feedback Synthesizer"
        assert synthesizer.role == AgentRole.FEEDBACK_SYNTHESIZER
        assert synthesizer.config.department == "Product"

    @pytest.mark.asyncio
    async def test_collect_feedback(self):
        """Test feedback collection."""
        synthesizer = FeedbackSynthesizer(llm_provider=MockLLMProvider())

        sources = [{"source": "survey", "feedback": "Great product"}]
        result = await synthesizer.collect_feedback(sources)

        assert "collected" in result
        assert "sources" in result


class TestUXResearcher:
    """Test UXResearcher agent."""

    def test_create_ux_researcher(self):
        """Test creating UXResearcher agent."""
        researcher = UXResearcher(llm_provider=MockLLMProvider())

        assert researcher.name == "UX Researcher"
        assert researcher.role == AgentRole.UX_RESEARCHER
        assert researcher.config.department == "Design"

    @pytest.mark.asyncio
    async def test_research_users(self):
        """Test user research."""
        researcher = UXResearcher(llm_provider=MockLLMProvider())

        questions = ["What are user pain points?", "How do users navigate?"]
        result = await researcher.research_users(questions)

        assert "research" in result
        assert "questions" in result


class TestUIDesigner:
    """Test UIDesigner agent."""

    def test_create_ui_designer(self):
        """Test creating UIDesigner agent."""
        designer = UIDesigner(llm_provider=MockLLMProvider())

        assert designer.name == "UI Designer"
        assert designer.role == AgentRole.UI_DESIGNER
        assert designer.config.department == "Design"

    @pytest.mark.asyncio
    async def test_create_design(self):
        """Test design creation."""
        designer = UIDesigner(llm_provider=MockLLMProvider())

        requirements = {"type": "dashboard", "style": "modern"}
        result = await designer.create_design(requirements)

        assert "design" in result
        assert "requirements" in result


class TestBrandGuardian:
    """Test BrandGuardian agent."""

    def test_create_brand_guardian(self):
        """Test creating BrandGuardian agent."""
        guardian = BrandGuardian(llm_provider=MockLLMProvider())

        assert guardian.name == "Brand Guardian"
        assert guardian.role == AgentRole.BRAND_GUARDIAN
        assert guardian.config.department == "Marketing"

    @pytest.mark.asyncio
    async def test_review_brand_compliance(self):
        """Test brand compliance review."""
        guardian = BrandGuardian(llm_provider=MockLLMProvider())

        result = await guardian.review_brand_compliance("Sample content", "text")

        assert "compliant" in result
        assert "content_type" in result


class TestContentCreator:
    """Test ContentCreator agent."""

    def test_create_content_creator(self):
        """Test creating ContentCreator agent."""
        creator = ContentCreator(llm_provider=MockLLMProvider())

        assert creator.name == "Content Creator"
        assert creator.role == AgentRole.CONTENT_CREATOR
        assert creator.config.department == "Marketing"
        assert creator.config.allow_delegation is True

    @pytest.mark.asyncio
    async def test_create_content(self):
        """Test content creation."""
        creator = ContentCreator(llm_provider=MockLLMProvider())

        brief = {"channel": "blog", "topic": "AI", "tone": "professional"}
        result = await creator.create_content(brief)

        assert "content" in result
        assert "brief" in result


class TestStorytellingSpecialist:
    """Test StorytellingSpecialist agent."""

    def test_create_storytelling_specialist(self):
        """Test creating StorytellingSpecialist agent."""
        specialist = StorytellingSpecialist(llm_provider=MockLLMProvider())

        assert specialist.name == "Storytelling Specialist"
        assert specialist.role == AgentRole.STORYTELLING_SPECIALIST
        assert specialist.config.department == "Marketing"
        assert specialist.config.allow_delegation is True

    @pytest.mark.asyncio
    async def test_create_story(self):
        """Test story creation."""
        specialist = StorytellingSpecialist(llm_provider=MockLLMProvider())

        brief = {"protagonist": "User", "conflict": "Problem", "resolution": "Solution"}
        result = await specialist.create_story(brief)

        assert "narrative" in result
        assert "brief" in result


class TestPitchSpecialist:
    """Test PitchSpecialist agent."""

    def test_create_pitch_specialist(self):
        """Test creating PitchSpecialist agent."""
        specialist = PitchSpecialist(llm_provider=MockLLMProvider())

        assert specialist.name == "Pitch Specialist"
        assert specialist.role == AgentRole.PITCH_SPECIALIST
        assert specialist.config.department == "Marketing"
        assert specialist.config.allow_delegation is True

    @pytest.mark.asyncio
    async def test_create_pitch(self):
        """Test pitch creation."""
        specialist = PitchSpecialist(llm_provider=MockLLMProvider())

        brief = {"audience": "investors", "objective": "funding", "duration": 10}
        result = await specialist.create_pitch(brief)

        assert "narrative" in result
        assert "brief" in result


class TestGrowthHacker:
    """Test GrowthHacker agent."""

    def test_create_growth_hacker(self):
        """Test creating GrowthHacker agent."""
        hacker = GrowthHacker(llm_provider=MockLLMProvider())

        assert hacker.name == "Growth Hacker"
        assert hacker.role == AgentRole.GROWTH_HACKER
        assert hacker.config.department == "Marketing"

    @pytest.mark.asyncio
    async def test_design_experiment(self):
        """Test experiment design."""
        hacker = GrowthHacker(llm_provider=MockLLMProvider())

        hypothesis = "Adding social proof increases conversions"
        result = await hacker.design_experiment(hypothesis)

        assert "experiment" in result
        assert "hypothesis" in result


class TestOperationsMaintainer:
    """Test OperationsMaintainer agent."""

    def test_create_operations_maintainer(self):
        """Test creating OperationsMaintainer agent."""
        maintainer = OperationsMaintainer(llm_provider=MockLLMProvider())

        assert maintainer.name == "Operations Maintainer"
        assert maintainer.role == AgentRole.OPERATIONS_MAINTAINER
        assert maintainer.config.department == "Operations"

    @pytest.mark.asyncio
    async def test_monitor_systems(self):
        """Test system monitoring."""
        maintainer = OperationsMaintainer(llm_provider=MockLLMProvider())

        result = await maintainer.monitor_systems()

        assert "status" in result
        assert "health" in result
