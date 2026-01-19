# Requisitos y Configuración: Agents_Army

## Requisitos del Sistema

### Mínimos

- **Python**: 3.10 o superior (3.11+ recomendado)
- **pip**: Incluido con Python
- **Sistema Operativo**: Windows 10+, Linux, macOS 11+
- **RAM**: 4GB mínimo (8GB+ recomendado)
- **Disco**: ~100MB para instalación base

### Recomendados

- **Entorno virtual**: Python venv o virtualenv
- **Git**: Para clonar el repositorio
- **IDE**: VS Code, PyCharm, o similar

## Dependencias del Proyecto

### Core (Obligatorias)

```txt
pydantic>=2.0.0              # Validación de datos
pydantic-settings>=2.0.0     # Configuración
typing-extensions>=4.8.0     # Type hints
pyyaml>=6.0.0                # Soporte YAML
```

### Desarrollo (Opcionales)

```txt
pytest>=7.4.0                # Testing
pytest-asyncio>=0.21.0       # Async testing
black>=23.0.0                # Formateo
ruff>=0.1.0                  # Linting
mypy>=1.5.0                  # Type checking
```

### LLM Providers (Opcionales - Elige uno o más)

```txt
# Para OpenAI
openai>=1.0.0

# Para Anthropic
anthropic>=0.7.0

# O implementa tu propio provider
```

## Instalación

Ver [INSTALLATION.md](INSTALLATION.md) para instrucciones detalladas.

## API Keys

### ¿Necesito API Keys?

- **NO** para:
  - Testing (usa mocks)
  - Desarrollo básico
  - Ejemplos básicos

- **SÍ** para:
  - Uso real con LLMs
  - Generación de contenido
  - Proyectos completos

### Cómo Obtener API Keys

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Anthropic**: https://console.anthropic.com/
3. **Otros**: Implementa tu propio `LLMProvider`

### Configuración Segura

```bash
# Opción 1: Variable de entorno (recomendado)
export OPENAI_API_KEY="tu-api-key"

# Opción 2: Archivo .env (no incluido en repo)
# OPENAI_API_KEY=tu-api-key
```

## Verificación

```bash
# Verificar Python
python --version  # Debe ser 3.10+

# Verificar instalación
python -c "from agents_army import AgentSystem; print('✅ OK')"

# Ejecutar tests
pytest tests/unit/test_version.py -v
```

## Troubleshooting

Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para problemas comunes.
