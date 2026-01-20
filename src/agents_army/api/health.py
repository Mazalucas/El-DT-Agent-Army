"""Health check endpoints for Agents_Army."""

from typing import Dict

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    FastAPI = None
    JSONResponse = None


def create_app() -> "FastAPI":
    """
    Create FastAPI application with health check endpoints.

    Returns:
        FastAPI application

    Raises:
        ImportError: If FastAPI is not installed
    """
    if not FASTAPI_AVAILABLE:
        raise ImportError("FastAPI not installed. Install with: pip install fastapi uvicorn")

    app = FastAPI(title="Agents_Army API", version="1.0.0")

    @app.get("/health")
    async def health() -> Dict[str, str]:
        """
        Health check endpoint.

        Returns:
            Health status
        """
        return {"status": "healthy"}

    @app.get("/ready")
    async def ready() -> Dict[str, bool]:
        """
        Readiness check endpoint.

        Returns:
            Readiness status
        """
        # Check if system is ready
        try:
            from agents_army.core.system import AgentSystem

            system = AgentSystem.get_instance()
            ready_status = system.agents_loaded()

            return {"ready": ready_status}
        except Exception:
            return {"ready": False}

    @app.get("/live")
    async def live() -> Dict[str, str]:
        """
        Liveness check endpoint.

        Returns:
            Liveness status
        """
        return {"status": "alive"}

    return app


# Simple HTTP server fallback if FastAPI not available
def create_simple_app():
    """Create simple HTTP server for health checks."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import json

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "healthy"}).encode())
            elif self.path == "/ready":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ready": True}).encode())
            elif self.path == "/live":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "alive"}).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress logging

    return HealthHandler
