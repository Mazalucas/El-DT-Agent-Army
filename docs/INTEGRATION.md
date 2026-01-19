# Guía de Integración: Conectando Agents_Army a Nuevos Proyectos

## Visión General

Esta guía explica cómo integrar el framework **Agents_Army** en nuevos proyectos de manera simple y rápida.

## Enfoque de Integración

### Principios de Diseño

1. **Mínima Invasión**: El framework no requiere cambios masivos en proyectos existentes
2. **Configuración Declarativa**: Define agentes y flujos mediante configuración
3. **Interfaces Estándar**: APIs claras y consistentes
4. **Modularidad**: Usa solo los componentes que necesitas

## Pasos de Integración

### Paso 1: Instalación

```bash
# Opción 1: Como dependencia (cuando esté publicado)
pip install agents-army

# Opción 2: Como submodule
git submodule add https://github.com/tu-usuario/Agents_Army.git agents_army

# Opción 3: Copiar componentes necesarios
# Copia solo los módulos que necesites a tu proyecto
```

### Paso 2: Configuración Básica

Crea un archivo de configuración `agents_config.yaml`:

```yaml
# agents_config.yaml
project:
  name: "Mi Proyecto"
  version: "1.0.0"

agents:
  coordinator:
    enabled: true
    type: "coordinator"
    config:
      max_concurrent_tasks: 10
      timeout: 300s

  researcher:
    enabled: true
    type: "specialist"
    specialization: "research"
    config:
      tools:
        - web_search
        - document_parser
      max_tokens: 4000

  validator:
    enabled: true
    type: "validator"
    config:
      min_quality_score: 0.7
      strict_mode: true

protocol:
  version: "1.0.0"
  message_timeout: 30s
  max_retries: 3

memory:
  enabled: true
  backend: "local"  # o "vector_db", "redis", etc.
  retention:
    session: "1h"
    task: "7d"
```

### Paso 3: Inicialización en tu Código

```python
# main.py o tu archivo principal
from agents_army import AgentSystem, Coordinator, Specialist, Validator
from agents_army.config import load_config

# Cargar configuración
config = load_config("agents_config.yaml")

# Inicializar sistema
system = AgentSystem(config)

# O inicializar agentes individuales
coordinator = Coordinator(config.agents.coordinator)
researcher = Specialist(config.agents.researcher)
validator = Validator(config.agents.validator)

# Registrar agentes en el sistema
system.register_agent(coordinator)
system.register_agent(researcher)
system.register_agent(validator)
```

### Paso 4: Definir tus Herramientas

```python
# tools/my_tools.py
from agents_army.tools import Tool, ToolRegistry

# Definir una herramienta personalizada
class MyCustomTool(Tool):
    name = "my_custom_tool"
    description = "Descripción de mi herramienta"
    
    def execute(self, params: dict) -> dict:
        # Tu lógica aquí
        result = do_something(params)
        return {
            "success": True,
            "result": result
        }

# Registrar herramienta
ToolRegistry.register(MyCustomTool())
```

### Paso 5: Usar el Sistema

```python
# Ejemplo de uso básico
async def main():
    # Solicitar una tarea al coordinador
    task = {
        "type": "research",
        "description": "Investigar sobre X",
        "parameters": {
            "topic": "X",
            "depth": "medium"
        }
    }
    
    # El coordinador maneja todo el flujo
    result = await coordinator.execute_task(task)
    
    print(f"Resultado: {result}")
```

## Patrones de Integración

### Patrón 1: Integración Mínima

Para proyectos que solo necesitan un agente simple:

```python
from agents_army import Specialist

# Crear un especialista simple
agent = Specialist(
    name="mi_agente",
    capabilities=["web_search", "text_generation"]
)

# Usar directamente
result = await agent.execute("Buscar información sobre X")
```

### Patrón 2: Integración con API Existente

Para agregar agentes a una API REST existente:

```python
# api/routes.py
from fastapi import FastAPI
from agents_army import AgentSystem

app = FastAPI()
system = AgentSystem.load_from_config("agents_config.yaml")

@app.post("/api/tasks")
async def create_task(task: dict):
    result = await system.coordinator.execute_task(task)
    return result
```

### Patrón 3: Integración con Base de Datos

Para proyectos que necesitan persistencia:

```python
from agents_army import AgentSystem
from agents_army.memory import DatabaseMemoryBackend

# Configurar memoria con base de datos
memory_backend = DatabaseMemoryBackend(
    connection_string="postgresql://...",
    table_name="agent_memory"
)

system = AgentSystem(
    config=config,
    memory_backend=memory_backend
)
```

### Patrón 4: Integración con Webhooks

Para sistemas que reciben eventos externos:

```python
from agents_army import AgentSystem

system = AgentSystem.load_from_config("agents_config.yaml")

async def handle_webhook(event: dict):
    # Convertir evento a tarea
    task = {
        "type": "process_event",
        "description": f"Procesar evento {event['type']}",
        "parameters": event
    }
    
    # Ejecutar con el sistema
    result = await system.coordinator.execute_task(task)
    return result
```

## Configuración por Entorno

### Desarrollo

```yaml
# config/development.yaml
agents:
  coordinator:
    config:
      debug: true
      log_level: "DEBUG"
      timeout: 600s  # Más tiempo para debugging

memory:
  backend: "local"
  retention:
    session: "24h"  # Más tiempo para desarrollo
```

