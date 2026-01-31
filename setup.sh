#!/bin/bash

# AutoDev Agent - Complete Setup Script
# This script will verify everything and help you get started

set -e

echo "🤖 AutoDev Agent - Complete Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is running
echo "Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi
print_success "Docker is running"

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi
print_success "Docker Compose is installed"

echo ""
echo "📋 Checking .env file..."

# Check if .env exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    exit 1
fi
print_success ".env file exists"

# Check if API keys are set
if grep -q "YOUR_GEMINI_API_KEY_HERE" .env; then
    print_warning "Gemini API key not set in .env"
    echo ""
    print_info "Please follow these steps to get your Gemini API key:"
    echo "  1. Go to: https://makersuite.google.com/app/apikey"
    echo "  2. Click 'Create API Key'"
    echo "  3. Copy the key"
    echo ""
    read -p "Enter your Gemini API key (or press Enter to skip): " gemini_key
    
    if [ ! -z "$gemini_key" ]; then
        # Update .env file
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/YOUR_GEMINI_API_KEY_HERE/$gemini_key/" .env
        else
            sed -i "s/YOUR_GEMINI_API_KEY_HERE/$gemini_key/" .env
        fi
        print_success "Gemini API key updated"
    fi
fi

if grep -q "YOUR_GITHUB_TOKEN_HERE" .env; then
    print_warning "GitHub token not set in .env"
    echo ""
    print_info "Please follow these steps to get your GitHub token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Select 'repo' scope"
    echo "  4. Copy the token"
    echo ""
    read -p "Enter your GitHub token (or press Enter to skip): " github_token
    
    if [ ! -z "$github_token" ]; then
        # Update .env file
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/YOUR_GITHUB_TOKEN_HERE/$github_token/" .env
        else
            sed -i "s/YOUR_GITHUB_TOKEN_HERE/$github_token/" .env
        fi
        print_success "GitHub token updated"
    fi
fi

echo ""
print_info "Note: PostgreSQL and Redis are included in Docker - no local installation needed!"
echo ""

# Ask if user wants to start services
echo "Ready to start AutoDev Agent?"
read -p "Start all services now? (y/n): " start_services

if [[ $start_services == "y" || $start_services == "Y" ]]; then
    echo ""
    echo "🏗️  Building Docker images (this may take a few minutes)..."
    docker-compose build
    
    echo ""
    echo "🚀 Starting all services..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Waiting for services to be ready..."
    sleep 15
    
    # Check service status
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    
    echo ""
    print_success "AutoDev Agent is running!"
    echo ""
    echo "📍 Access the application:"
    echo "   🌐 Frontend:  http://localhost:3000"
    echo "   🔧 Backend:   http://localhost:8000"
    echo "   📚 API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📊 View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose down"
    echo ""
    
    # Try to open in browser
    if command -v open &> /dev/null; then
        print_info "Opening dashboard in browser..."
        sleep 3
        open http://localhost:3000
    fi
    
    echo ""
    print_success "Setup complete! Happy coding! 🎉"
else
    echo ""
    print_info "To start services later, run:"
    echo "   docker-compose up -d"
fi

echo ""
print_info "Need help? Check out:"
echo "   📖 QUICKSTART.md - Quick start guide"
echo "   📘 README.md - Full documentation"
echo "   🚀 DEPLOYMENT.md - Deployment guide"
