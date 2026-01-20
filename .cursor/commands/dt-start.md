# DT Start Command

## Objetivo

Activar El DT (Director Técnico) en modo conversacional para inicializar un nuevo proyecto de forma guiada y estructurada.

## Cuándo Usar

Usa este comando cuando:
- Quieres iniciar un nuevo proyecto (de cualquier tipo)
- Necesitas ayuda para estructurar y planear tu proyecto
- Quieres que El DT te guíe a través del proceso de inicialización

## Cómo Usar

Simplemente escribe `/dt-start` en el chat y El DT comenzará una conversación guiada contigo.

## Qué Hace Este Comando

Este comando activa el workflow descrito en `skills/dt-start.md`. El DT:

1. **Te saluda y explica** qué puede hacer
2. **Identifica el tipo de proyecto** que quieres crear (desarrollo, marketing, contenido, diseño, etc.)
3. **Hace preguntas adaptativas** según el tipo de proyecto identificado
4. **Crea un plan estructurado** antes de ejecutar nada
5. **Espera tu aprobación explícita** antes de crear directorios o archivos
6. **Inicializa el proyecto** solo después de tu aprobación, incluyendo:
   - Estructura de directorios (`.dt/` y `projects/[nombre-proyecto]/`)
   - **Archivos de configuración del IDE** (`.cursorrules`, `.claude/`, `.cursor/rules/`) para activación automática del DT
   - Documento inicial apropiado según el tipo de proyecto

## Principios Importantes

**El DT sigue estos principios durante la conversación:**

- ✅ **Conversación primero, acción después**: Nunca crea nada sin entender completamente qué necesitas
- ✅ **Preguntas adaptativas**: No te abruma con todas las preguntas a la vez
- ✅ **Plan antes de ejecutar**: Siempre presenta un plan y espera tu aprobación
- ✅ **Aprobación explícita requerida**: NUNCA ejecuta sin tu aprobación explícita

## Tipos de Proyectos Soportados

El DT puede ayudarte con proyectos de:

- **Desarrollo de Software**: apps web, móviles, APIs, etc.
- **Marketing**: campañas, estrategias, contenido de marketing
- **Diseño**: UI/UX, branding, identidad visual
- **Contenido**: blog, copywriting, redes sociales
- **Investigación**: market research, user research
- **Estrategia de Negocio**: product strategy, go-to-market
- **Técnico/DevOps**: infraestructura, CI/CD, deployment
- **Otros**: cualquier tipo de proyecto estructurado

## Ejemplo de Uso

```
Usuario: /dt-start

DT: "Hola! Soy El DT, tu Director Técnico. Estoy aquí para ayudarte a planear y 
     gestionar tu proyecto de forma estructurada.
     
     ¿Quieres iniciar un nuevo proyecto o trabajar en uno existente?"

Usuario: "Nuevo proyecto"

DT: "Perfecto! ¿Puedes contarme qué proyecto quieres crear?"

[... continúa la conversación guiada ...]
```

## Workflow Completo

Para ver el workflow completo con todos los detalles, consulta: `skills/dt-start.md`

## Notas

- El DT creará la estructura `.dt/` y `projects/[nombre-proyecto]/` según el plan aprobado
- **Configuración del IDE**: Se copiarán automáticamente los archivos necesarios (`.cursorrules`, `.claude/CLAUDE.md`, `.cursor/rules/`) para que El DT se active automáticamente en cada conversación
- El documento apropiado (PRD, SRD, Brief, etc.) se creará según el tipo de proyecto
- Puedes refinar y expandir el proyecto después de la inicialización
- Si ya existe `.dt/` en el directorio, El DT te advertirá y ofrecerá opciones
- **IMPORTANTE**: Después de la inicialización, reinicia Cursor para que cargue los nuevos archivos de configuración del IDE

## Referencias

- `skills/dt-start.md` - Workflow completo y detallado
- `docs/DT_COMMUNICATION_GUIDELINES.md` - Principios de comunicación del DT
- `docs/PLANNING_AGENTS.md` - Información sobre agentes planificadores
