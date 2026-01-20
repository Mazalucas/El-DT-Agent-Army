# Preguntas Frecuentes (FAQ)

## 1. ¿Por qué Python?

### Razones Técnicas

**Python es ideal para este proyecto porque:**

1. **Ecosistema de IA/ML**
   - Librerías maduras para LLMs (OpenAI, Anthropic, LangChain)
   - Excelente soporte para async/await (necesario para agentes concurrentes)
   - Comunidad activa en IA

2. **Facilidad de Uso**
   - Sintaxis clara y legible
   - Type hints modernos (Python 3.10+)
   - Pydantic para validación de datos

3. **Ecosistema de Herramientas**
   - Testing robusto (pytest)
   - Linting y formatting (black, ruff, mypy)
   - Gestión de dependencias (pip, poetry)

4. **Interoperabilidad**
   - Fácil integración con APIs REST
   - Soporte para JSON/YAML nativo
   - Compatible con sistemas existentes

5. **Rapidez de Desarrollo**
   - Desarrollo rápido de prototipos
   - Fácil extensión y modificación
   - Ideal para frameworks modulares

### Alternativas Consideradas

- **TypeScript/Node.js**: Mejor para frontend, pero Python es superior para IA
- **Go/Rust**: Más performantes pero menos ecosistema de IA
- **Java**: Más verboso, menos popular en IA

**Conclusión**: Python es la mejor opción para un framework de agentes de IA en 2025.

---

## 2. ¿Qué Requerimientos Previos Necesito?

### Requisitos Mínimos

#### Sistema Operativo
- ✅ **Windows** 10/11
- ✅ **Linux** (Ubuntu 20.04+, Debian 11+, etc.)
- ✅ **macOS** 11+

#### Software Base
- **Python 3.10 o superior** (3.11+ recomendado)
- **pip** (incluido con Python)
- **git** (para clonar el repositorio)

#### Memoria y Espacio
- **RAM**: Mínimo 4GB (8GB+ recomendado)
- **Disco**: ~100MB para instalación base
- **Espacio adicional**: Depende del uso (memoria SQLite, proyectos, etc.)

### Verificar Requisitos

```bash
# Verificar Python
python --version  # Debe ser 3.10+

# Verificar pip
pip --version

# Verificar git (opcional)
git --version
```

### No Requerido (pero útil)

- **Entorno virtual** (recomendado pero no obligatorio)
- **IDE** (VS Code, PyCharm, etc.)
- **Docker** (solo para deployment avanzado)

---

## 3. ¿Requiere API Keys?

### Respuesta Corta: **SÍ, pero NO para empezar**

### Detalles

#### Para Testing y Desarrollo Básico
- ❌ **NO necesitas API keys** para:
  - Ejecutar tests (usan mocks)
  - Probar la estructura del framework
  - Ver ejemplos básicos
  - Entender el funcionamiento

#### Para Uso Real
- ✅ **SÍ necesitas API keys** para:
  - Usar agentes con LLMs reales
  - Generar contenido real
  - Ejecutar proyectos completos

### Qué API Keys Necesitas

**Opcional - Elige uno o más:**

1. **OpenAI API Key** (si usas GPT-4, GPT-3.5)
   - Obtener en: https://platform.openai.com/api-keys
   - Costo: Pay-per-use

2. **Anthropic API Key** (si usas Claude)
   - Obtener en: https://console.anthropic.com/
   - Costo: Pay-per-use

3. **Otros LLM Providers**
   - Puedes integrar cualquier provider
   - Solo necesitas implementar la interfaz `LLMProvider`

### Cómo Configurar API Keys

```python
# Opción 1: Variable de entorno
import os
os.environ["OPENAI_API_KEY"] = "tu-api-key"

# Opción 2: En código (no recomendado para producción)
from agents_army.core.agent import LLMProvider
import openai

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate(self, prompt: str, **kwargs):
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

# Usar
llm = OpenAIProvider(api_key="tu-api-key")
dt = DT(llm_provider=llm)
```

