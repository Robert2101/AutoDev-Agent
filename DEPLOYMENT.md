# 🚀 Deployment Guide - AutoDev Agent

This guide will help you deploy AutoDev Agent locally or on a production server.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- **Git** (v2.30+)
- **GitHub Personal Access Token** with `repo` permissions
- **Google Gemini API Key**

### Getting API Keys

#### 1. GitHub Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "AutoDev Agent")
4. Select scopes:
   - ✓ `repo` (Full control of private repositories)
   - ✓ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy and save the token** (you won't see it again!)

#### 2. Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Select a Google Cloud project or create a new one
4. Click "Create API key in existing project"
5. **Copy and save the API key**

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/autodev-agent.git
cd autodev-agent
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env  # or use your preferred editor
```

**Required variables to update:**

```env
# Update these with your actual API keys
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here

# Update this with a secure random string in production
SECRET_KEY=your_super_secret_key_here_change_in_production
```

### Step 3: Build and Start Services

```bash
# Build all Docker images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Step 5: Verify Services

```bash
# Check service status
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

## Production Deployment

### Option 1: Docker Compose on VPS

#### 1. Provision a Server

- **Recommended specs**:
  - 4 CPU cores
  - 8GB RAM
  - 50GB SSD
  - Ubuntu 22.04 LTS

Popular providers: DigitalOcean, AWS EC2, Google Cloud, Azure

#### 2. Install Docker

```bash
# Update packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Clone and Configure

```bash
# Clone repository
git clone https://github.com/your-username/autodev-agent.git
cd autodev-agent

# Set up environment
cp .env.example .env
nano .env  # Update with production values
```

#### 4. Production Configuration

Update `.env` for production:

```env
# Use strong, random passwords
POSTGRES_PASSWORD=<strong-random-password>
SECRET_KEY=<strong-random-secret>

# Production URLs
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

#### 5. Set Up Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt-get install nginx -y

# Create configuration
sudo nano /etc/nginx/sites-available/autodev
```

Add this configuration:

```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/autodev /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### 6. Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get SSL certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

#### 7. Start Production Services

```bash
# Build and start
docker-compose up -d --build

# Verify
docker-compose ps
docker-compose logs -f
```

#### 8. Set Up Auto-start on Reboot

```bash
# Create systemd service
sudo nano /etc/systemd/system/autodev.service
```

Add:

```ini
[Unit]
Description=AutoDev Agent
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/your-user/autodev-agent
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable autodev.service
sudo systemctl start autodev.service
```

### Option 2: Kubernetes Deployment

(For advanced users or high-traffic deployments)

1. Create Kubernetes manifests
2. Set up secrets for API keys
3. Deploy with `kubectl apply`
4. Use Ingress for routing
5. Set up autoscaling

See `k8s/` directory for example manifests (coming soon).

## Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | Yes | - | Redis connection string |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `GITHUB_TOKEN` | Yes | - | GitHub Personal Access Token |
| `SECRET_KEY` | Yes | - | Secret key for JWT tokens |
| `CLONE_DIR` | No | `/tmp/autodev-clones` | Directory for cloning repos |
| `MAX_FILE_SIZE` | No | `1048576` (1MB) | Max file size to process |
| `MAX_FILES_PER_REPO` | No | `100` | Max files per repository |

### Database Migrations

```bash
# Access backend container
docker-compose exec backend bash

# Run migrations (if using Alembic)
alembic upgrade head
```

### Scaling Workers

To handle more concurrent audits, scale the worker service:

```bash
# Scale to 3 workers
docker-compose up -d --scale worker=3
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs worker
docker-compose logs frontend

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Issues

```bash
# Check database logs
docker-compose logs db

# Connect to database
docker-compose exec db psql -U autodev -d autodev_db

# Reset database
docker-compose down -v  # WARNING: This deletes data!
docker-compose up -d
```

### Redis Connection Issues

```bash
# Check Redis
docker-compose exec redis redis-cli ping
# Should return: PONG

# View Redis logs
docker-compose logs redis
```

### Worker Not Processing Jobs

```bash
# Check worker logs
docker-compose logs -f worker

# Restart worker
docker-compose restart worker

# Check Celery queue
docker-compose exec redis redis-cli LLEN celery

# Purge queue (if stuck)
docker-compose exec worker celery -A worker.worker purge
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a

# Clean clone directory
rm -rf /tmp/autodev-clones/*

# Check disk usage
df -h
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Check API connectivity
curl http://localhost:8000/health

# Rebuild frontend
docker-compose up -d --build frontend
```

## Monitoring

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f worker
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

## Backup & Recovery

### Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U autodev autodev_db > backup_$(date +%Y%m%d).sql

# Restore backup
cat backup_20240131.sql | docker-compose exec -T db psql -U autodev -d autodev_db
```

### Full Backup

```bash
# Stop services
docker-compose down

# Backup volumes
docker run --rm -v autodev-agent_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data

# Restart
docker-compose up -d
```

## Updating

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Support

For issues and questions:
- 📖 [Documentation](README.md)
- 🐛 [Issue Tracker](https://github.com/your-org/autodev-agent/issues)
- 💬 [Discussions](https://github.com/your-org/autodev-agent/discussions)

---

**Happy Deploying! 🚀**
