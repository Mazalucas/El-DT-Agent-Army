#!/usr/bin/env python3
"""
Helper script para verificar configuración MCP y detectar si necesita API keys.
Usado por el workflow dt-start.
"""

import json
import os
import platform
from pathlib import Path
from typing import Dict, Optional, Tuple


def get_editor_config_paths() -> Dict[str, Dict[str, Path]]:
    """Retorna las rutas de configuración MCP para cada editor."""
    system = platform.system()
    is_windows = system == "Windows"
    
    if is_windows:
        user_home = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        user_home = os.path.expanduser("~")
    
    current_dir = Path.cwd()
    
    configs = {
        "cursor": {
            "global": Path(user_home) / ".cursor" / "mcp.json",
            "project": current_dir / ".cursor" / "mcp.json",
        },
        "vscode": {
            "global": None,
            "project": current_dir / ".vscode" / "mcp.json",
        },
        "windsurf": {
            "global": Path(user_home) / ".codeium" / "windsurf" / "mcp_config.json",
            "project": None,
        },
        "q_cli": {
            "global": Path(user_home) / ".aws" / "amazonq" / "mcp.json",
            "project": None,
        }
    }
    
    return configs


def detect_editor() -> Optional[str]:
    """Detecta qué editor está siendo usado."""
    current_dir = Path.cwd()
    
    if (current_dir / ".cursor" / "rules").exists() or (current_dir / ".cursorrules").exists():
        return "cursor"
    
    if (current_dir / ".vscode").exists():
        return "vscode"
    
    if os.environ.get("CURSOR"):
        return "cursor"
    
    if os.environ.get("VSCODE"):
        return "vscode"
    
    if os.environ.get("WINDSURF"):
        return "windsurf"
    
    return None


def has_placeholder_keys(config: Dict) -> bool:
    """Verifica si el archivo tiene placeholders en lugar de keys reales."""
    if not config:
        return True
    
    # Buscar en mcpServers o servers
    servers = config.get("mcpServers", {}) or config.get("servers", {})
    
    if not servers:
        return True
    
    # Buscar agents-army
    agents_config = servers.get("agents-army", {})
    if not agents_config:
        return True
    
    env = agents_config.get("env", {})
    if not env:
        return True
    
    # Verificar si hay placeholders
    placeholder_values = ["YOUR_", "HERE", "PLACEHOLDER", ""]
    
    for key, value in env.items():
        if isinstance(value, str):
            if any(placeholder in value.upper() for placeholder in placeholder_values):
                return True
            if len(value.strip()) == 0:
                return True
    
    return False


def check_mcp_config() -> Tuple[bool, Optional[str], Optional[Path], bool]:
    """
    Verifica si existe configuración MCP y si tiene API keys válidas.
    
    Returns:
        Tuple (has_config, editor, config_path, has_valid_keys)
    """
    editor = detect_editor()
    
    if editor is None:
        return False, None, None, False
    
    configs = get_editor_config_paths()
    editor_config = configs.get(editor, {})
    
    # Buscar primero en proyecto, luego global
    config_path = None
    for scope in ["project", "global"]:
        path = editor_config.get(scope)
        if path and path.exists():
            config_path = path
            break
    
    if config_path is None:
        # No existe configuración
        # Retornar la ruta donde debería crearse
        project_path = editor_config.get("project")
        if project_path:
            config_path = project_path
        else:
            config_path = editor_config.get("global")
        
        return False, editor, config_path, False
    
    # Existe configuración, verificar si tiene keys válidas
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        has_valid_keys = not has_placeholder_keys(config)
        return True, editor, config_path, has_valid_keys
    
    except (json.JSONDecodeError, IOError):
        # Archivo corrupto o no legible
        return True, editor, config_path, False


def main():
    """Función principal para uso desde línea de comandos."""
    has_config, editor, config_path, has_valid_keys = check_mcp_config()
    
    if not has_config:
        print(f"NO_CONFIG:{editor}:{config_path}")
        return
    
    if not has_valid_keys:
        print(f"NO_KEYS:{editor}:{config_path}")
        return
    
    print(f"OK:{editor}:{config_path}")


if __name__ == "__main__":
    main()
