# Quick Start: Agents_Army

## 🚀 Dos Caminos para Empezar

### Camino 1: Ya Tienes un Proyecto

Si ya tienes un proyecto Python y quieres integrar Agents_Army:

```bash
# 1. Clonar el repo en tu proyecto (o instalar como dependencia)
cd tu-proyecto-existente
git clone https://github.com/Mazalucas/El-DT-Agent-Army.git
cd El-DT-Agent-Army
pip install -e .

# 2. Configurar API key (opcional para empezar)
export OPENAI_API_KEY="tu-api-key"  # Linux/macOS
# O
$env:OPENAI_API_KEY="tu-api-key"    # Windows PowerShell

# 3. Usar en tu código existente
```

```python
# En tu proyecto existente
from agents_army import DT, Researcher, BackendArchitect
from agents_army.core.agent import LLMProvider
import os

# Crear tu LLM Provider
class OpenAIProvider(LLMProvider):
    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate(self, prompt: str, **kwargs):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# Usar El DT en tu proyecto
llm = OpenAIProvider()
dt = DT(project_path=".", llm_provider=llm)

# Inicializar proyecto en tu directorio actual
project = await dt.initialize_project(
    project_name="Tu Proyecto",
    description="Descripción de tu proyecto"
)
```

**Listo**: El DT está integrado en tu proyecto y puede gestionar tareas.

---

### Camino 2: Conversar con El DT para Planear y Armar el Proyecto

Si no tienes un proyecto y quieres que El DT te ayude a planearlo desde cero:

```bash
# 1. Clonar el repo
git clone https://github.com/Mazalucas/El-DT-Agent-Army.git
cd El-DT-Agent-Army

# 2. Instalar
pip install -e .

# 3. Configurar API key
export OPENAI_API_KEY="tu-api-key"  # Linux/macOS
# O
$env:OPENAI_API_KEY="tu-api-key"    # Windows PowerShell

# 4. Ejecutar ejemplo de conversación con El DT
python examples/dt_example.py
```

O crear tu propio script de conversación:

```python
import asyncio
from agents_army import DT
from agents_army.core.agent import LLMProvider
import os

# Tu LLM Provider (ver docs/API_KEYS_CONFIG.md)
class OpenAIProvider(LLMProvider):
    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate(self, prompt: str, **kwargs):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

async def main():
    # Crear El DT
    llm = OpenAIProvider()
    dt = DT(project_path=".nuevo_proyecto", llm_provider=llm)
    
    # Conversar con El DT para planear
    print("🤖 Conversando con El DT para planear tu proyecto...")
    
    # Inicializar proyecto
    project = await dt.initialize_project(
        project_name="Mi Nuevo Proyecto",
        description="Quiero crear una aplicación web con Python y React"
    )
    
    # Crear PRD (Product Requirements Document)
    prd_content = """
# Mi Proyecto

## Objetivo
Crear una aplicación web moderna

## Requisitos
1. Backend con Python/FastAPI
2. Frontend con React
3. Base de datos PostgreSQL
4. Autenticación de usuarios
"""
    
    # Guardar PRD
    prd_path = ".nuevo_proyecto/docs/prd.txt"
    with open(prd_path, "w") as f:
        f.write(prd_content)
    
    # El DT parsea el PRD y genera tareas automáticamente
    tasks = await dt.parse_prd()
    
    print(f"\n✅ El DT ha generado {len(tasks)} tareas:")
    for task in tasks:
        print(f"  - {task.title} (Prioridad: {task.priority})")
    
    # El DT puede asignar tareas a agentes especializados
    next_task = await dt.get_next_task()
    if next_task:
        print(f"\n📋 Siguiente tarea: {next_task.title}")
        print(f"   Descripción: {next_task.description}")

asyncio.run(main())
```

**Resultado**: El DT te ayuda a planear, genera tareas automáticamente y puede asignarlas a agentes especializados.

---

## ⚠️ Configuración de API Keys

**Importante**: Para usar LLMs reales, necesitas configurar API keys.

Ver **[API_KEYS_CONFIG.md](API_KEYS_CONFIG.md)** para instrucciones detalladas.

```bash
# Configurar variable de entorno (recomendado)
export OPENAI_API_KEY="tu-api-key"  # Linux/macOS
# O
$env:OPENAI_API_KEY="tu-api-key"    # Windows PowerShell
```

**Nota**: Puedes empezar sin API key usando mocks para probar la estructura.

---

## 📚 Próximos Pasos

1. **Leer**: [USER_GUIDE.md](USER_GUIDE.md) - Guía completa de usuario
2. **Configurar**: [API_KEYS_CONFIG.md](API_KEYS_CONFIG.md) - Configuración de API keys
3. **Integrar**: [INTEGRATION.md](INTEGRATION.md) - Integración en tu proyecto
4. **Explorar**: [examples/](../examples/) - Más ejemplos

## 🔍 ¿Problemas?

- Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Ver [FAQ.md](FAQ.md)
- Verificar [REQUIREMENTS.md](REQUIREMENTS.md)

---

**Tiempo estimado**: 5-10 minutos  
**Dificultad**: Fácil