### Costos Estimados

- **Testing/Desarrollo**: $0 (usa mocks)
- **Uso básico**: $1-10/mes (depende del uso)
- **Producción**: Variable según volumen

---

## 4. Documentación: ¿Qué es Necesario vs Referencia?

### 📁 Estructura Propuesta

```
docs/
├── README.md                    # Overview y quick start
├── INSTALLATION.md              # Guía de instalación
├── USER_GUIDE.md                # Guía de usuario
├── ARCHITECTURE.md              # Arquitectura del sistema
├── PROTOCOL.md                  # Protocolo de comunicación
├── INTEGRATION.md               # Guía de integración
├── TROUBLESHOOTING.md           # Solución de problemas
```

### ✅ Documentación Necesaria (Mantener)

**Para Usuarios:**
1. **README.md** - Overview, quick start, estado
2. **INSTALLATION.md** - Cómo instalar
3. **USER_GUIDE.md** - Cómo usar el framework
4. **TROUBLESHOOTING.md** - Solución de problemas

**Para Desarrolladores:**
5. **ARCHITECTURE.md** - Diseño del sistema
6. **PROTOCOL.md** - Protocolo de comunicación
7. **INTEGRATION.md** - Cómo integrar
8. **SPECIFICATIONS_V2.md** - Especificaciones técnicas actuales

**Operacional:**
9. **TESTING_STRATEGY.md** - Estrategia de testing
10. **DEPLOYMENT.md** - Cómo desplegar (futuro)
11. **SECURITY.md** - Seguridad (futuro)
12. **MONITORING.md** - Observabilidad (futuro)
13. **COST_MANAGEMENT.md** - Gestión de costos (futuro)

### 📚 Documentación de Referencia

La documentación histórica ha sido eliminada para mantener solo lo esencial para el funcionamiento del framework.
10. **INDEX.md** - Índice (útil pero puede simplificarse)

### 🗂️ Propuesta de Reorganización

```
docs/
├── README.md                    # Overview
├── INSTALLATION.md              # Instalación
├── USER_GUIDE.md                # Guía de usuario
├── ARCHITECTURE.md              # Arquitectura
├── PROTOCOL.md                  # Protocolo
├── INTEGRATION.md               # Integración
├── TROUBLESHOOTING.md           # Troubleshooting
├── SPECIFICATIONS_V2.md         # Especificaciones actuales
├── TESTING_STRATEGY.md          # Testing
├── DEPLOYMENT.md                # Deployment (futuro)
├── SECURITY.md                  # Seguridad (futuro)
├── MONITORING.md                # Observabilidad (futuro)
├── COST_MANAGEMENT.md           # Costos (futuro)
    ├── INSPIRATION.md
    ├── RESEARCH.md
    ├── SPECIFICATIONS.md        # v1 deprecated
    ├── PLAN_REVIEW.md
    ├── CREWAI_LEARNINGS.md
    ├── TASKMASTER_RULES_INTEGRATION.md
    ├── DT_AUTONOMY.md
    ├── IMPLEMENTATION_PLAN.md
    ├── PROJECT_SUMMARY.md
    └── INDEX.md                 # Índice antiguo
```

---

## Resumen Rápido

### 1. ¿Por qué Python?
✅ Ecosistema de IA, async/await, Pydantic, facilidad de uso

### 2. Requerimientos
✅ Python 3.10+, pip, 4GB RAM mínimo

### 3. API Keys
❌ NO para testing/desarrollo básico
✅ SÍ para uso real con LLMs

### 4. Documentación
✅ Mantener: README, INSTALLATION, USER_GUIDE, ARCHITECTURE, PROTOCOL, INTEGRATION
📚 Documentación histórica eliminada - solo esencial

---

**Última actualización**: Enero 2025
