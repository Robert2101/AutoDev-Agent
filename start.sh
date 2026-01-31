#!/bin/bash
echo "==================================================="
echo "🚀 AutoDev Agent Launcher"
echo "==================================================="
echo ""
echo "Select an option:"
echo " [1] Start AutoDev Agent (Normal)"
echo " [2] Hard Reset (Fix Database/Environment Issues)"
echo ""
read -p "Enter choice [1]: " choice
choice=${choice:-1}

if [ "$choice" = "2" ]; then
    echo ""
    echo "🛑 Stopping containers and WIPING DATA volumes..."
    docker-compose down -v
    echo "✅ Cleanup complete. Starting fresh..."
    echo ""
else
    echo ""
    echo "🐳 Starting containers..."
fi

docker-compose up -d --remove-orphans

echo ""
echo "🎉 System is running!"
echo "---------------------------------------------------"
echo "🌍 Dashboard: http://localhost:3000"
echo "🔌 API Docs:  http://localhost:8000/docs"
echo "---------------------------------------------------"
echo "📝 Tip: Use option [2] if you see DB errors."
echo "---------------------------------------------------"
echo "logs: docker-compose logs -f"
