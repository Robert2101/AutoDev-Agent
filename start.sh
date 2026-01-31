#!/bin/bash
# One-button script to run the project
echo "🚀 Starting AutoDev Agent..."
docker-compose up -d --remove-orphans

echo ""
echo "🎉 System is running!"
echo "---------------------------------------------------"
echo "🌍 Dashboard: http://localhost:3000"
echo "🔌 API Docs:  http://localhost:8000/docs"
echo "---------------------------------------------------"
echo "📝 Development Workflow:"
echo "   - Frontend changes (Next.js): Auto-reload"
echo "   - API changes (FastAPI):      Auto-reload"
echo "   - Agent changes (Celery):     Requires restart"
echo "     👉 Run: docker-compose restart worker"
echo "---------------------------------------------------"
echo "logs: docker-compose logs -f"
