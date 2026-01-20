# GitHub Sync Workflow

## Objetivo
Sincronizar el repositorio local con el remoto, haciendo pull de cambios y manejando merges cuando sea necesario de forma automática y segura.

## Pre-requisitos y Validaciones

### 1. Verificar Repositorio Git Inicializado
**Comando**: `git status`

**Validación**:
- Si el comando falla con "not a git repository": **DETENER** y avisar al usuario que necesita inicializar un repositorio con `git init` o navegar a un directorio con un repo existente.
- Si el comando funciona, continuar.

### 2. Verificar Conexión con Remoto
**Comando**: `git remote -v`

**Validación**:
- Si no hay remoto configurado: **DETENER** y avisar al usuario que necesita agregar un remoto con `git remote add origin <url>`.
- Si hay remoto, continuar.

### 3. Verificar Estado de Cambios Locales Sin Commitear
**Comando**: `git status`

**Validación**:
- Si hay cambios sin commitear (modified, untracked files): **ADVERTIR** al usuario que tiene cambios locales sin guardar.
- **Opciones**:
  1. Hacer commit de los cambios locales primero (recomendado)
  2. Hacer stash de los cambios (`git stash`)
  3. Continuar de todas formas (puede causar conflictos)

## Workflow Principal

### Paso 1: Obtener Estado Remoto
**Comando**: `git fetch origin`

**Acción**:
- Obtener información sobre cambios en el remoto sin modificar el working directory.
- Esto permite comparar el estado local vs remoto sin riesgo.

### Paso 2: Analizar Estado Local vs Remoto
**Comando**: `git status`

**Análisis de Estados**:

#### Caso 1: Repositorio Actualizado
**Mensaje**: "Your branch is up to date with 'origin/main'"
- **Acción**: ✅ **COMPLETAR** - No hay cambios que sincronizar.
- **Mensaje al usuario**: "✅ Tu repositorio local está sincronizado con el remoto. No hay cambios para traer."

#### Caso 2: Rama Local Detrás del Remoto
**Mensaje**: "Your branch is behind 'origin/main' by X commits"
- **Acción**: Proceder con **Paso 3: Pull Simple** (sin conflictos esperados).

#### Caso 3: Rama Local Adelantada del Remoto
**Mensaje**: "Your branch is ahead of 'origin/main' by X commits"
- **Acción**: ✅ **COMPLETAR** - No hay cambios remotos que traer.
- **Mensaje al usuario**: "ℹ️ Tu rama local tiene commits que no están en el remoto. Usa `github-save` si quieres hacer push de estos cambios."

#### Caso 4: Ramas Divergentes
**Mensaje**: "Your branch and 'origin/main' have diverged"
- **Acción**: Proceder con **Paso 4: Manejo de Divergencias**.

### Paso 3: Pull Simple (Sin Conflictos Esperados)
**Comando**: `git pull origin main`

**Cuándo usar**:
- Cuando la rama local está detrás del remoto.
- Cuando no hay cambios locales sin commitear (o están en stash).

**Validación**:
- Si el pull es exitoso: ✅ **COMPLETAR** - Sincronización exitosa.
- Si hay conflictos: Proceder con **Paso 5: Resolución de Conflictos**.

**Mensaje de éxito**: "✅ Sincronización completada. Se trajeron X commits del remoto."

### Paso 4: Manejo de Divergencias

Cuando las ramas local y remota han divergido, hay dos estrategias principales:

#### Estrategia A: Merge (Recomendado para la mayoría de casos)
**Comando**: `git pull origin main` (o `git pull --no-rebase`)

**Cuándo usar**:
- Cuando trabajas en equipo y quieres preservar el historial completo.
- Cuando los cambios locales y remotos son independientes.
- Cuando prefieres un historial más explícito de merges.

**Ventajas**:
- Preserva el historial completo de ambas ramas.
- Más seguro y fácil de entender.
- No reescribe commits existentes.

**Desventajas**:
- Crea commits de merge adicionales.
- Historial puede volverse más complejo.

#### Estrategia B: Rebase (Recomendado para historial limpio)
**Comando**: `git pull --rebase origin main`

