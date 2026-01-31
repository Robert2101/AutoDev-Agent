#!/bin/bash
echo "🔧 AutoDev DB Fixer"
echo "======================"
echo "🛑 Stopping containers and removing volumes..."
docker-compose down -v

echo "✅ Database volume cleaned."
echo "🚀 Restarting..."
./start.sh
