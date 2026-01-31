@echo off
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo 🚀 AutoDev Agent Launcher
echo ===================================================
echo.
echo Select an option:
echo [1] Start AutoDev Agent (Normal)
echo [2] Hard Reset (Fix Database/Environment Issues)
echo.

set /p choice="Enter choice [1]: "
if "%choice%"=="" set choice=1

IF "%choice%"=="2" (
    echo.
    echo 🛑 Stopping containers and WAPING DATA volumes...
    docker-compose down -v
    echo ✅ Cleanup complete. Starting fresh...
    echo.
) else (
    echo.
    echo 🐳 Starting containers...
)

:: Check Docker
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running!
    pause
    exit /b 1
)

docker-compose up -d --remove-orphans

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Startup failed.
    pause
    exit /b 1
)

echo.
echo 🎉 System is running!
echo ---------------------------------------------------
echo 🌍 Dashboard: http://localhost:3000
echo 🔌 API Docs:  http://localhost:8000/docs
echo ---------------------------------------------------
echo 📝 Tip: Use option [2] if you see DB errors.
echo ---------------------------------------------------
echo 📜 Logs: docker-compose logs -f
echo.
pause
