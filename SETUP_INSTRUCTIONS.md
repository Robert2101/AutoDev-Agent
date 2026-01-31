# 🎯 SETUP INSTRUCTIONS - READ THIS FIRST!

## ✅ Status: .env file created successfully at project root!

The `.env` file is located at:
```
/Users/b.jessyrobert/Desktop/AutoDev Agent/.env
```

## 🔑 You Need to Add 2 API Keys

### 1️⃣ Gemini API Key (Required)

**Get it here:** https://makersuite.google.com/app/apikey

Steps:
1. Visit the link above
2. Click "Create API Key"
3. Select a Google Cloud project (or create new one)
4. Copy the API key

### 2️⃣ GitHub Personal Access Token (Required)

**Get it here:** https://github.com/settings/tokens

Steps:
1. Click "Generate new token (classic)"
2. Give it a name: "AutoDev Agent"
3. ✅ Check the `repo` scope (Full control of private repositories)
4. Click "Generate token"
5. **Copy the token immediately** (you won't see it again!)

## 📝 How to Add API Keys

### Option A: Edit .env file manually

Open the file and replace the placeholders:
```bash
# Edit the .env file
nano .env
# or
code .env  # if you have VS Code
```

Replace:
```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE
```

With your actual keys:
```env
GEMINI_API_KEY=AIzaSyD...your-actual-key
GITHUB_TOKEN=ghp_...your-actual-token
```

### Option B: Use the interactive setup script

```bash
./setup.sh
# Follow the prompts to enter your keys
```

## 🚀 After Adding Keys

Run this command to start everything:
```bash
docker-compose up -d
```

Or use the quick start script:
```bash
./start.sh
```

### Windows Users
Use the `start.bat` script:
```cmd
start.bat
```

## ❓ Important Notes

### Do I need PostgreSQL or Redis installed locally?
**NO!** Docker handles everything. PostgreSQL and Redis run in containers.

You do NOT need to run:
- ❌ `brew install postgresql`
- ❌ `brew install redis`

Docker Compose automatically:
- ✅ Downloads PostgreSQL image
- ✅ Downloads Redis image
- ✅ Creates containers
- ✅ Sets up networking
- ✅ Manages data persistence

### What's included in Docker?
The `docker-compose up` command starts 5 services:
1. **db** - PostgreSQL database (port 5432)
2. **redis** - Redis message broker (port 6379)
3. **backend** - FastAPI server (port 8000)
4. **worker** - Celery background worker
5. **frontend** - Next.js app (port 3000)

## 🎯 Quick Summary

```
1. ✅ .env file created - Located in project root
2. 🔑 Add API keys - Edit .env file
3. 🚀 Run: docker-compose up -d
4. 🌐 Open: http://localhost:3000
```

## 🆘 Troubleshooting

### "Docker is not running"
- Open Docker Desktop application
- Wait for it to fully start
- Try again

### "API key is invalid"
- Double-check you copied the full key
- Make sure there are no extra spaces
- Gemini key starts with: `AIza...`
- GitHub token starts with: `ghp_...`

### "Port already in use"
Stop any existing services using ports 3000, 8000, 5432, or 6379:
```bash
docker-compose down
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

---

## ✨ Ready to Start?

Once you've added your API keys, run:
```bash
docker-compose up -d
```

Then open: **http://localhost:3000**

Enjoy! 🎉
