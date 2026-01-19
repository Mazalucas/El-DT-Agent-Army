# Plan de Reorganización de Documentación

## Objetivo

Limpiar y organizar la documentación separando:
- **Documentación esencial** para usar el proyecto
- **Documentación de referencia** (inspiración, investigación, planes completados)

## Estructura Propuesta

```
docs/
├── README.md                    # Overview y quick start
├── REQUIREMENTS.md              # Requisitos y configuración
├── INSTALLATION.md              # Guía de instalación
├── USER_GUIDE.md                # Guía de usuario
├── ARCHITECTURE.md              # Arquitectura del sistema
├── PROTOCOL.md                  # Protocolo de comunicación
├── INTEGRATION.md               # Guía de integración
├── TROUBLESHOOTING.md           # Solución de problemas
├── SPECIFICATIONS_V2.md         # Especificaciones técnicas actuales
├── TESTING_STRATEGY.md          # Estrategia de testing
├── DEPLOYMENT.md                # Deployment (futuro)
├── SECURITY.md                  # Seguridad (futuro)
├── MONITORING.md                # Observabilidad (futuro)
├── COST_MANAGEMENT.md           # Gestión de costos (futuro)
├── FAQ.md                       # Preguntas frecuentes
└── archive/                     # Documentación de referencia
    ├── INSPIRATION.md           # Fuentes de inspiración
    ├── RESEARCH.md              # Investigación inicial
    ├── SPECIFICATIONS.md        # Especificaciones v1 (deprecated)
    ├── PLAN_REVIEW.md           # Revisión del plan
    ├── CREWAI_LEARNINGS.md      # Lecciones de CrewAI
    ├── TASKMASTER_RULES_INTEGRATION.md
    ├── DT_AUTONOMY.md           # Autonomía del DT (detalle avanzado)
    ├── IMPLEMENTATION_PLAN.md   # Plan de implementación (completado)
    ├── PROJECT_SUMMARY.md       # Resumen del proyecto
    └── INDEX.md                 # Índice antiguo
```

## Documentos a Mover a archive/

1. ✅ **INSPIRATION.md** - Fuentes de inspiración (útil pero no esencial)
2. ✅ **RESEARCH.md** - Investigación inicial (útil pero no esencial)
3. ✅ **SPECIFICATIONS.md** - Especificaciones v1 (deprecated)
4. ✅ **PLAN_REVIEW.md** - Revisión del plan (completado)
5. ✅ **CREWAI_LEARNINGS.md** - Lecciones aprendidas (referencia)
6. ✅ **TASKMASTER_RULES_INTEGRATION.md** - Integración de reglas (referencia)
7. ✅ **DT_AUTONOMY.md** - Autonomía del DT (detalle avanzado)
8. ✅ **IMPLEMENTATION_PLAN.md** - Plan de implementación (completado)
9. ✅ **PROJECT_SUMMARY.md** - Resumen del proyecto (útil pero no esencial)
10. ✅ **INDEX.md** - Índice antiguo (puede simplificarse)

## Documentos a Mantener en docs/

1. ✅ **README.md** - Overview (si existe, o crear)
2. ✅ **REQUIREMENTS.md** - Requisitos (nuevo)
3. ✅ **INSTALLATION.md** - Instalación
4. ✅ **USER_GUIDE.md** - Guía de usuario
5. ✅ **ARCHITECTURE.md** - Arquitectura
6. ✅ **PROTOCOL.md** - Protocolo
7. ✅ **INTEGRATION.md** - Integración
8. ✅ **TROUBLESHOOTING.md** - Troubleshooting
9. ✅ **SPECIFICATIONS_V2.md** - Especificaciones actuales
10. ✅ **TESTING_STRATEGY.md** - Testing
11. ✅ **DEPLOYMENT.md** - Deployment
12. ✅ **SECURITY.md** - Seguridad
13. ✅ **MONITORING.md** - Observabilidad
14. ✅ **COST_MANAGEMENT.md** - Costos
15. ✅ **FAQ.md** - Preguntas frecuentes (nuevo)
16. ✅ **ROLES.md** - Roles (mantener, es útil)

## Acciones a Realizar

### Paso 1: Crear directorio archive/
```bash
mkdir docs/archive
```

### Paso 2: Mover documentos a archive/
```bash
# Mover documentos de referencia
mv docs/INSPIRATION.md docs/archive/
mv docs/RESEARCH.md docs/archive/
mv docs/SPECIFICATIONS.md docs/archive/
mv docs/PLAN_REVIEW.md docs/archive/
mv docs/CREWAI_LEARNINGS.md docs/archive/
mv docs/TASKMASTER_RULES_INTEGRATION.md docs/archive/
mv docs/DT_AUTONOMY.md docs/archive/
mv docs/IMPLEMENTATION_PLAN.md docs/archive/
mv docs/PROJECT_SUMMARY.md docs/archive/
mv docs/INDEX.md docs/archive/
```

### Paso 3: Crear nuevos documentos
- ✅ `docs/REQUIREMENTS.md` - Creado
- ✅ `docs/FAQ.md` - Creado

### Paso 4: Actualizar referencias
- Actualizar README.md con nueva estructura
- Actualizar links en documentos que referencien archivos movidos

## Beneficios

1. **Claridad**: Documentación esencial separada de referencia
2. **Navegación**: Más fácil encontrar lo necesario
3. **Mantenimiento**: Menos confusión sobre qué es actual
4. **Profesionalismo**: Estructura más limpia para compartir

## Notas

- Los documentos en `archive/` siguen siendo útiles para entender el contexto
- Pueden consultarse cuando sea necesario
- No son necesarios para usar el framework
- Pueden eliminarse si se desea (pero recomendado mantenerlos)
