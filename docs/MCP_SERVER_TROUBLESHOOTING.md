# Solución de Problemas del Servidor MCP

## Problemas Identificados y Solucionados

### 1. RuntimeWarning: 'agents_army.mcp.server' found in sys.modules

#### Problema
Cuando Cursor intentaba ejecutar el servidor MCP con `python -m agents_army.mcp.server`, aparecía este error:

```
RuntimeWarning: 'agents_army.mcp.server' found in sys.modules after import of package 'agents_army.mcp', but prior to execution of 'agents_army.mcp.server'; this may result in unpredictable behaviour
```

#### Causa
El problema ocurría porque:
1. Python intentaba ejecutar `agents_army.mcp.server` como módulo principal (`-m`)
2. No existía un archivo `__main__.py` en el directorio `mcp/`
3. Python intentaba ejecutar `server.py` directamente, pero `server.py` contiene una clase `MCPServer`, no un punto de entrada ejecutable
4. Esto causaba que el módulo se importara antes de ejecutarse como `__main__`, generando el warning

#### Solución
Se creó el archivo `src/agents_army/mcp/__main__.py` que:
- Implementa un servidor MCP real usando el SDK oficial de MCP (`mcp.server.fastmcp`)
- Usa transporte stdio (estándar para MCP)
- Expone herramientas básicas (`get_server_info`, `check_api_keys`)
- Tiene un fallback si el paquete `mcp` no está instalado (implementación básica)

#### Instalación
Para usar el servidor MCP completo, instala la dependencia opcional:

```bash
pip install agents-army[mcp]
# o
pip install mcp
```

### 2. Connection Closed y "No server info found"

#### Problema
Los logs mostraban:
```
Connection closed
Pending server creation failed: MCP error -32000: Connection closed
No server info found
```

#### Causa
Estos errores ocurrían porque:
1. El servidor MCP no podía inicializarse correctamente debido al RuntimeWarning
2. Sin un `__main__.py` válido, el servidor fallaba al iniciar
3. Cursor no podía establecer comunicación con el servidor

#### Solución
Con el nuevo `__main__.py`:
- El servidor puede inicializarse correctamente
- Responde a las solicitudes de inicialización del protocolo MCP
- Maneja errores de forma más elegante

### 3. Mensaje de API Key Poco Destacado

#### Problema
El mensaje sobre la falta de API keys se mostraba de forma muy discreta, en texto pequeño, y no transmitía la urgencia del problema.

#### Solución
Se mejoró el mensaje en `skills/dt-start.md` para que:
- Use emojis y formato destacado (⚠️, 🔴)
- Sea más urgente e imperativo
- Muestre claramente las consecuencias de no tener API keys
- Incluya enlaces directos a donde obtener las keys

## Verificación de la Solución

### 1. Verificar que el servidor MCP funciona

Ejecuta manualmente el servidor para verificar:

```bash
python -m agents_army.mcp.server
```

Deberías ver que el servidor se inicia sin errores. Presiona Ctrl+C para detenerlo.

### 2. Verificar configuración MCP en Cursor

1. Abre Cursor Settings (`Ctrl+Shift+J` o `Cmd+Shift+J`)
2. Ve a la pestaña **MCP**
3. Verifica que `agents-army` esté habilitado
4. Revisa los logs de MCP para confirmar que no hay errores

### 3. Verificar API Keys

Usa el script de verificación:

```bash
python scripts/check_mcp_config.py
```

O verifica manualmente el archivo `.cursor/mcp.json` (o `~/.cursor/mcp.json` para configuración global).

## Prevención en Futuros Proyectos

### Checklist para Nuevos Proyectos

1. **Verificar estructura del módulo MCP**:
   - ✅ Debe existir `src/agents_army/mcp/__main__.py`
   - ✅ Debe tener un punto de entrada ejecutable

2. **Instalar dependencias opcionales si se usa MCP**:
   ```bash
   pip install agents-army[mcp]
   ```

3. **Configurar MCP antes de usar**:
   ```bash
   python scripts/setup_mcp_config.py
   ```

4. **Verificar que el servidor funciona**:
   ```bash
   python -m agents_army.mcp.server
   ```

### Estructura Correcta del Módulo MCP

```
src/agents_army/mcp/
├── __init__.py          # Exporta clases principales
├── __main__.py          # ⭐ Punto de entrada ejecutable (NUEVO)
├── server.py            # Clase MCPServer
├── client.py            # Clase MCPClient
└── models.py            # Modelos de datos MCP
```

## Comandos Útiles

### Verificar configuración MCP
```bash
python scripts/check_mcp_config.py
```

### Configurar MCP automáticamente
```bash
python scripts/setup_mcp_config.py --editor cursor --scope project
```

### Probar servidor MCP manualmente
```bash
python -m agents_army.mcp.server
```

### Instalar dependencias MCP
```bash
pip install agents-army[mcp]
# o
pip install mcp
```

## Referencias

- [MCP Configuration Guide](MCP_CONFIGURATION.md)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [DT Start Workflow](../skills/dt-start.md)
