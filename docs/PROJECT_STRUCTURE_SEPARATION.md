# Separación de Estructura: DT vs Proyectos

## Visión General

El sistema de Agents_Army mantiene una separación clara entre:
- **Archivos del DT**: Gestión del sistema multi-agente (tareas, reglas, configuración)
- **Archivos del Proyecto**: Código, documentación y assets específicos del proyecto

Esta separación permite:
- ✅ Múltiples proyectos sin conflictos
- ✅ Reutilización de reglas y configuración del DT
- ✅ Organización clara de archivos
- ✅ Facilidad para compartir o mover proyectos

## Estructura de Directorios

```
workspace/
├── .dt/                          # DT System Files (compartido entre proyectos)
│   ├── docs/                     # Documentación del sistema DT
│   ├── tasks/                    # Tareas del DT (gestión)
│   │   ├── pending/
│   │   ├── in-progress/
│   │   └── done/
│   ├── rules/                    # Reglas del sistema DT
│   │   ├── dt_rules.md
│   │   ├── delegation_rules.md
│   │   └── mandatory_rules.md
│   ├── config/                   # Configuración del DT
│   └── templates/                # Plantillas del DT
│
└── projects/                     # Proyectos Específicos
    ├── mi_proyecto/              # Proyecto 1
    │   ├── project.json          # Metadatos del proyecto
    │   ├── docs/
    │   │   └── prd.txt           # PRD del proyecto
    │   ├── src/                  # Código fuente del proyecto
    │   ├── tests/                # Tests del proyecto
    │   ├── assets/               # Assets del proyecto
    │   └── config/               # Configuración del proyecto
    │
    └── otro_proyecto/            # Proyecto 2
        ├── project.json
        ├── docs/
        ├── src/
        └── ...
```

## Reglas de Separación

### ✅ Archivos que van en `.dt/`

- **Tareas de gestión**: Archivos JSON de tareas asignadas por el DT
- **Reglas del sistema**: Reglas que aplican a todos los proyectos
- **Configuración del DT**: Configuración de agentes y sistema
- **Templates**: Plantillas reutilizables para tareas

### ✅ Archivos que van en `projects/{nombre_proyecto}/`

- **Código fuente**: Todo el código del proyecto (`src/`)
- **Documentación del proyecto**: PRD, especificaciones, README (`docs/`)
- **Tests**: Tests específicos del proyecto (`tests/`)
- **Assets**: Imágenes, recursos, datos (`assets/`)
- **Configuración del proyecto**: Config específica (`config/`)
- **Metadatos**: `project.json` con información del proyecto

## Inicialización de Proyectos

Cuando se crea un nuevo proyecto con `initialize_project()`:

```python
project = await dt.initialize_project(
    project_name="Mi Nuevo Proyecto",
    description="Descripción del proyecto",
    rules=["Regla 1", "Regla 2"],
    project_base_path=None  # Opcional: defaults a "projects/"
)
```

El sistema:
1. Crea la estructura en `projects/mi_nuevo_proyecto/`
2. Genera `project.json` con metadatos
3. Mantiene referencia al proyecto en el DT
4. Separa automáticamente archivos DT vs proyecto

## Comportamiento del DT y Agentes

### El DT debe entender:

1. **Rutas de proyecto**: Cuando se trabaja en un proyecto específico, todos los archivos del proyecto van en `projects/{nombre}/`
2. **Rutas del sistema**: Las tareas y gestión van en `.dt/`
3. **PRD del proyecto**: Siempre está en `projects/{nombre}/docs/prd.txt`
4. **Código del proyecto**: Siempre va en `projects/{nombre}/src/`

### Los agentes especializados deben:

- **Leer desde proyecto**: Código, docs, config del proyecto
- **Escribir en proyecto**: Nuevo código, documentación, assets
- **Consultar DT**: Reglas, tareas asignadas, configuración del sistema
- **Nunca mezclar**: No escribir código del proyecto en `.dt/`, no escribir gestión en `projects/`

## Ejemplo de Flujo

### 1. Crear Proyecto

```python
dt = DT(project_path=".dt")
project = await dt.initialize_project(
    project_name="E-commerce App",
    description="Aplicación de comercio electrónico"
)
# Crea: projects/e_commerce_app/
```

### 2. Crear PRD del Proyecto

```python
prd_path = project.prd_path  # projects/e_commerce_app/docs/prd.txt
prd_path.write_text("# PRD del proyecto...")
```

### 3. Parsear PRD y Generar Tareas

```python
tasks = await dt.parse_prd()  # Lee de projects/e_commerce_app/docs/prd.txt
# Tareas se guardan en .dt/tasks/ (gestión)
```

### 4. Agente Trabaja en Proyecto

```python
# Backend Architect recibe tarea
# Escribe código en: projects/e_commerce_app/src/
# Lee configuración de: projects/e_commerce_app/config/
# Consulta reglas de: .dt/rules/
```

## Migración de Proyectos Existentes

Si tienes proyectos existentes que mezclan archivos:

1. **Identificar archivos del proyecto**: Código, docs específicos, assets
2. **Crear estructura nueva**: `projects/{nombre}/`
3. **Mover archivos**: Proyecto → `projects/{nombre}/`
4. **Mantener DT**: `.dt/` queda para gestión
5. **Actualizar referencias**: Actualizar rutas en código/config

## Ventajas de Esta Separación

1. **Múltiples proyectos**: Cada proyecto tiene su espacio aislado
2. **Versionado claro**: Puedes hacer commit de proyectos por separado
3. **Compartir proyectos**: Fácil compartir solo `projects/{nombre}/`
4. **Backup selectivo**: Puedes hacer backup de proyectos específicos
5. **Limpieza fácil**: Eliminar proyecto = eliminar `projects/{nombre}/`
6. **Reutilización**: El DT y sus reglas se reutilizan entre proyectos

## Notas Importantes

⚠️ **Nunca mezclar**:
- No poner código del proyecto en `.dt/`
- No poner tareas/gestión en `projects/`
- No poner PRD del proyecto en `.dt/docs/`

✅ **Siempre separar**:
- Gestión del DT → `.dt/`
- Contenido del proyecto → `projects/{nombre}/`

## Referencias

- Ver `src/agents_army/agents/dt.py` para implementación
- Ver `docs/PROJECT_STRUCTURE.md` para estructura general
- Ver `docs/ENFOQUE_SIMPLIFICADO.md` para ejemplos de uso
