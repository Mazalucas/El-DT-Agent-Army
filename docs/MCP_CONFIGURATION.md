# Configuración MCP para El DT

Este documento explica cómo configurar El DT usando el protocolo MCP (Model Context Protocol) en diferentes editores, siguiendo la metodología de Task Master.

## ¿Qué es MCP?

MCP (Model Context Protocol) permite que El DT se integre directamente con tu editor, permitiendo que los agentes accedan a herramientas y recursos sin necesidad de configuración manual compleja.

## Métodos de Configuración

### Método 1: Configuración Automática (Recomendado)

El método más fácil es usar nuestro script de configuración automática:

```bash
# Detectar editor automáticamente y crear configuración
python scripts/setup_mcp_config.py

# O especificar editor manualmente
python scripts/setup_mcp_config.py --editor cursor

# Crear configuración global (todos los proyectos)
python scripts/setup_mcp_config.py --editor cursor --scope global

# Crear para todos los editores
python scripts/setup_mcp_config.py --all
```

El script:
1. ✅ Detecta automáticamente tu editor
2. ✅ Crea el archivo de configuración en la ubicación correcta
3. ✅ Incluye placeholders para todas las API keys
4. ✅ Preserva configuraciones existentes

### Método 2: Configuración Manual

Si prefieres configurar manualmente, sigue las instrucciones según tu editor:

## Editores Soportados

### Cursor

#### Configuración Global (Todos los Proyectos)

**Ubicación del archivo:**
- **Linux/macOS**: `~/.cursor/mcp.json`
- **Windows**: `%USERPROFILE%\.cursor\mcp.json`

**Contenido:**

```json
{
  "mcpServers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_API_KEY_HERE",
        "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_API_KEY_HERE"
      }
    }
  }
}
```

#### Configuración por Proyecto

**Ubicación del archivo:** `<project_folder>/.cursor/mcp.json`

Mismo formato que la configuración global.

#### Habilitar en Cursor

Después de crear el archivo:

1. Abre Cursor Settings (`Ctrl+Shift+J` o `Cmd+Shift+J`)
2. Ve a la pestaña **MCP** en el menú lateral
3. Habilita `agents-army` con el toggle
4. Reinicia Cursor

### Visual Studio Code

#### Configuración por Proyecto

**Ubicación del archivo:** `<project_folder>/.vscode/mcp.json`

**Contenido:**

```json
{
  "servers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "type": "stdio",
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_API_KEY_HERE",
        "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_API_KEY_HERE"
      }
    }
  }
}
```

**Nota**: VS Code requiere la extensión MCP para funcionar.

### Windsurf

#### Configuración Global

**Ubicación del archivo:**
- **Linux/macOS**: `~/.codeium/windsurf/mcp_config.json`
- **Windows**: `%USERPROFILE%\.codeium\windsurf\mcp_config.json`

**Contenido:**

```json
{
  "mcpServers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_API_KEY_HERE",
        "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_API_KEY_HERE"
      }
    }
  }
}
```

### Amazon Q Developer CLI

#### Configuración Global

**Ubicación del archivo:**
- **Linux/macOS**: `~/.aws/amazonq/mcp.json`
- **Windows**: `%USERPROFILE%\.aws\amazonq\mcp.json`

**Contenido:**

```json
{
  "mcpServers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_API_KEY_HERE",
        "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_API_KEY_HERE"
      }
    }
  }
}
```

## Configuración de API Keys

### ¿Qué API Keys Necesito?

**Mínimo requerido**: Al menos UNA de las siguientes:

- **OpenAI API Key**: Para usar GPT-4, GPT-3.5
- **Anthropic API Key**: Para usar Claude
- **Google API Key**: Para usar Gemini
- **Perplexity API Key**: Para investigación (recomendado)
- **Otros**: Mistral, Groq, OpenRouter, xAI

### Cómo Obtener API Keys

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Anthropic**: https://console.anthropic.com/
3. **Google**: https://makersuite.google.com/app/apikey
4. **Perplexity**: https://www.perplexity.ai/settings/api
5. **Otros**: Consulta la documentación de cada proveedor

### Reemplazar Placeholders

Después de crear el archivo de configuración:

1. Abre el archivo `mcp.json` creado
2. Reemplaza `YOUR_OPENAI_API_KEY_HERE` con tu API key real
3. Reemplaza otras keys según las que uses
4. Elimina las líneas de keys que no uses (opcional)

**Ejemplo:**

```json
{
  "mcpServers": {
    "agents-army": {
      "command": "python",
      "args": ["-m", "agents_army.mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-proj-abc123...",  // ← Tu key real aquí
        "ANTHROPIC_API_KEY": "sk-ant-api03-..."  // ← Tu key real aquí
        // Eliminé las otras keys que no uso
      }
    }
  }
}
```

## Verificación

### Verificar que Funciona

1. Reinicia tu editor después de configurar
2. En Cursor: Ve a Settings → MCP y verifica que `agents-army` esté habilitado
3. En el chat de tu editor, prueba:
   ```
   ¿Puedes usar las herramientas de El DT?
   ```

Si todo está bien configurado, El DT debería poder usar las herramientas MCP.

### Troubleshooting

#### Problema: "0 tools enabled" en Cursor

**Solución:**
1. Verifica que las API keys estén correctamente configuradas
2. Reinicia Cursor completamente
3. Verifica que el archivo `mcp.json` tenga el formato correcto
4. Asegúrate de que `agents-army` esté habilitado en Settings → MCP

#### Problema: "Command not found: python"

**Solución:**
1. Verifica que Python esté instalado: `python --version`
2. Si usas `python3`, actualiza el comando en `mcp.json`:
   ```json
   "command": "python3"
   ```

#### Problema: El archivo no se crea

**Solución:**
1. Verifica permisos de escritura en el directorio
2. Crea el directorio manualmente si no existe:
   ```bash
   mkdir -p ~/.cursor  # Linux/macOS
   mkdir %USERPROFILE%\.cursor  # Windows
   ```

## Configuración Avanzada

### Usar Solo Ciertas API Keys

Puedes eliminar las keys que no uses del archivo de configuración. Solo deja las que necesitas.

### Configuración por Proyecto vs Global

- **Global**: Aplica a todos los proyectos (más conveniente)
- **Proyecto**: Solo aplica al proyecto actual (más específico)

Recomendamos empezar con configuración **por proyecto** para probar, y luego mover a **global** si funciona bien.

## Seguridad

### ⚠️ Importante

- **NUNCA** subas tu archivo `mcp.json` con API keys reales a GitHub
- Asegúrate de que `.cursor/mcp.json` esté en `.gitignore`
- Si accidentalmente subiste keys, revócalas inmediatamente y crea nuevas

### Verificar .gitignore

Asegúrate de que estos archivos estén en `.gitignore`:

```
.cursor/mcp.json
.vscode/mcp.json
.env
```

## Próximos Pasos

Después de configurar MCP:

1. **Inicializa El DT**: Usa `/dt-start` en tu editor
2. **Prueba las herramientas**: Pide a El DT que use alguna herramienta
3. **Lee la documentación**: [QUICK_START.md](QUICK_START.md)

---

**¿Problemas?** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) o abre un issue en GitHub.
