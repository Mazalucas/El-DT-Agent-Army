# Estrategia de Despliegue: Agents_Army

## Visión General

Este documento define la estrategia completa de despliegue para **Agents_Army**, incluyendo desarrollo, staging, producción, CI/CD, y operaciones.

## Estrategias de Despliegue

### 1. Desarrollo Local

**Objetivo**: Desarrollo y testing local.

**Stack**:
```yaml
development:
  runtime: "python 3.10+"
  dependencies: "requirements-dev.txt"
  database: "sqlite"
  memory_backend: "in_memory"
  monitoring: "local_logs"
  
  setup:
    - "pip install -r requirements-dev.txt"
    - "python -m agents_army init"
    - "python -m agents_army serve --dev"
```

**Docker Compose** (opcional):
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  agents_army:
    build: .
    volumes:
      - .:/app
      - ./.taskmaster:/app/.taskmaster
    environment:
      - ENV=development
      - DEBUG=true
    ports:
      - "8000:8000"
  
  memory_db:
    image: postgres:15
    environment:
      - POSTGRES_DB=agents_army_dev
    volumes:
      - memory_data:/var/lib/postgresql/data
```

### 2. Staging

**Objetivo**: Testing en ambiente similar a producción.

**Stack**:
```yaml
staging:
  platform: "cloud_run"  # o ECS, Kubernetes
  database: "cloud_sql"
  memory_backend: "postgresql"
  monitoring: "cloud_monitoring"
  
  deployment:
    strategy: "rolling"
    health_check: "/health"
    min_instances: 1
    max_instances: 3
```

### 3. Producción

**Objetivo**: Ambiente de producción con alta disponibilidad.

**Stack**:
```yaml
production:
  platform: "cloud_run"  # o Kubernetes
  database: "cloud_sql_ha"
  memory_backend: "postgresql_ha"
  monitoring: "full_observability"
  
  deployment:
    strategy: "blue-green"
    health_check: "/health"
    readiness_probe: "/ready"
    liveness_probe: "/live"
    min_instances: 2
    max_instances: 10
    auto_scaling: true
```

## Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear usuario no-root
RUN useradd -m -u 1000 agent && \
    chown -R agent:agent /app
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -m agents_army health

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "-m", "agents_army", "serve"]
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: |
          pytest tests/ --cov=agents_army --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run linters
        run: |
          ruff check .
          black --check .
          mypy agents_army/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: |
          pip install safety
          safety check

  build:
    needs: [test, lint, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t agents-army:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker tag agents-army:${{ github.sha }} gcr.io/$PROJECT/agents-army:${{ github.sha }}
          docker push gcr.io/$PROJECT/agents-army:${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          gcloud run deploy agents-army-staging \
            --image gcr.io/$PROJECT/agents-army:${{ github.sha }} \
            --region us-central1 \
            --platform managed

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          gcloud run deploy agents-army \
            --image gcr.io/$PROJECT/agents-army:${{ github.sha }} \
            --region us-central1 \
            --platform managed \
            --no-traffic \
            --tag blue
          
          # Health check
          sleep 30
          curl -f https://agents-army.run.app/health || exit 1
          
          # Switch traffic
          gcloud run services update-traffic agents-army \
            --to-latest
```

## Health Checks

```python
# agents_army/health.py
from fastapi import APIRouter, status
from agents_army.core.system import AgentSystem

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check básico.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/ready")
async def readiness_check():
    """
    Readiness check - verifica que el sistema está listo.
    """
    system = AgentSystem.get_instance()
    
    checks = {
        "agents_loaded": system.agents_loaded(),
        "memory_connected": system.memory_connected(),
        "tools_registered": system.tools_registered()
    }
    
    if all(checks.values()):
        return {
            "status": "ready",
            "checks": checks
        }
    else:
        return Response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "checks": checks
            }
        )

@router.get("/live")
async def liveness_check():
    """
    Liveness check - verifica que el proceso está vivo.
    """
    return {
        "status": "alive",
        "pid": os.getpid()
    }
```

