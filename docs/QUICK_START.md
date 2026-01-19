# Quick Start: Agents_Army

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd Agents_Army

# Instalar
pip install -e .
```

### Paso 2: Configurar API Key (Opcional)

```bash
# Para usar LLMs reales (opcional para empezar)
export OPENAI_API_KEY="tu-api-key"  # Linux/macOS
# O
$env:OPENAI_API_KEY="tu-api-key"     # Windows PowerShell
```

**Nota**: Puedes empezar sin API key usando mocks. Ver [API_KEYS_CONFIG.md](API_KEYS_CONFIG.md) para más detalles.

### Paso 3: Crear tu Primer Agente

```python
import asyncio
from agents_army import DT
from agents_army.core.agent import LLMProvider

# Crear LLM Provider (mock para empezar)
class MockLLMProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs):
        return f"Mock response to: {prompt[:50]}..."

# Crear El DT
dt = DT(
    project_path=".my_project",
    llm_provider=MockLLMProvider()
)

# Inicializar proyecto
async def main():
    project = await dt.initialize_project(
        project_name="Mi Primer Proyecto",
        description="Un proyecto de prueba"
    )
    print(f"✅ Proyecto creado: {project.name}")

asyncio.run(main())
```

### Paso 4: Ejecutar Ejemplo

```bash
# Ver ejemplo básico
python examples/basic_agent_example.py

# Ver ejemplo completo
python examples/complete_app_example.py
```

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

**Tiempo estimado**: 5 minutos  
**Dificultad**: Fácil
