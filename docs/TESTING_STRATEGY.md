# Estrategia de Testing: Agents_Army

## Visión General

Este documento define la estrategia completa de testing para **Agents_Army**, incluyendo unit tests, integration tests, end-to-end tests, y testing de agentes.

## Pirámide de Testing

```
        /\
       /  \      E2E Tests (pocos, críticos)
      /____\
     /      \    Integration Tests (algunos, importantes)
    /________\
   /          \  Unit Tests (muchos, rápidos)
  /____________\
```

## Niveles de Testing

### 1. Unit Tests

**Objetivo**: Probar componentes individuales en aislamiento.

**Cobertura Objetivo**: > 80%

**Estrategia**:
```python
# tests/unit/test_agent.py
class TestAgent:
    def test_agent_initialization(self):
        """Test que un agente se inicializa correctamente."""
        agent = Agent(
            role="researcher",
            goal="Research topics",
            backstory="You are a researcher"
        )
        assert agent.role == "researcher"
        assert agent.goal == "Research topics"
    
    def test_agent_execute_task(self):
        """Test ejecución de tarea."""
        agent = create_test_agent()
        task = create_test_task()
        result = await agent.execute(task)
        assert result.status == "completed"
    
    @pytest.mark.asyncio
    async def test_agent_with_mock_llm(self):
        """Test agente con LLM mockeado."""
        mock_llm = MockLLM(response="Test response")
        agent = Agent(llm=mock_llm)
        result = await agent.execute(task)
        assert result.content == "Test response"
```

**Mock de LLMs**:
```python
# tests/fixtures/mock_llm.py
class MockLLM:
    def __init__(self, response: str = None, error: Exception = None):
        self.response = response
        self.error = error
        self.call_count = 0
    
    async def generate(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        if self.error:
            raise self.error
        return self.response or f"Mock response to: {prompt}"
    
    def assert_called_with(self, expected_prompt: str):
        """Verifica que se llamó con el prompt esperado."""
        assert self.last_prompt == expected_prompt
```

### 2. Integration Tests

**Objetivo**: Probar interacción entre componentes.

**Estrategia**:
```python
# tests/integration/test_agent_communication.py
class TestAgentCommunication:
    @pytest.mark.asyncio
    async def test_dt_to_agent_communication(self):
        """Test comunicación DT → Agente."""
        dt = create_test_dt()
        agent = create_test_agent()
        
        message = AgentMessage(
            from_role="dt",
            to_role="researcher",
            type="task_request",
            payload={"task": "Research X"}
        )
        
        result = await dt.send_message(message, agent)
        assert result.status == "received"
    
    @pytest.mark.asyncio
    async def test_multi_agent_workflow(self):
        """Test workflow multi-agente."""
        dt = create_test_dt()
        researcher = create_test_researcher()
        writer = create_test_writer()
        
        # DT asigna tarea a researcher
        task1 = await dt.assign_task(researcher, "Research X")
        result1 = await researcher.execute(task1)
        
        # DT asigna tarea a writer con contexto
        task2 = await dt.assign_task(writer, "Write about X", context=result1)
        result2 = await writer.execute(task2)
        
        assert result2.status == "completed"
        assert "X" in result2.content
```

### 3. End-to-End Tests

**Objetivo**: Probar flujos completos de usuario.

**Estrategia**:
```python
# tests/e2e/test_complete_project.py
class TestCompleteProject:
    @pytest.mark.asyncio
    async def test_complete_marketing_campaign(self):
        """Test creación completa de campaña de marketing."""
        # 1. Inicializar proyecto
        dt = DT()
        project = await dt.initialize_project("Marketing Campaign")
        
        # 2. Parsear PRD
        tasks = await dt.parse_prd("docs/prd_marketing.txt")
        assert len(tasks) > 0
        
        # 3. Ejecutar tareas
        for task in tasks:
            result = await dt.execute_task(task)
            assert result.status == "completed"
        
        # 4. Verificar resultados
        final_result = await dt.synthesize_results()
        assert final_result.has_all_components()
```

### 4. Performance Tests

**Objetivo**: Verificar performance y escalabilidad.

**Estrategia**:
```python
# tests/performance/test_load.py
class TestLoad:
    @pytest.mark.asyncio
    async def test_concurrent_tasks(self):
        """Test ejecución concurrente de tareas."""
        dt = create_test_dt()
        tasks = [create_test_task() for _ in range(10)]
        
        start = time.time()
        results = await asyncio.gather(*[dt.execute_task(t) for t in tasks])
        duration = time.time() - start
        
        assert all(r.status == "completed" for r in results)
        assert duration < 30  # Debe completar en < 30s
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test uso de memoria."""
        import tracemalloc
        
        tracemalloc.start()
        dt = create_test_dt()
        await dt.execute_complex_workflow()
        
        current, peak = tracemalloc.get_traced_memory()
        assert peak < 500 * 1024 * 1024  # < 500MB
```

