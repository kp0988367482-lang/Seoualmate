from mcp.server.fastmcp import FastMCP
import os
import sys
import logging
import requests
from typing import List, Dict, Any

logging.basicConfig(filename="mcp_server.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("mcp_server")

mcp = FastMCP("playform")


@mcp.tool()
def hello(name: str) -> str:
    return f"Hello {name}"


@mcp.tool()
def list_games() -> List[Dict[str, Any]]:
    """Return public games from the running Playform API."""
    api = os.getenv("PLAYFORM_API", "http://127.0.0.1:8000")
    r = requests.get(f"{api}/api/games", timeout=5)
    r.raise_for_status()
    return r.json()


@mcp.tool()
def create_game(name: str, token: str = None) -> Dict[str, Any]:
    """Create a game via Playform API. Pass optional bearer token for admin actions."""
    api = os.getenv("PLAYFORM_API", "http://127.0.0.1:8000")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.post(f"{api}/api/games", json={"name": name}, headers=headers, timeout=5)
    r.raise_for_status()
    return r.json()


def log_env():
    try:
        logger.info(f"Python executable: {sys.executable}")
        logger.info(f"sys.path: {sys.path}")
        # versions
        import importlib

        for mod in ("mcp", "requests"):
            try:
                m = importlib.import_module(mod)
                ver = getattr(m, "__version__", None)
                logger.info(f"{mod} version: {ver}")
            except Exception as e:
                logger.exception(f"Failed to import {mod}: {e}")
    except Exception:
        logger.exception("Failed to log environment")


if __name__ == "__main__":
    log_env()
    try:
        logger.info("Starting MCP server (playform)")
        mcp.run()
    except Exception as e:
        logger.exception(f"MCP server failed to start: {e}")
        # print to stderr so VS Code shows it
        print(f"MCP server failed to start: {e}", file=sys.stderr)
