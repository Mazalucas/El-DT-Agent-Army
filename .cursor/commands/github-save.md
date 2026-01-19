# GitHub Save Workflow

## Objetivo
Ejecutar un workflow completo de Git para guardar cambios, crear un tag de versión y hacer push al repositorio remoto en la rama `main`.

## Pre-requisitos y Validaciones

### 1. Verificar Repositorio Git Inicializado
**Comando**: `git status`

**Validación**:
- Si el comando falla con "not a git repository": **DETENER** y avisar al usuario que necesita inicializar un repositorio con `git init` o navegar a un directorio con un repo existente.
- Si el comando funciona, continuar.

### 2. Verificar Autenticación con GitHub
**Comando**: `gh auth status`

**Validación**:
- Si el comando falla o muestra "not logged in": **DETENER** y avisar al usuario que necesita autenticarse con `gh auth login`.
- Si está autenticado, continuar.

### 3. Verificar Conexión con Remoto
**Comando**: `git remote -v`

**Validación**:
- Si no hay remoto configurado: **DETENER** y avisar al usuario que necesita agregar un remoto con `git remote add origin <url>`.
- Si hay remoto, continuar.

### 4. Verificar Estado de la Rama Local vs Remota
**Comando**: `git fetch origin` seguido de `git status`

**Validación**:
- Si `git status` muestra "Your branch is behind 'origin/main' by X commits": **ADVERTIR** al usuario que hay cambios remotos y recomendar hacer `git pull` antes de continuar.
- Si muestra "Your branch and 'origin/main' have diverged": **ADVERTIR** al usuario que necesita hacer merge o rebase.
- Si muestra "Your branch is ahead of 'origin/main'": continuar normalmente.
- Si muestra "Your branch is up to date with 'origin/main'": continuar normalmente.

## Workflow Principal

### Paso 1: Verificar Estado Actual
**Comando**: `git status`

**Acción**:
- Mostrar al usuario el estado actual del repositorio.
- Si no hay cambios para commitear: **DETENER** y avisar que no hay cambios para guardar.
- Si hay cambios sin agregar o sin commitear, continuar.

### Paso 2: Agregar Cambios al Staging
**Comando**: `git add .`

**Nota**: Esto agrega todos los cambios (nuevos, modificados y eliminados).

**Alternativa si el usuario quiere ser selectivo**: 
- Mostrar los archivos modificados con `git status --short`
- Preguntar al usuario si quiere agregar todos o archivos específicos
- Si específicos: `git add <archivo1> <archivo2> ...`

### Paso 3: Crear Commit
**Comando**: `git commit -m "<mensaje>"`

**Generación del mensaje de commit**:
- Analizar los cambios agregados con `git diff --cached --stat`
- Generar un mensaje descriptivo basado en los cambios:
  - Si hay nuevos archivos: mencionar "Add: ..."
  - Si hay modificaciones: mencionar "Update: ..."
  - Si hay eliminaciones: mencionar "Remove: ..."
  - Incluir un resumen breve de los cambios principales

**Formato sugerido**: `"<tipo>: <descripción breve>"`

**Ejemplos**:
- `"feat: Add new authentication module"`
- `"fix: Resolve memory leak in agent system"`
- `"docs: Update API documentation"`
- `"refactor: Improve code structure in core module"`

### Paso 4: Determinar Versión del Tag
**Comando**: `git describe --tags --abbrev=0` (para obtener el último tag)

**Lógica de versionado**:
- Si no hay tags previos: usar `v0.1.0` (primera versión)
- Si hay tags previos:
  - Analizar el último tag (formato esperado: `vX.Y.Z` o `X.Y.Z`)
  - Incrementar según el tipo de cambios:
    - **MAJOR** (X): Cambios incompatibles o breaking changes
    - **MINOR** (Y): Nuevas funcionalidades compatibles
    - **PATCH** (Z): Correcciones de bugs
- Si no se puede determinar automáticamente: **PREGUNTAR** al usuario qué versión desea usar.

**Formato del tag**: `v<MAJOR>.<MINOR>.<PATCH>` (ejemplo: `v1.2.3`)

