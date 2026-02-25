@echo off
REM Robust wrapper: prefer backend\.venv\Scripts\python.exe. If missing, use PATH python.
REM If still missing, install Python via winget (no uv), fallback to python.org download page.
cd /d "%~dp0"
setlocal

set "VENV_PY=%~dp0backend\.venv\Scripts\python.exe"
set "PY_EXE="

if exist "%VENV_PY%" (
    echo Using virtualenv python: "%VENV_PY%"
    set "PY_EXE=%VENV_PY%"
    goto :run
)

for /f "usebackq delims=" %%i in (`where python 2^>nul`) do (
    set "PY_EXE=%%i"
    goto :run
)

echo Python not found. Trying to install Python 3.12 via winget...
where winget >nul 2>nul
if %ERRORLEVEL%==0 (
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    if %ERRORLEVEL%==0 (
        for /f "usebackq delims=" %%i in (`where python 2^>nul`) do (
            set "PY_EXE=%%i"
            goto :run
        )
    )
)

echo Could not auto-install Python with winget.
echo Opening official Python download page...
start "" "https://www.python.org/downloads/windows/"
echo After installing Python, re-run this script.
exit /b 1

:run
echo Python executable: "%PY_EXE%"
set PLAYFORM_API=http://127.0.0.1:8000
"%PY_EXE%" "%~dp0mcp_server.py"
endlocal