### 5. Agent-Specific Tests

**Objetivo**: Probar cada agente individualmente.

**Estrategia**:
```python
# tests/agents/test_researcher.py
class TestResearcher:
    @pytest.mark.asyncio
    async def test_researcher_web_search(self):
        """Test búsqueda web del researcher."""
        researcher = create_test_researcher()
        results = await researcher.search_web("Python testing")
        assert len(results) > 0
        assert all(r.has_url() for r in results)
    
    @pytest.mark.asyncio
    async def test_researcher_document_analysis(self):
        """Test análisis de documentos."""
        researcher = create_test_researcher()
        document = "Test document content..."
        analysis = await researcher.analyze_document(document)
        assert analysis.has_summary()
        assert analysis.has_key_points()

# tests/agents/test_dt.py
class TestDT:
    @pytest.mark.asyncio
    async def test_dt_autonomous_decision(self):
        """Test decisión autónoma del DT."""
        dt = create_test_dt()
        situation = create_test_situation(risk="low", confidence="high")
        
        decision = await dt.decide_and_act(situation)
        assert decision.autonomous == True
        assert decision.action == Action.EXECUTE_AUTONOMOUSLY
    
    @pytest.mark.asyncio
    async def test_dt_escalation(self):
        """Test escalamiento del DT."""
        dt = create_test_dt()
        situation = create_test_situation(risk="high")
        
        decision = await dt.decide_and_act(situation)
        assert decision.autonomous == False
        assert decision.action == Action.ESCALATE_TO_HUMAN
```

## Fixtures y Helpers

### Fixtures Comunes

```python
# tests/conftest.py
import pytest
from agents_army import AgentSystem, DT, Researcher
from tests.fixtures.mock_llm import MockLLM

@pytest.fixture
def mock_llm():
    """Fixture de LLM mockeado."""
    return MockLLM(response="Mock response")

@pytest.fixture
def test_agent_system(mock_llm):
    """Fixture de sistema de agentes para testing."""
    system = AgentSystem()
    system.llm_provider = mock_llm
    return system

@pytest.fixture
def test_dt(test_agent_system):
    """Fixture de DT para testing."""
    return DT(system=test_agent_system)

@pytest.fixture
def sample_task():
    """Fixture de tarea de ejemplo."""
    return Task(
        id="test_task_1",
        description="Test task",
        type="research",
        parameters={"query": "test"}
    )
```

### Helpers de Testing

```python
# tests/helpers.py
def create_test_agent(role: str = "test", **kwargs) -> Agent:
    """Helper para crear agentes de test."""
    defaults = {
        "role": role,
        "goal": f"Test goal for {role}",
        "backstory": f"Test backstory for {role}",
        "model": "mock"
    }
    defaults.update(kwargs)
    return Agent(**defaults)

def create_test_task(**kwargs) -> Task:
    """Helper para crear tareas de test."""
    defaults = {
        "id": f"test_{uuid.uuid4()}",
        "description": "Test task",
        "type": "test"
    }
    defaults.update(kwargs)
    return Task(**defaults)

async def wait_for_condition(
    condition: Callable,
    timeout: int = 10,
    interval: float = 0.5
) -> bool:
    """Espera hasta que una condición se cumpla."""
    start = time.time()
    while time.time() - start < timeout:
        if await condition():
            return True
        await asyncio.sleep(interval)
    return False
```

## Test Data Management

### Datos de Test

```python
# tests/fixtures/test_data.py
class TestData:
    SAMPLE_PRD = """
    # Product Requirements Document
    
    ## Overview
    Test product for testing purposes.
    
    ## Features
    1. Feature A
    2. Feature B
    """
    
    SAMPLE_TASKS = [
        {
            "id": "task_1",
            "description": "Implement feature A",
            "type": "development"
        },
        {
            "id": "task_2",
            "description": "Test feature A",
            "type": "testing"
        }
    ]
    
    SAMPLE_AGENT_RESPONSES = {
        "researcher": "Research results: ...",
        "writer": "Written content: ...",
        "validator": {"valid": True, "score": 0.9}
    }
```

## Mocking Strategies

### Mock de LLMs

```python
# tests/fixtures/mock_llm.py
class MockLLM:
    """Mock de LLM para testing."""
    
    def __init__(self):
        self.responses = {}
        self.call_history = []
    
    def set_response(self, prompt_pattern: str, response: str):
        """Configura respuesta para un patrón de prompt."""
        self.responses[prompt_pattern] = response
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Genera respuesta mockeada."""
        self.call_history.append({
            "prompt": prompt,
            "kwargs": kwargs,
            "timestamp": datetime.now()
        })
        
        # Buscar respuesta configurada
        for pattern, response in self.responses.items():
            if pattern in prompt:
                return response
        
        # Respuesta por defecto
        return f"Mock response to: {prompt[:50]}..."
    
    def assert_called(self, times: int = None):
        """Verifica que se llamó el número de veces esperado."""
        if times is not None:
            assert len(self.call_history) == times
        else:
            assert len(self.call_history) > 0
```

