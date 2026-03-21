@echo off
REM Wrapper to set PLAYFORM_API and launch the MCP server using python on PATH
set PLAYFORM_API=http://127.0.0.1:8000
cd /d "%~dp0"
python "%~dp0mcp_server.py"