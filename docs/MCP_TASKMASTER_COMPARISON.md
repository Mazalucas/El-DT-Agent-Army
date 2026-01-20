# Comparación: Agents Army MCP vs Taskmaster MCP

Este documento compara la implementación del servidor MCP de Agents Army con la de Taskmaster para asegurar compatibilidad y funcionalidad correcta.

## Estructura de Configuración MCP

### Taskmaster
```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
        ...
      }
    }
  }
}
```

### Agents Army
```json
{
  "mcpServers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        ...
      }
    }
  }
}
```

## Diferencias Clave

| Aspecto | Taskmaster | Agents Army |
|--------|-----------|-------------|
| **Runtime** | Node.js (npx) | Python |
| **Punto de entrada** | `dist/mcp-server.js` | `src/agents_army/mcp/__main__.py` |
| **Framework MCP** | FastMCP (JavaScript) | FastMCP (Python) |
| **Transporte** | stdio | stdio |
| **Comando** | `npx task-master-ai` | `python -m agents_army.mcp` |

## Similitudes

✅ Ambos usan **FastMCP** como framework  
✅ Ambos usan **stdio** como transporte  
✅ Ambos exponen herramientas (tools) vía MCP  
✅ Ambos requieren API keys en el bloque `env`  
✅ Ambos se configuran en `.cursor/mcp.json` (Cursor) o equivalente  

## Estructura de Archivos

### Taskmaster
```
task-master-ai/
├── dist/
│   └── mcp-server.js          # Punto de entrada ejecutable
├── mcp-server/
│   └── src/
│       └── tools/
│           └── index.js       # Registro de herramientas
└── package.json
```

### Agents Army
```
agents_army/
├── mcp/
│   ├── __init__.py
│   ├── __main__.py            # Punto de entrada ejecutable
│   ├── server.py              # Clase MCPServer
│   ├── client.py
│   └── models.py
└── ...
```

## Verificación de Funcionamiento

### Cómo verificar que Taskmaster funciona:
1. Configurar `.cursor/mcp.json` con el comando `npx`
2. Habilitar en Cursor Settings → MCP
3. Verificar que las herramientas aparecen en el cliente MCP

### Cómo verificar que Agents Army funciona:
1. Configurar `.cursor/mcp.json` con el comando `python -m agents_army.mcp`
2. Habilitar en Cursor Settings → MCP
3. Verificar que las herramientas aparecen en el cliente MCP

### Comando de prueba manual:

**Taskmaster:**
```bash
npx -y --package=task-master-ai task-master-ai
```

**Agents Army:**
```bash
python -m agents_army.mcp
```

Ambos deberían iniciar el servidor MCP y esperar comandos por stdio.

## Herramientas Expuestas

### Taskmaster
- ~36 herramientas por defecto
- Gestión de tareas (init, parse-prd, list, next, expand, etc.)
- Investigación
- Configuración de proyectos

### Agents Army (Actual)
- `get_server_info` - Información del servidor
- `check_api_keys` - Verificar API keys configuradas

### Agents Army (Planeado)
- Herramientas del DT (gestión de proyectos, tareas, agentes)
- Herramientas de agentes especializados
- Integración con sistemas externos

## Solución de Problemas Comunes

### Problema: RuntimeWarning al ejecutar
**Causa:** El módulo se importa antes de ejecutarse como `__main__`

**Solución Agents Army:**
- ✅ Usar `python -m agents_army.mcp` (no `agents_army.mcp.server`)
- ✅ Tener `__main__.py` en el paquete `mcp/`
- ✅ Agregar fallback en `server.py` para compatibilidad

### Problema: Connection Closed
**Causa:** El servidor no puede inicializarse correctamente

**Solución:**
- Verificar que el comando en `mcp.json` es correcto
- Verificar que Python puede ejecutar el módulo
- Verificar que las dependencias están instaladas (`pip install mcp`)

### Problema: No aparecen herramientas
**Causa:** El servidor no está registrando herramientas correctamente

**Solución:**
- Verificar que FastMCP está instalado
- Verificar logs del servidor MCP en Cursor
- Probar ejecutando el servidor manualmente

## Mejores Prácticas (Aprendidas de Taskmaster)

1. **Usar FastMCP**: Framework estándar y bien soportado
2. **stdio transport**: Compatible con todos los clientes MCP
3. **Herramientas modulares**: Registrar herramientas de forma organizada
4. **Manejo de errores**: Responder correctamente a errores del protocolo MCP
5. **Logging**: Usar `ctx.log_info()` para debugging
6. **Validación**: Validar parámetros de herramientas con schemas

## Referencias

- [Taskmaster GitHub](https://github.com/eyaltoledano/claude-task-master)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
