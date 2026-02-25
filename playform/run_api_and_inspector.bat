@echo off
setlocal enableextensions
cd /d "%~dp0"

set "NO_PAUSE=0"
if /I "%~1"=="--no-pause" set "NO_PAUSE=1"

set "API_HOST=127.0.0.1"
set "API_PORT=8000"
set "PLAYFORM_API=http://%API_HOST%:%API_PORT%"
set "BACKEND_DIR=%~dp0backend"
set "VENV_DIR=%BACKEND_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "REQ_FILE=%BACKEND_DIR%\requirements.txt"
set "MCP_SERVER=%~dp0mcp_server.py"
set "PY_EXE="

if not exist "%MCP_SERVER%" (
    echo [ERROR] Missing MCP server script:
    echo         "%MCP_SERVER%"
    call :finish 1
)

if not exist "%REQ_FILE%" (
    echo [ERROR] Missing requirements file:
    echo         "%REQ_FILE%"
    call :finish 1
)

where npx.cmd >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npx.cmd not found. Install Node.js first.
    call :finish 1
)

if exist "%VENV_PY%" (
    set "PY_EXE=%VENV_PY%"
) else (
    call :find_system_python
    if not defined PY_EXE (
        echo [ERROR] Python 3.11+ not found.
        echo Install Python and run this script again.
        call :finish 1
    )

    echo [INFO] Creating virtualenv:
    echo        "%VENV_DIR%"
    "%PY_EXE%" -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtualenv.
        call :finish 1
    )
    set "PY_EXE=%VENV_PY%"
)

echo [INFO] Verifying backend dependencies...
"%VENV_PY%" -c "import fastapi,uvicorn,mcp,requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing backend dependencies...
    "%VENV_PY%" -m pip install -r "%REQ_FILE%"
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        call :finish 1
    )
)

call :is_api_up
if errorlevel 1 (
    echo [INFO] Starting Playform API on %PLAYFORM_API% ...
    start "Playform API" cmd /k "cd /d ""%~dp0"" ^&^& ""%VENV_PY%"" -m uvicorn backend.main:app --reload --host %API_HOST% --port %API_PORT%"
    ping -n 4 127.0.0.1 >nul
) else (
    echo [INFO] API already running on %PLAYFORM_API%.
)

echo [INFO] Waiting API health to reach 100%% ...
call :wait_for_api_100
if errorlevel 1 (
    echo [ERROR] API readiness did not reach 100%%.
    call :finish 1
)

echo [INFO] Starting MCP Inspector ...
start "MCP Inspector" cmd /k "set PLAYFORM_API=%PLAYFORM_API% ^&^& cd /d ""%~dp0"" ^&^& npx.cmd @modelcontextprotocol/inspector"

echo.
echo ===========================================================
echo Auto-detection complete.
echo In Inspector use:
echo.
echo Transport:  STDIO
echo Command:    %VENV_PY%
echo Arguments:  %MCP_SERVER%
echo Env:        PLAYFORM_API=%PLAYFORM_API%
echo ===========================================================
echo.
echo Keep the opened terminal windows running while testing.
call :finish 0

:find_system_python
set "PY_EXE="
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set "PY_EXE=%LocalAppData%\Programs\Python\Python312\python.exe"
if not defined PY_EXE if exist "%LocalAppData%\Programs\Python\Python311\python.exe" set "PY_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"

if not defined PY_EXE (
    for /f "usebackq tokens=*" %%i in (`where python 2^>nul`) do (
        echo %%i | find /I "WindowsApps\python.exe" >nul
        if errorlevel 1 (
            set "PY_EXE=%%i"
            goto :find_python_done
        )
    )
)

:find_python_done
if defined PY_EXE (
    for /f "tokens=2 delims= " %%v in ('"%PY_EXE%" --version 2^>^&1') do set "PY_VER=%%v"
    echo [INFO] Using Python:
    echo        "%PY_EXE%"  (%PY_VER%)
)
exit /b 0

:is_api_up
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r = Invoke-RestMethod -Uri '%PLAYFORM_API%/health' -TimeoutSec 2; if ($r.status -eq 'ok') { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
exit /b %errorlevel%

:wait_for_api_100
setlocal
set /a ATTEMPTS=20
set /a I=0

:wait_loop
set /a I+=1
call :is_api_up
if not errorlevel 1 (
    echo [INFO] API health check: 100%%
    endlocal & exit /b 0
)

set /a P=I*5
if %P% gtr 99 set /a P=99
echo [INFO] API health check: %P%%%  (retry %I%/%ATTEMPTS%)
ping -n 2 127.0.0.1 >nul
if %I% lss %ATTEMPTS% goto :wait_loop

echo [ERROR] API health timeout after %ATTEMPTS% checks.
endlocal & exit /b 1

:finish
set "RC=%~1"
if "%NO_PAUSE%"=="0" pause
endlocal & exit /b %RC%