## Estrategia de Versionado

### Semantic Versioning

```yaml
versioning:
  format: "semantic"  # major.minor.patch
  examples:
    - "1.0.0"  # Release inicial
    - "1.1.0"  # Nueva feature
    - "1.1.1"  # Bug fix
    - "2.0.0"  # Breaking change
  
  agent_versioning:
    format: "semantic"
    independent: true  # Cada agente puede versionarse independientemente
  
  rules_versioning:
    format: "semantic"
    migration: "automatic"  # Migración automática cuando sea posible
```

### Versionado de Agentes

```python
@dataclass
class AgentVersion:
    agent_id: str
    version: str  # "1.2.3"
    compatible_with: List[str]  # Versiones compatibles del sistema
    breaking_changes: List[str]  # Cambios incompatibles
    
class AgentVersionManager:
    async def upgrade_agent(
        self,
        agent_id: str,
        target_version: str
    ) -> UpgradeResult:
        """
        Actualiza un agente a nueva versión.
        """
        # Verificar compatibilidad
        # Migrar configuración si es necesario
        # Actualizar agente
        # Validar funcionamiento
```

## Rollback Strategy

```python
class RollbackManager:
    async def rollback(
        self,
        target_version: str,
        reason: str
    ) -> RollbackResult:
        """
        Hace rollback a versión anterior.
        """
        # 1. Detener tráfico nuevo
        # 2. Verificar versión anterior disponible
        # 3. Desplegar versión anterior
        # 4. Validar health checks
        # 5. Reanudar tráfico
        # 6. Notificar
```

## Auto-scaling

```yaml
auto_scaling:
  enabled: true
  min_instances: 2
  max_instances: 10
  target_cpu: 70
  target_memory: 80
  target_requests: 100  # requests per second
  
  scaling_policy:
    scale_up:
      threshold: 80
      cooldown: 60s
      increment: 1
    
    scale_down:
      threshold: 30
      cooldown: 300s
      decrement: 1
```

## Monitoring en Producción

```yaml
monitoring:
  metrics:
    - cpu_usage
    - memory_usage
    - request_rate
    - error_rate
    - latency
    - agent_performance
    - cost_per_request
  
  alerts:
    - name: "high_error_rate"
      condition: "error_rate > 5%"
      action: "notify_team"
    
    - name: "high_latency"
      condition: "p95_latency > 5s"
      action: "scale_up"
    
    - name: "agent_failure"
      condition: "agent_error_rate > 10%"
      action: "alert_dt"
```

## Secret Management

```yaml
secrets:
  backend: "google_secret_manager"  # o AWS Secrets, Vault
  
  secrets:
    - name: "OPENAI_API_KEY"
      required: true
      rotation: "manual"
    
    - name: "DATABASE_PASSWORD"
      required: true
      rotation: "automatic"
      interval: "90d"
```

## Backup y Recovery

```yaml
backup:
  database:
    frequency: "daily"
    retention: "30d"
    location: "cloud_storage"
  
  memory:
    frequency: "hourly"
    retention: "7d"
  
  configuration:
    frequency: "on_change"
    retention: "90d"
  
  recovery:
    rpo: "1h"  # Recovery Point Objective
    rto: "15m"  # Recovery Time Objective
```

## Checklist de Despliegue

### Pre-despliegue
- [ ] Tests pasan
- [ ] Linting pasa
- [ ] Security scan pasa
- [ ] Documentación actualizada
- [ ] Changelog actualizado
- [ ] Version bump

### Despliegue
- [ ] Build de imagen exitoso
- [ ] Push a registry exitoso
- [ ] Health checks pasan
- [ ] Smoke tests pasan
- [ ] Monitoring configurado

### Post-despliegue
- [ ] Verificar logs
- [ ] Verificar métricas
- [ ] Verificar funcionalidad end-to-end
- [ ] Notificar equipo

---

**Última actualización**: Enero 2025  
**Estado**: Estrategia Definida