### Producción

```yaml
# config/production.yaml
agents:
  coordinator:
    config:
      debug: false
      log_level: "INFO"
      timeout: 300s
      rate_limit: 100  # Límites de rate

memory:
  backend: "redis"
  connection: "${REDIS_URL}"
  retention:
    session: "1h"
    task: "7d"
```

## Adaptadores para Proyectos Existentes

### Adaptador para Django

```python
# agents_army/adapters/django.py
from django.apps import AppConfig
from agents_army import AgentSystem

class AgentsArmyConfig(AppConfig):
    default_auto_field = 'django.db.BigAutoField'
    name = 'agents_army'
    
    def ready(self):
        # Inicializar sistema al arrancar Django
        self.system = AgentSystem.load_from_config(
            "agents_config.yaml"
        )
```

### Adaptador para Flask

```python
# agents_army/adapters/flask.py
from flask import Flask, g
from agents_army import AgentSystem

def get_agent_system():
    if 'agent_system' not in g:
        g.agent_system = AgentSystem.load_from_config(
            "agents_config.yaml"
        )
    return g.agent_system

@app.teardown_appcontext
def close_agent_system(error):
    g.pop('agent_system', None)
```

### Adaptador para FastAPI

```python
# agents_army/adapters/fastapi.py
from fastapi import FastAPI, Depends
from agents_army import AgentSystem

def get_agent_system():
    return AgentSystem.load_from_config("agents_config.yaml")

app = FastAPI()

@app.post("/tasks")
async def create_task(
    task: dict,
    system: AgentSystem = Depends(get_agent_system)
):
    return await system.coordinator.execute_task(task)
```

## Herramientas Personalizadas

### Crear Herramientas para tu Dominio

```python
# tools/domain_tools.py
from agents_army.tools import Tool

class DomainSpecificTool(Tool):
    """Herramienta específica de tu dominio"""
    
    name = "domain_tool"
    description = "Herramienta para operaciones de dominio"
    parameters = {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["action"]
    }
    
    def execute(self, params: dict) -> dict:
        action = params.get("action")
        data = params.get("data", {})
        
        # Tu lógica de dominio
        if action == "create":
            result = self.create_item(data)
        elif action == "update":
            result = self.update_item(data)
        else:
            raise ValueError(f"Acción desconocida: {action}")
        
        return {
            "success": True,
            "result": result
        }
    
    def create_item(self, data):
        # Implementación
        pass
    
    def update_item(self, data):
        # Implementación
        pass
```

## Testing

### Configuración para Tests

```python
# tests/conftest.py
import pytest
from agents_army import AgentSystem
from agents_army.memory import InMemoryBackend

@pytest.fixture
def test_agent_system():
    """Sistema de agentes para testing"""
    config = {
        "agents": {
            "coordinator": {"enabled": True},
            "researcher": {"enabled": True}
        },
        "memory": {
            "backend": "in_memory"
        }
    }
    
    system = AgentSystem(config)
    system.memory_backend = InMemoryBackend()
    
    return system
```

### Tests de Integración

```python
# tests/test_integration.py
import pytest

@pytest.mark.asyncio
async def test_task_execution(test_agent_system):
    task = {
        "type": "research",
        "description": "Test task",
        "parameters": {"topic": "test"}
    }
    
    result = await test_agent_system.coordinator.execute_task(task)
    
    assert result["status"] == "completed"
    assert "result" in result
```

## Migración Gradual

### Fase 1: Prueba de Concepto

1. Instala el framework en un entorno de desarrollo
2. Crea un agente simple para una tarea específica
3. Prueba con casos de uso reales
4. Evalúa resultados y ajusta

### Fase 2: Integración Parcial

1. Integra agentes en módulos específicos
2. Mantén funcionalidad existente intacta
3. Compara resultados entre métodos antiguos y nuevos
4. Itera y mejora

### Fase 3: Migración Completa

1. Reemplaza funcionalidad antigua con agentes
2. Configura producción con monitoreo
3. Documenta cambios y procedimientos
4. Capacita al equipo

## Checklist de Integración

- [ ] Framework instalado y configurado
- [ ] Archivo de configuración creado
- [ ] Agentes básicos inicializados
- [ ] Herramientas personalizadas definidas (si aplica)
- [ ] Integración con proyecto existente completada
- [ ] Tests escritos y pasando
- [ ] Documentación actualizada
- [ ] Monitoreo y logging configurados
- [ ] Despliegue en entorno de desarrollo
- [ ] Pruebas de carga realizadas
- [ ] Despliegue en producción

## Troubleshooting

### Problema: Agentes no se comunican

**Solución**: Verifica la configuración del protocolo y que todos los agentes estén registrados en el sistema.

### Problema: Timeouts frecuentes

**Solución**: Aumenta los timeouts en la configuración o optimiza las tareas.

### Problema: Memoria no persiste

**Solución**: Verifica la configuración del backend de memoria y las credenciales de conexión.

## Recursos Adicionales

- [Guía de Arquitectura](ARCHITECTURE.md)
- [Ejemplos de Uso](EXAMPLES.md)
- [API Reference](API.md) (próximamente)
