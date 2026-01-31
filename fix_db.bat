@echo off
echo ===================================================
echo 🔧 AutoDev DB Fixer (Windows)
echo ===================================================
echo.
echo 🛑 Stopping containers and deleting old database volumes...
echo    (This will wipe existing audit history!)
echo.

docker-compose down -v

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to clean up. Ensure Docker is running.
    pause
    exit /b 1
)

echo.
echo ✅ Database volume cleaned.
echo 🚀 Restarting fresh...
echo.

call start.bat
