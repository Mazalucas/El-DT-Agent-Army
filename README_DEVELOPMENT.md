# Guía de Desarrollo: Agents_Army

## Setup Inicial

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Agents_Army.git
cd Agents_Army
```

### 2. Crear Entorno Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
# Desarrollo
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install
```

### 4. Verificar Instalación

```bash
# Ejecutar tests
pytest tests/ -v

# Verificar linting
make lint
```

## Estructura del Proyecto

```
Agents_Army/
├── src/
│   └── agents_army/          # Código fuente principal
│       ├── core/             # Componentes core
│       ├── agents/           # Implementaciones de agentes
│       ├── memory/           # Sistema de memoria
│       ├── tools/            # Herramientas
│       └── protocol/         # Protocolos de comunicación
├── tests/                     # Tests
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   ├── e2e/                  # E2E tests
│   └── fixtures/             # Fixtures y mocks
├── docs/                      # Documentación
├── .github/                   # GitHub Actions
└── requirements*.txt          # Dependencias
```

## Comandos Útiles

### Testing

```bash
# Todos los tests
pytest tests/ -v

# Solo unit tests
pytest tests/unit/ -v

# Con cobertura
pytest tests/ -v --cov=agents_army --cov-report=html

# Tests específicos
pytest tests/unit/test_version.py -v
```

### Code Quality

```bash
# Formatear código
make format

# Verificar linting
make lint

# Type checking
make type-check
```

### Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e .

# Limpiar artefactos
make clean
```

## Flujo de Trabajo

1. **Crear branch**: `git checkout -b feature/nueva-funcionalidad`
2. **Desarrollar**: Implementar cambios
3. **Tests**: Asegurar que tests pasan
4. **Linting**: `make format && make lint`
5. **Commit**: `git commit -m "feat: nueva funcionalidad"`
6. **Push**: `git push origin feature/nueva-funcionalidad`
7. **PR**: Crear Pull Request

## Convenciones

### Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `test:` Tests
- `refactor:` Refactorización
- `chore:` Mantenimiento

### Código

- Type hints obligatorios
- Docstrings en todas las funciones públicas
- Tests para nueva funcionalidad
- Seguir PEP 8 (con black)

## Próximos Pasos

Ver [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) para el plan completo de implementación.
