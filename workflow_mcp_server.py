"""Local MCP server that exposes Playform automation workflow tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from workflow_engine import WorkflowEngine


mcp = FastMCP("playform-workflow")
engine = WorkflowEngine()


@mcp.tool()
def run_daily_workflow(
    objective: str,
    mode: str = "demo",
    save_report: bool = True,
) -> dict:
    """Run the Playform daily automation workflow and optionally persist a report."""
    return engine.run_daily_workflow(objective=objective, mode=mode, save_report=save_report)


@mcp.tool()
def list_workflow_reports(limit: int = 10) -> list[dict]:
    """List recent workflow run summaries."""
    return engine.list_reports(limit=limit)


@mcp.tool()
def latest_workflow_report() -> dict:
    """Return the most recent workflow report."""
    return engine.latest_report()


@mcp.tool()
def get_workflow_report(run_id: str) -> dict:
    """Fetch one workflow report by run ID."""
    return engine.get_report(run_id=run_id)


@mcp.tool()
def workflow_healthcheck() -> dict:
    """Basic healthcheck for MCP workflow server."""
    return {
        "status": "ok",
        "server": "playform-workflow",
        "tools": [
            "run_daily_workflow",
            "list_workflow_reports",
            "latest_workflow_report",
            "get_workflow_report",
            "workflow_healthcheck",
        ],
    }


if __name__ == "__main__":
    mcp.run()
