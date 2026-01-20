#!/usr/bin/env python3
"""
MCP Server entry point for Agents Army.

This module implements a real MCP (Model Context Protocol) server that can be
invoked via `python -m agents_army.mcp.server`.

The server uses stdio transport and exposes tools and resources for El DT
and its specialized agents.
"""

import sys
from typing import Any, Dict

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp import Context
    
    # Initialize FastMCP server
    mcp = FastMCP(name="agents-army", json_response=True)
    
    @mcp.tool()
    def get_server_info(ctx: Context) -> Dict[str, Any]:
        """
        Get information about the Agents Army MCP server.
        
        Returns:
            Dict with server information
        """
        ctx.log_info("Getting server info")
        return {
            "name": "agents-army",
            "version": "0.1.0",
            "description": "MCP Server for Agents Army - El DT and specialized agents",
            "status": "running"
        }
    
    @mcp.tool()
    def check_api_keys(ctx: Context) -> Dict[str, Any]:
        """
        Check which API keys are configured in the environment.
        
        Returns:
            Dict with API key status for each provider
        """
        import os
        
        ctx.log_info("Checking API keys")
        
        api_keys = {
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_API_KEY", "").startswith("YOUR_")),
            "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY") and not os.getenv("ANTHROPIC_API_KEY", "").startswith("YOUR_")),
            "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_API_KEY", "").startswith("YOUR_")),
            "PERPLEXITY_API_KEY": bool(os.getenv("PERPLEXITY_API_KEY") and not os.getenv("PERPLEXITY_API_KEY", "").startswith("YOUR_")),
            "MISTRAL_API_KEY": bool(os.getenv("MISTRAL_API_KEY") and not os.getenv("MISTRAL_API_KEY", "").startswith("YOUR_")),
            "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY") and not os.getenv("GROQ_API_KEY", "").startswith("YOUR_")),
            "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENROUTER_API_KEY", "").startswith("YOUR_")),
            "XAI_API_KEY": bool(os.getenv("XAI_API_KEY") and not os.getenv("XAI_API_KEY", "").startswith("YOUR_")),
        }
        
        configured_count = sum(1 for v in api_keys.values() if v)
        
        return {
            "api_keys": api_keys,
            "configured_count": configured_count,
            "has_any_key": configured_count > 0,
            "status": "configured" if configured_count > 0 else "not_configured"
        }
    
    # Main entry point
    if __name__ == "__main__":
        # Run the server using stdio transport (default)
        mcp.run()
        
except ImportError:
    # Fallback if mcp package is not installed
    import sys
    import json
    
    # Simple stdio-based server that at least responds to initialization
    # This prevents the RuntimeWarning but won't provide full MCP functionality
    def simple_mcp_server():
        """Simple MCP server implementation without external dependencies."""
        try:
            # Read initialization request
            line = sys.stdin.readline()
            if line:
                init_request = json.loads(line.strip())
                
                # Respond with initialization
                init_response = {
                    "jsonrpc": "2.0",
                    "id": init_request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {}
                        },
                        "serverInfo": {
                            "name": "agents-army",
                            "version": "0.1.0"
                        }
                    }
                }
                
                print(json.dumps(init_response), flush=True)
                
                # Keep reading and responding to requests
                while True:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    
                    try:
                        request = json.loads(line.strip())
                        method = request.get("method", "")
                        
                        if method == "tools/list":
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "tools": [
                                        {
                                            "name": "get_server_info",
                                            "description": "Get information about the Agents Army MCP server"
                                        },
                                        {
                                            "name": "check_api_keys",
                                            "description": "Check which API keys are configured"
                                        }
                                    ]
                                }
                            }
                            print(json.dumps(response), flush=True)
                        elif method == "tools/call":
                            tool_name = request.get("params", {}).get("name", "")
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"Tool {tool_name} called (mcp package not installed - install with: pip install mcp)"
                                        }
                                    ]
                                }
                            }
                            print(json.dumps(response), flush=True)
                        else:
                            # Echo back for other methods
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {}
                            }
                            print(json.dumps(response), flush=True)
                    except json.JSONDecodeError:
                        continue
                    except Exception:
                        continue
                        
        except Exception as e:
            # Write error to stderr
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32000,
                    "message": f"MCP server error: {str(e)}"
                }
            }
            print(json.dumps(error_response), file=sys.stderr, flush=True)
            sys.exit(1)
    
    if __name__ == "__main__":
        simple_mcp_server()
