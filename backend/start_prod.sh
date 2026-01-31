#!/bin/bash

echo "🚀 Starting AutoDev 'All-in-One' Service (Backend + Worker)"

# Start Celery Worker in the background
# We use '&' to detach it so the script continues
echo "👷 Starting Celery Worker..."
celery -A worker.worker worker --loglevel=info &

# Start FastAPI Server in the foreground
# This keeps the container running and listening on the port
echo "🌐 Starting FastAPI Server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
