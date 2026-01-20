# Guía de Instalación: Agents_Army

## Requisitos Previos

- **Python**: 3.10 o superior
- **pip**: Versión reciente
- **Sistema Operativo**: Windows, Linux, macOS

## Instalación

### Opción 1: Instalación en Modo Desarrollo (Recomendado)

```bash
# 1. Clonar o descargar el repositorio
git clone <repo-url>
cd Agents_Army

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. Instalar en modo desarrollo
pip install -e .

# 4. Instalar dependencias de desarrollo (opcional)
pip install -r requirements-dev.txt
```

### Opción 2: Instalación de Dependencias Directa

```bash
# Instalar solo dependencias core
pip install -r requirements.txt

# Para desarrollo
pip install -r requirements-dev.txt
```

## Verificación de Instalación

```bash
# Verificar que el paquete se importa correctamente
python -c "from agents_army import AgentSystem, DT; print('✅ Instalación exitosa')"

# Ejecutar tests
pytest tests/unit/test_version.py -v

# Ejecutar ejemplo básico
python examples/basic_message_example.py
```

## Dependencias Principales

### Core
- `pydantic>=2.0.0` - Validación de datos
- `pydantic-settings>=2.0.0` - Configuración
- `pyyaml>=6.0.0` - Soporte YAML

### Desarrollo
- `pytest>=7.4.0` - Testing
- `black>=23.0.0` - Formateo
- `ruff>=0.1.0` - Linting
- `mypy>=1.5.0` - Type checking

## Configuración de LLM Provider

El framework requiere un LLM provider. Ejemplo de integración:

```python
from agents_army.core.agent import LLMProvider
import openai  # o anthropic, etc.

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate(self, prompt: str, **kwargs):
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
```

## Próximos Pasos

1. Ver [USER_GUIDE.md](docs/USER_GUIDE.md) para uso básico
2. Revisar [ejemplos/](examples/) para casos de uso
3. Leer [INTEGRATION.md](docs/INTEGRATION.md) para integración

## Troubleshooting

### Error: "No module named 'agents_army'"

```bash
# Asegúrate de estar en el directorio del proyecto
cd Agents_Army

# Reinstalar en modo desarrollo
pip install -e .
```

### Error: "ModuleNotFoundError: No module named 'yaml'"

```bash
# Instalar PyYAML
pip install pyyaml
```

### Error en Windows con encoding

Algunos ejemplos pueden tener problemas con emojis en Windows. Los ejemplos han sido actualizados para evitar este problema.

## Soporte

- Ver [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para más ayuda
- Revisar [ejemplos/](examples/) para referencias
- Consultar [docs/](docs/) para documentación completa