### Mock de Herramientas

```python
# tests/fixtures/mock_tools.py
class MockWebSearch:
    def __init__(self):
        self.results = []
    
    def set_results(self, query: str, results: List[Source]):
        """Configura resultados para una query."""
        self.results.append((query, results))
    
    async def search(self, query: str) -> List[Source]:
        """Búsqueda mockeada."""
        for q, results in self.results:
            if q in query:
                return results
        return []
```

## Test Coverage

### Cobertura Objetivo

```yaml
coverage:
  overall: 80
  critical_paths: 95
  agents: 85
  dt: 90
  protocol: 90
  memory: 80
  tools: 75
```

### Configuración

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=agents_army
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

## Continuous Testing

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest tests/unit -v
        language: system
        pass_filenames: false
      
      - id: lint
        name: Lint code
        entry: ruff check .
        language: system
      
      - id: type-check
        name: Type check
        entry: mypy agents_army/
        language: system
```

### CI Testing

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: pytest tests/unit -v --cov
      
      - name: Run integration tests
        run: pytest tests/integration -v
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Scenarios

### Escenarios Críticos

```python
# tests/scenarios/critical.py
class CriticalScenarios:
    @pytest.mark.asyncio
    async def test_dt_handles_agent_failure(self):
        """Test que El DT maneja fallo de agente."""
        dt = create_test_dt()
        agent = create_failing_agent()
        
        task = await dt.assign_task(agent, "Test task")
        # Agente falla
        result = await agent.execute(task)
        assert result.status == "failed"
        
        # DT debe reasignar
        new_result = await dt.handle_agent_failure(task, agent)
        assert new_result.status == "reassigned"
    
    @pytest.mark.asyncio
    async def test_dt_autonomous_decision_under_pressure(self):
        """Test decisión autónoma bajo presión."""
        dt = create_test_dt()
        # Simular alta carga
        for _ in range(10):
            await dt.create_task("High priority task")
        
        # DT debe seguir tomando decisiones
        situation = create_test_situation()
        decision = await dt.decide_and_act(situation)
        assert decision is not None
```

## Property-Based Testing

```python
# tests/property/test_protocol.py
from hypothesis import given, strategies as st

class TestProtocolProperties:
    @given(
        message_type=st.sampled_from(MessageType),
        payload=st.dictionaries(st.text(), st.text())
    )
    def test_message_serialization_roundtrip(
        self,
        message_type: MessageType,
        payload: dict
    ):
        """Test que serialización/deserialización es idempotente."""
        message = AgentMessage(
            type=message_type,
            payload=payload
        )
        
        serialized = serialize(message)
        deserialized = deserialize(serialized)
        
        assert deserialized.type == message.type
        assert deserialized.payload == message.payload
```

## Performance Benchmarks

```python
# tests/benchmarks/test_performance.py
import pytest

@pytest.mark.benchmark
class TestPerformance:
    def test_message_throughput(self, benchmark):
        """Benchmark de throughput de mensajes."""
        router = MessageRouter()
        message = create_test_message()
        
        result = benchmark.pedantic(
            router.route,
            args=(message,),
            rounds=1000
        )
        
        assert result < 0.001  # < 1ms por mensaje
    
    def test_agent_initialization(self, benchmark):
        """Benchmark de inicialización de agentes."""
        result = benchmark.pedantic(
            Agent,
            kwargs={"role": "test", "goal": "test"},
            rounds=100
        )
        
        assert result is not None
```

## Test Documentation

### Documentar Tests

```python
class TestResearcher:
    """
    Tests para el agente Researcher.
    
    Estos tests verifican:
    - Búsqueda web correcta
    - Análisis de documentos
    - Extracción de información
    - Manejo de errores
    """
    
    @pytest.mark.asyncio
    async def test_researcher_web_search(self):
        """
        Test: Researcher puede buscar en web.
        
        Given: Researcher con herramienta web_search
        When: Se ejecuta búsqueda
        Then: Retorna resultados válidos con URLs
        """
        # Given
        researcher = create_test_researcher()
        
        # When
        results = await researcher.search_web("Python")
        
        # Then
        assert len(results) > 0
        assert all(r.url for r in results)
```

## Checklist de Testing

### Pre-commit
- [ ] Unit tests pasan
- [ ] Linting pasa
- [ ] Type checking pasa
- [ ] Coverage > 80%

### Pre-merge
- [ ] Todos los tests pasan
- [ ] Integration tests pasan
- [ ] Coverage report generado
- [ ] Performance tests pasan

### Pre-release
- [ ] E2E tests pasan
- [ ] Load tests pasan
- [ ] Security tests pasan
- [ ] Regression tests pasan

---

**Última actualización**: Enero 2025  
**Estado**: Estrategia Definida
