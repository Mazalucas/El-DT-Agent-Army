#!/usr/bin/env python3
"""
Script para configurar automáticamente MCP en diferentes editores.
Replica la metodología de Task Master para configuración automática.
"""

import json
import os
import platform
from pathlib import Path
from typing import Dict, Optional, Tuple


def get_editor_config_paths() -> Dict[str, Dict[str, str]]:
    """
    Retorna las rutas de configuración MCP para cada editor.
    
    Returns:
        Dict con editor como key y dict con 'global' y 'project' paths
    """
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
            "key": "mcpServers"
        },
        "vscode": {
            "global": None,  # VS Code no tiene configuración global MCP estándar
            "project": current_dir / ".vscode" / "mcp.json",
            "key": "servers"
        },
        "windsurf": {
            "global": Path(user_home) / ".codeium" / "windsurf" / "mcp_config.json",
            "project": None,  # Windsurf usa solo global
            "key": "mcpServers"
        },
        "q_cli": {
            "global": Path(user_home) / ".aws" / "amazonq" / "mcp.json",
            "project": None,
            "key": "mcpServers"
        }
    }
    
    return configs


def detect_editor() -> Optional[str]:
    """
    Detecta qué editor está siendo usado basándose en archivos presentes.
    
    Returns:
        Nombre del editor detectado o None
    """
    current_dir = Path.cwd()
    
    # Detectar por archivos de configuración
    if (current_dir / ".cursor" / "rules").exists() or (current_dir / ".cursorrules").exists():
        return "cursor"
    
    if (current_dir / ".vscode").exists():
        return "vscode"
    
    # Detectar por variables de entorno
    if os.environ.get("CURSOR"):
        return "cursor"
    
    if os.environ.get("VSCODE"):
        return "vscode"
    
    if os.environ.get("WINDSURF"):
        return "windsurf"
    
    return None


def get_mcp_config_template(editor: str) -> Dict:
    """
    Genera el template de configuración MCP según el editor.
    
    Args:
        editor: Nombre del editor
        
    Returns:
        Dict con la configuración MCP
    """
    # Template base para todos los editores
    base_config = {
        "command": "python",
        "args": ["-m", "agents_army.mcp.server"],
        "env": {
            "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE",
            "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
            "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE",
            "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
            "MISTRAL_API_KEY": "YOUR_MISTRAL_API_KEY_HERE",
            "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
            "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE",
            "XAI_API_KEY": "YOUR_XAI_API_KEY_HERE",
        }
    }
    
    configs = get_editor_config_paths()
    editor_config = configs.get(editor, {})
    key = editor_config.get("key", "mcpServers")
    
    if editor == "vscode":
        # VS Code usa formato diferente
        return {
            "servers": {
                "agents-army": {
                    **base_config,
                    "type": "stdio"
                }
            }
        }
    else:
        # Cursor, Windsurf, Q CLI usan mcpServers
        return {
            "mcpServers": {
                "agents-army": base_config
            }
        }


def create_mcp_config(editor: str, scope: str = "project") -> Tuple[bool, str]:
    """
    Crea el archivo de configuración MCP para el editor especificado.
    
    Args:
        editor: Nombre del editor (cursor, vscode, windsurf, q_cli)
        scope: 'global' o 'project'
        
    Returns:
        Tuple (success, message)
    """
    configs = get_editor_config_paths()
    
    if editor not in configs:
        return False, f"Editor '{editor}' no soportado. Editores soportados: {list(configs.keys())}"
    
    editor_config = configs[editor]
    config_path = editor_config.get(scope)
    
    if config_path is None:
        return False, f"El editor '{editor}' no soporta configuración '{scope}'"
    
    # Crear directorio si no existe
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Verificar si ya existe configuración
    existing_config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            existing_config = {}
    
    # Obtener template
    template = get_mcp_config_template(editor)
    
    # Merge con configuración existente
    if editor == "vscode":
        if "servers" not in existing_config:
            existing_config["servers"] = {}
        existing_config["servers"].update(template["servers"])
    else:
        if "mcpServers" not in existing_config:
            existing_config["mcpServers"] = {}
        existing_config["mcpServers"].update(template["mcpServers"])
    
    # Escribir archivo
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        
        return True, f"✅ Configuración MCP creada en: {config_path}\n\n🔑 Reemplaza 'YOUR_*_API_KEY_HERE' con tus API keys reales."
    except Exception as e:
        return False, f"❌ Error al crear configuración: {str(e)}"


def main():
    """Función principal del script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Configura automáticamente MCP para El DT en tu editor"
    )
    parser.add_argument(
        "--editor",
        choices=["cursor", "vscode", "windsurf", "q_cli"],
        help="Editor a configurar (si no se especifica, se detecta automáticamente)"
    )
    parser.add_argument(
        "--scope",
        choices=["global", "project"],
        default="project",
        help="Alcance de la configuración: 'global' (todos los proyectos) o 'project' (solo este proyecto)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Crear configuración para todos los editores soportados"
    )
    
    args = parser.parse_args()
    
    if args.all:
        # Crear para todos los editores
        configs = get_editor_config_paths()
        results = []
        
        for editor in configs.keys():
            for scope in ["global", "project"]:
                success, message = create_mcp_config(editor, scope)
                if success:
                    results.append(f"{editor} ({scope}): {message}")
        
        print("\n".join(results))
        return
    
    # Detectar o usar editor especificado
    editor = args.editor or detect_editor()
    
    if editor is None:
        print("⚠️  No se pudo detectar el editor automáticamente.")
        print("\nEditores soportados:")
        print("  - cursor: Cursor AI")
        print("  - vscode: Visual Studio Code")
        print("  - windsurf: Windsurf")
        print("  - q_cli: Amazon Q Developer CLI")
        print("\nUsa --editor <nombre> para especificar manualmente.")
        print("\nEjemplo: python scripts/setup_mcp_config.py --editor cursor")
        return
    
    print(f"🔍 Editor detectado: {editor}")
    print(f"📁 Alcance: {args.scope}\n")
    
    success, message = create_mcp_config(editor, args.scope)
    print(message)
    
    if success:
        print("\n📝 Próximos pasos:")
        print("1. Abre el archivo de configuración creado")
        print("2. Reemplaza 'YOUR_*_API_KEY_HERE' con tus API keys reales")
        print("3. Reinicia tu editor para que cargue la nueva configuración")
        print("4. En Cursor: Ve a Settings (Ctrl+Shift+J) → MCP → Habilita 'agents-army'")


if __name__ == "__main__":
    main()