**Cuándo usar**:
- Cuando quieres mantener un historial lineal y limpio.
- Cuando trabajas solo o en ramas de feature.
- Cuando los cambios locales son pequeños y recientes.

**Ventajas**:
- Historial lineal y más fácil de leer.
- No crea commits de merge adicionales.
- Mejor para revisar cambios.

**Desventajas**:
- Reescribe el historial (cambia SHAs de commits).
- Puede ser más complejo si hay conflictos múltiples.

#### Decisión Automática Recomendada

**Lógica de decisión**:
1. **Si hay cambios locales sin commitear**: Usar **Merge** (más seguro).
2. **Si los commits locales son recientes (< 3 commits)**: Usar **Rebase** (historial limpio).
3. **Si los commits locales son antiguos (> 3 commits)**: Usar **Merge** (evitar reescribir mucho historial).
4. **Si el usuario prefiere historial explícito**: Usar **Merge**.
5. **Si el usuario prefiere historial limpio**: Usar **Rebase**.

**Por defecto**: Usar **Merge** (más seguro y predecible).

**Mensaje al usuario antes de ejecutar**:
```
⚠️ Las ramas local y remota han divergido.
📊 Cambios locales: X commits
📊 Cambios remotos: Y commits

Estrategia recomendada: Merge (más seguro)
¿Proceder con merge? (S/n)
```

Si el usuario prefiere rebase, usar `git pull --rebase origin main`.

### Paso 5: Resolución de Conflictos

Si durante el pull (merge o rebase) aparecen conflictos:

**Comando para ver conflictos**: `git status`

**Archivos en conflicto**:
- Git mostrará qué archivos tienen conflictos.
- Mostrar al usuario la lista de archivos conflictivos.

**Opciones de Resolución**:

#### Opción 1: Resolución Manual (Recomendado)
**Pasos**:
1. Abrir archivos conflictivos en el editor.
2. Buscar marcadores de conflicto: `<<<<<<<`, `=======`, `>>>>>>>`
3. Decidir qué código mantener (local, remoto, o combinación).
4. Eliminar marcadores de conflicto.
5. Guardar archivos.

**Comandos después de resolver**:
- Si fue merge: `git add <archivos-resueltos>` luego `git commit`
- Si fue rebase: `git add <archivos-resueltos>` luego `git rebase --continue`

#### Opción 2: Aceptar Versión Local
**Comando**: `git checkout --ours <archivo>` (para merge) o `git checkout --theirs <archivo>` (para rebase)

**Cuándo usar**: Cuando estás seguro de que tu versión local es la correcta.

#### Opción 3: Aceptar Versión Remota
**Comando**: `git checkout --theirs <archivo>` (para merge) o `git checkout --ours <archivo>` (para rebase)

**Cuándo usar**: Cuando estás seguro de que la versión remota es la correcta.

#### Opción 4: Abortar Merge/Rebase
**Comandos**:
- Si fue merge: `git merge --abort`
- Si fue rebase: `git rebase --abort`

**Cuándo usar**: Cuando los conflictos son demasiado complejos y prefieres resolverlos manualmente después.

**Mensaje al usuario**:
```
❌ Se encontraron conflictos durante la sincronización.
📝 Archivos con conflictos:
   - archivo1.py
   - archivo2.py

Opciones:
1. Resolver manualmente (recomendado)
2. Aceptar versión local para todos
3. Aceptar versión remota para todos
4. Abortar y resolver después

¿Qué prefieres hacer?
```

### Paso 6: Verificación Final
**Comando**: `git status`

**Validación**:
- Si muestra "Your branch is up to date with 'origin/main'": ✅ **COMPLETAR** - Sincronización exitosa.
- Si aún hay conflictos: Volver a **Paso 5**.
- Si hay cambios sin commitear de la resolución: Recordar al usuario que debe hacer commit.

**Mensaje de éxito final**:
```
✅ Sincronización completada exitosamente.
📊 Estado: Tu rama local está actualizada con origin/main.
```

## Resumen del Workflow Completo

