# Configuración del IDE para Agents_Army

## Archivos de Configuración Automática

Agents_Army incluye archivos de configuración que se cargan automáticamente en cada conversación del IDE, asegurando que **El DT esté presente y activo** en todo momento.

## Estructura de Archivos

```
proyecto/
├── .cursorrules                    # Reglas globales de Cursor (CARGADO AUTOMÁTICAMENTE)
├── .claude/
│   └── CLAUDE.md                   # Configuración para Claude Code (CARGADO AUTOMÁTICAMENTE)
└── .cursor/
    ├── commands/                   # Comandos personalizados
    │   └── dt-start.md
    └── rules/                      # Reglas específicas del DT
        ├── dt-activation.md        # Reglas de activación automática
        └── dt-rules.md            # Reglas del DT
```

## Archivos Principales

### 1. `.cursorrules` (Raíz del Proyecto)

**Propósito**: Reglas globales que Cursor carga automáticamente en cada conversación.

**Contenido**:
- Definición del rol del DT
- Principios fundamentales de Agents_Army
- Protocolos de comunicación
- Reglas de activación automática
- Referencias a documentación

**Carga**: Automática en cada conversación de Cursor

### 2. `.claude/CLAUDE.md`

**Propósito**: Configuración específica para Claude Code.

**Contenido**:
- Introducción a Agents_Army
- Rol del DT en el proyecto
- Estructura del proyecto
- Principios fundamentales
- Referencias importantes

**Carga**: Automática cuando se usa Claude Code

### 3. `.cursor/rules/dt-activation.md`

**Propósito**: Define cuándo y cómo el DT debe activarse automáticamente.

**Contenido**:
- Situaciones de activación automática
- Comportamiento esperado del DT
- Ejemplos de activación

**Carga**: Referenciado desde `.cursorrules`

### 4. `.cursor/rules/dt-rules.md`

**Propósito**: Reglas específicas del comportamiento del DT.

**Contenido**:
- Autonomía y autoridad del DT
- Protocolos de acción
- Reglas de priorización
- Comunicación

**Carga**: Referenciado desde `.cursorrules`

## Cómo Funciona la Activación Automática

### En Cursor

1. **Al iniciar conversación**: Cursor carga automáticamente `.cursorrules`
2. **El DT se activa** cuando detecta:
   - Decisiones arquitectónicas importantes
   - Creación/modificación de código significativo
   - Gestión de tareas o features
   - Necesidad de planificación
   - Validación de calidad

3. **Comportamiento del DT**:
   - Interviene activamente cuando es apropiado
   - Propone planes estructurados antes de ejecutar
   - Monitorea el progreso
   - Valida decisiones técnicas

### En Claude Code

1. **Al iniciar conversación**: Claude Code carga automáticamente `.claude/CLAUDE.md`
2. **El DT se activa** de la misma manera que en Cursor
3. **Comportamiento**: Similar a Cursor, adaptado al contexto de Claude Code

## Verificación de Configuración

### Verificar que los Archivos Existen

```bash
# Verificar archivos principales
ls -la .cursorrules
ls -la .claude/CLAUDE.md
ls -la .cursor/rules/dt-activation.md
ls -la .cursor/rules/dt-rules.md
```

### Probar Activación del DT

1. **Abre una nueva conversación** en tu IDE
2. **Menciona una decisión técnica importante**, por ejemplo:
   ```
   "Quiero crear un sistema de autenticación"
   ```
3. **El DT debería activarse** y:
   - Presentarse como El DT
   - Preguntar sobre requisitos específicos
   - Proponer un plan estructurado
   - Esperar aprobación antes de crear código

### Si el DT No Se Activa

1. **Verifica que los archivos existen** en la raíz del proyecto
2. **Reinicia el IDE** para que cargue los nuevos archivos
3. **Verifica la configuración del IDE**:
   - En Cursor: Settings → Rules → Verificar que `.cursorrules` está siendo leído
   - En Claude Code: Verificar que `.claude/CLAUDE.md` existe

## Personalización

### Modificar Reglas del DT

Puedes personalizar el comportamiento del DT editando:

1. **`.cursorrules`** - Para cambios globales
2. **`.cursor/rules/dt-rules.md`** - Para reglas específicas del DT
3. **`.cursor/rules/dt-activation.md`** - Para cambiar cuándo se activa

### Agregar Reglas Específicas del Proyecto

Crea archivos adicionales en `.cursor/rules/` y referéncialos desde `.cursorrules`.

## Comparación con Taskmaster

Agents_Army sigue un patrón similar a [Claude Taskmaster](https://github.com/eyaltoledano/claude-task-master):

| Aspecto | Taskmaster | Agents_Army |
|---------|-----------|-------------|
| Archivo principal | `.cursorrules` | `.cursorrules` |
| Configuración Claude | `.claude/CLAUDE.md` | `.claude/CLAUDE.md` |
| Reglas específicas | `.cursor/rules/` | `.cursor/rules/` |
| Activación automática | ✅ Sí | ✅ Sí |
| Carga en cada conversación | ✅ Sí | ✅ Sí |

## Referencias

- [DT Communication Guidelines](DT_COMMUNICATION_GUIDELINES.md) - Guías de comunicación del DT
- [Protocol](PROTOCOL.md) - Protocolo de mensajes entre agentes
- [Quick Start](QUICK_START.md) - Guía rápida de inicio

## Troubleshooting

### El DT no aparece en las conversaciones

1. Verifica que `.cursorrules` existe en la raíz del proyecto
2. Reinicia el IDE completamente
3. Verifica que no hay errores de sintaxis en `.cursorrules`
4. En Cursor, verifica Settings → Rules

### El DT no se activa cuando debería

1. Revisa `.cursor/rules/dt-activation.md` para ver las condiciones de activación
2. Asegúrate de mencionar explícitamente decisiones técnicas o tareas
3. Verifica que el proyecto tiene estructura `.dt/` si es necesario

### Los archivos no se cargan automáticamente

1. Verifica la ubicación de los archivos (deben estar en la raíz del proyecto)
2. Reinicia el IDE
3. Verifica la configuración del IDE según tu editor

---

**Última actualización**: Enero 2025  
**Estado**: Configuración Automática Implementada
