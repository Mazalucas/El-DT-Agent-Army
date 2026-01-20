# Explicación de Archivos en el Directorio Raíz

Este documento explica qué son y por qué están en el directorio raíz del proyecto.

## ✅ Archivos que DEBEN estar en el raíz

### 📦 Configuración del Proyecto Python

#### `pyproject.toml` ✅ **ESENCIAL**
- **Qué es**: Configuración moderna del proyecto Python (PEP 518)
- **Por qué en raíz**: Estándar de Python, herramientas como pip, setuptools lo buscan aquí
- **Contiene**: Metadata del proyecto, dependencias, configuración de herramientas (black, ruff, mypy, pytest)

#### `setup.py` ✅ **NECESARIO**
- **Qué es**: Script de instalación tradicional (compatibilidad)
- **Por qué en raíz**: Necesario para `pip install -e .` y compatibilidad con herramientas antiguas
- **Nota**: Aunque `pyproject.toml` es moderno, `setup.py` aún se necesita para algunos casos

#### `requirements.txt` ✅ **ESENCIAL**
- **Qué es**: Lista de dependencias de producción
- **Por qué en raíz**: Convención estándar, `pip install -r requirements.txt` lo busca aquí
- **Uso**: `pip install -r requirements.txt`

#### `requirements-dev.txt` ✅ **ESENCIAL**
- **Qué es**: Dependencias de desarrollo (tests, linting, etc.)
- **Por qué en raíz**: Convención estándar para separar dependencias de desarrollo
- **Uso**: `pip install -r requirements-dev.txt`

### 🐳 Configuración Docker

#### `Dockerfile` ✅ **ESENCIAL**
- **Qué es**: Instrucciones para construir imagen Docker
- **Por qué en raíz**: Docker busca `Dockerfile` en el contexto (raíz por defecto)
- **Uso**: `docker build .`

#### `docker-compose.yml` ✅ **ÚTIL**
- **Qué es**: Configuración de servicios Docker (orquestación)
- **Por qué en raíz**: `docker-compose` busca este archivo en el raíz
- **Uso**: `docker-compose up`

### 🛠️ Herramientas de Desarrollo

#### `.pre-commit-config.yaml` ✅ **ÚTIL**
- **Qué es**: Configuración de hooks de pre-commit (linting automático antes de commit)
- **Por qué en raíz**: `pre-commit` busca este archivo en el raíz
- **Uso**: `pre-commit install` (se ejecuta automáticamente en git commit)

#### `Makefile` ✅ **ÚTIL**
- **Qué es**: Comandos útiles del proyecto (atajos)
- **Por qué en raíz**: `make` busca `Makefile` en el raíz
- **Uso**: `make test`, `make lint`, `make install-dev`
- **Beneficio**: Comandos consistentes sin recordar flags complejos

### 📄 Documentación Legal

#### `LICENSE` ✅ **ESENCIAL**
- **Qué es**: Licencia del proyecto
- **Por qué en raíz**: Convención estándar, GitHub y otras plataformas lo buscan aquí
- **Contiene**: Texto completo de la licencia (CC0 en este caso)

## 📊 Resumen: ¿Deben estar en el raíz?

| Archivo | ¿En raíz? | Razón |
|---------|-----------|-------|
| `pyproject.toml` | ✅ **SÍ** | Estándar Python (PEP 518) |
| `setup.py` | ✅ **SÍ** | Compatibilidad con pip |
| `requirements.txt` | ✅ **SÍ** | Convención estándar |
| `requirements-dev.txt` | ✅ **SÍ** | Convención estándar |
| `Dockerfile` | ✅ **SÍ** | Docker lo busca aquí |
| `docker-compose.yml` | ✅ **SÍ** | docker-compose lo busca aquí |
| `.pre-commit-config.yaml` | ✅ **SÍ** | pre-commit lo busca aquí |
| `Makefile` | ✅ **SÍ** | make lo busca aquí |
| `LICENSE` | ✅ **SÍ** | Convención estándar |

## 🎯 Conclusión

**Todos estos archivos DEBEN estar en el raíz** porque:
1. Son estándares de la industria
2. Las herramientas los buscan específicamente en el raíz
3. Facilitan la adopción del proyecto por otros desarrolladores
4. Siguen convenciones reconocidas (Python, Docker, Git)

## 📚 Referencias

- [PEP 518 - Specifying Build Dependencies](https://peps.python.org/pep-0518/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Pre-commit Documentation](https://pre-commit.com/)

---

**Nota**: Si quieres reducir el "ruido visual" en el raíz, puedes:
- Usar un IDE que colapse archivos de configuración
- Crear un `.editorconfig` para organizar la vista
- Pero **NO muevas estos archivos** - romperías la compatibilidad