```bash
# 1. Validaciones previas
git status                    # Verificar repo y cambios locales
git remote -v                 # Verificar remoto configurado

# 2. Obtener estado remoto
git fetch origin              # Obtener información sin modificar

# 3. Analizar estado
git status                    # Ver relación local vs remoto

# 4. Sincronizar según el caso:
#    - Si está detrás: git pull origin main
#    - Si divergió: git pull origin main (merge) o git pull --rebase origin main
#    - Si hay conflictos: resolver y continuar

# 5. Verificación final
git status                    # Confirmar sincronización exitosa
```

## Manejo de Errores y Advertencias

### Error: No hay repositorio Git
**Mensaje**: "⚠️ Este directorio no es un repositorio Git. Por favor, inicializa uno con `git init` o navega a un directorio con un repositorio existente."

### Error: No hay remoto configurado
**Mensaje**: "⚠️ No hay un remoto configurado. Agrega uno con `git remote add origin <url-del-repositorio>`."

### Advertencia: Cambios locales sin commitear
**Mensaje**: "⚠️ Tienes cambios locales sin commitear. Opciones:\n1. Hacer commit primero (recomendado)\n2. Hacer stash (`git stash`)\n3. Continuar de todas formas (puede causar conflictos)\n¿Qué prefieres hacer?"

### Error: Pull fallido por permisos
**Mensaje**: "❌ El pull falló por problemas de permisos. Verifica tu autenticación y tus permisos en el repositorio."

### Error: Pull fallido por cambios remotos conflictivos
**Mensaje**: "❌ El pull falló. Hay conflictos que requieren resolución manual. Ver 'Paso 5: Resolución de Conflictos'."

### Advertencia: Rebase en progreso
**Mensaje**: "⚠️ Hay un rebase en progreso. Opciones:\n1. Continuar: `git rebase --continue`\n2. Abortar: `git rebase --abort`"

### Advertencia: Merge en progreso
**Mensaje**: "⚠️ Hay un merge en progreso. Opciones:\n1. Completar: Resolver conflictos y hacer `git commit`\n2. Abortar: `git merge --abort`"

## Mejores Prácticas

1. **Siempre hacer fetch primero**: Usar `git fetch` antes de `git pull` para ver qué va a pasar sin modificar nada.
2. **Commitear cambios locales antes de pull**: Evita conflictos innecesarios.
3. **Usar stash para cambios temporales**: Si tienes cambios que no quieres commitear aún, usa `git stash`.
4. **Merge vs Rebase**: 
   - Usa **Merge** para trabajo en equipo y preservar historial completo.
   - Usa **Rebase** para historial limpio cuando trabajas solo o en features.
5. **Resolver conflictos inmediatamente**: No dejes conflictos sin resolver.
6. **Verificar estado después de sync**: Siempre ejecuta `git status` al final para confirmar éxito.

## Estrategias de Merge Recomendadas por Escenario

### Escenario 1: Trabajo Individual
- **Estrategia**: Rebase (historial limpio)
- **Comando**: `git pull --rebase origin main`

### Escenario 2: Trabajo en Equipo
- **Estrategia**: Merge (preservar historial)
- **Comando**: `git pull origin main`

### Escenario 3: Rama de Feature
- **Estrategia**: Rebase (antes de merge a main)
- **Comando**: `git pull --rebase origin main`

### Escenario 4: Rama Principal (main/master)
- **Estrategia**: Merge (más seguro y explícito)
- **Comando**: `git pull origin main`

### Escenario 5: Cambios Locales Importantes
- **Estrategia**: Merge (evitar reescribir historial importante)
- **Comando**: `git pull origin main`

## Notas Adicionales

- Este workflow asume que estás trabajando en la rama `main`. Si trabajas en otra rama, ajusta los comandos según corresponda.
- Para ramas específicas: `git pull origin <nombre-rama>`
- El comando `git pull` es equivalente a `git fetch` seguido de `git merge` (o `git rebase` si usas `--rebase`).
- Si prefieres más control, puedes hacer `git fetch` y luego decidir manualmente si hacer `git merge` o `git rebase`.
- Los conflictos son normales en trabajo colaborativo. Resuélvelos con cuidado y comunica cambios importantes al equipo.