### Paso 5: Crear Tag de Versión
**Comando**: `git tag -a <version> -m "Release <version>"`

**Ejemplo**: `git tag -a v1.2.3 -m "Release v1.2.3"`

**Nota**: Usar tag anotado (`-a`) para incluir metadata.

### Paso 6: Push de Commits y Tags
**Comandos**:
1. `git push origin main` - Push de commits
2. `git push origin <version>` - Push del tag específico

**O en un solo comando**:
- `git push origin main --tags` - Push de commits y todos los tags

**Validación**:
- Si el push falla por permisos: **DETENER** y avisar al usuario sobre problemas de autenticación.
- Si el push falla porque hay cambios remotos: **DETENER** y recomendar hacer `git pull --rebase` primero.
- Si el push es exitoso: confirmar al usuario.

## Resumen del Workflow Completo

```bash
# 1. Validaciones previas
git status                    # Verificar repo inicializado
gh auth status               # Verificar autenticación
git remote -v                # Verificar remoto configurado
git fetch origin            # Obtener estado remoto
git status                  # Verificar divergencias

# 2. Workflow principal
git status                  # Ver estado actual
git add .                   # Agregar cambios
git commit -m "<mensaje>"   # Crear commit
git tag -a <version> -m "Release <version>"  # Crear tag
git push origin main        # Push commits
git push origin <version>   # Push tag
```

## Manejo de Errores y Advertencias

### Error: No hay repositorio Git
**Mensaje**: "⚠️ Este directorio no es un repositorio Git. Por favor, inicializa uno con `git init` o navega a un directorio con un repositorio existente."

### Error: No autenticado en GitHub
**Mensaje**: "⚠️ No estás autenticado en GitHub CLI. Por favor, ejecuta `gh auth login` para autenticarte."

### Error: No hay remoto configurado
**Mensaje**: "⚠️ No hay un remoto configurado. Agrega uno con `git remote add origin <url-del-repositorio>`."

### Advertencia: Rama local detrás de remota
**Mensaje**: "⚠️ Tu rama local está detrás de 'origin/main' por X commits. Se recomienda hacer `git pull` antes de continuar para evitar conflictos. ¿Deseas continuar de todas formas?"

**Recomendación**: Si el usuario acepta continuar, hacer `git pull --rebase` antes del commit.

### Advertencia: Ramas divergentes
**Mensaje**: "⚠️ Tu rama local y 'origin/main' han divergido. Necesitas hacer merge o rebase. Opciones:\n1. `git pull --rebase` (recomendado para historial limpio)\n2. `git pull` (merge tradicional)\n¿Qué prefieres hacer?"

### Advertencia: No hay cambios para commitear
**Mensaje**: "ℹ️ No hay cambios para commitear. El repositorio está limpio."

### Error: Push fallido por permisos
**Mensaje**: "❌ El push falló por problemas de permisos. Verifica tu autenticación con `gh auth status` y tus permisos en el repositorio."

### Error: Push fallido por cambios remotos
**Mensaje**: "❌ El push falló porque hay cambios nuevos en el remoto. Ejecuta `git pull --rebase` y luego intenta el push nuevamente."

## Mejores Prácticas

1. **Siempre verificar estado antes de hacer cambios**: Ejecutar `git status` al inicio.
2. **Hacer pull antes de push**: Si hay cambios remotos, sincronizar primero.
3. **Mensajes de commit descriptivos**: Usar formato convencional (feat, fix, docs, etc.).
4. **Versionado semántico**: Seguir el formato `vMAJOR.MINOR.PATCH`.
5. **Tags anotados**: Usar `-a` para incluir metadata en los tags.
6. **Confirmar antes de push**: Mostrar resumen de cambios antes de hacer push.

## Notas Adicionales

- Este workflow asume que estás trabajando en la rama `main`. Si trabajas en otra rama, ajusta los comandos según corresponda.
- Para proyectos con múltiples ramas, considera hacer merge a `main` antes de hacer push.
- Los tags son inmutables una vez pusheados. Si necesitas cambiar un tag, elimínalo local y remoto, luego créalo nuevamente.
