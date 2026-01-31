@echo off
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo 🚀 Starting AutoDev Agent (Windows)
echo ===================================================

:: Check if Docker is running
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running! Please start Docker Desktop and try again.
    pause
    exit /b 1
)

:: Run Docker Compose
echo 🐳 Docker is running. Starting containers...
docker-compose up -d --remove-orphans

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to start containers. Please check error messages above.
    pause
    exit /b 1
)

echo.
echo 🎉 System is running!
echo ---------------------------------------------------
echo 🌍 Dashboard: http://localhost:3000
echo 🔌 API Docs:  http://localhost:8000/docs
echo ---------------------------------------------------
echo 📝 Development Workflow:
echo    - Frontend changes (Next.js): Auto-reload
echo    - API changes (FastAPI):      Auto-reload
echo    - Agent changes (Celery):     Requires restart
echo      👉 Run: docker-compose restart worker
echo ---------------------------------------------------
echo 📜 To view logs, run: docker-compose logs -f
echo.
pause
