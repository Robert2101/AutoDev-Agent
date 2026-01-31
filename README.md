# AutoDev Agent - The Self-Healing Repository 🤖

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-purple)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **An autonomous AI agent that audits GitHub repositories, detects bugs & security vulnerabilities using Google Gemini 2.5 Flash, and automatically opens Pull Requests with fixed code.**

---

## 🎯 What is AutoDev Agent?

Imagine a world where bugs fix themselves. **AutoDev Agent** is an autonomous AI-powered system that:

- 🔍 **Audits** your GitHub repositories automatically.
- 🐛 **Detects** bugs, security vulnerabilities, and code smells.
- 🤖 **Fixes** issues using state-of-the-art **Gemini 2.5 Flash** AI.
- 🔄 **Opens** Pull Requests with verified fixes.
- 🔐 **Secure** handling of credentials and API keys.

---

## 🚀 Key Features

### 1. Multi-User & Dynamic Configuration
- **Custom API Keys**: Users can provide their own `GitHub Token` and `Gemini API Key` for specific audits via the "Advanced Settings" UI.
- **Privacy First**: Credentials are used only for the requested audit and not stored permanently if passed dynamicallly.

### 2. Intelligent Context & RAG
- Skips irrelevant files (`node_modules`, `.git`, `dist`).
- Prioritizes source code analysis based on language (`.py`, `.js`, `.ts`, `.go`, `.rs`, etc.).

### 3. Automated PR Creation
- **Safety Valve**: Never commits directly to `main`.
- Creates isolated branches (e.g., `fix/ai-auto-patch-ID`).
- Push changes and opens a PR with a detailed summary.

### 4. Robust Error Handling
- **Rate Limit Handling**: Automatically pauses and retries (Exponential Backoff) if AI quotas are exceeded.
- **Auth Diagnostics**: Detects permission errors (e.g., missing `repo` scope) and guides users to fix them.

---

## 🔧 Setup & Installation

### Prerequisites
1.  **Docker Desktop** (Running).
2.  **Git** installed.
3.  **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey)).
4.  **GitHub Personal Access Token** ([Get it here](https://github.com/settings/tokens)).
    -   **Required Scope**: `repo` (Full control of private repositories).

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-org/autodev-agent.git
cd autodev-agent
```

### Step 2: Configure Environment
Create a `.env` file in the root directory:

```bash
# Copy example file (if available) or create new
touch .env
```

**Add the following content to `.env`:**

```env
# AI Configuration
GEMINI_API_KEY=AIzaSy...your-gemini-key

# GitHub Configuration
GITHUB_TOKEN=ghp_...your-github-token

# Database & Infrastructure
POSTGRES_USER=autodev
POSTGRES_PASSWORD=autodev_password
POSTGRES_DB=autodev_db
DATABASE_URL=postgresql://autodev:autodev_password@db:5432/autodev_db
REDIS_URL=redis://redis:6379/0

# App Configuration
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## ⚡ How to Run

We provide automated scripts for a "One-Button" start experience on all platforms.

### 🪟 Windows Users
Double-click `start.bat` or run in Command Prompt:

```cmd
.\start.bat
```

### 🍎 Mac / 🐧 Linux Users
Run the shell script:

```bash
./start.sh
```

### 🐳 Manual Method
If you prefer running Docker Compose directly:

```bash
docker-compose up -d
```

---

## 📖 Usage Guide

1.  **Access Dashboard**: Open [http://localhost:3000](http://localhost:3000).
2.  **Submit Repository**:
    -   Enter GitHub URL (e.g., `https://github.com/owner/repo`).
    -   (Optional) Click **Advanced Settings** to use a custom GitHub Token or Gemini Key for this specific audit.
3.  **Monitor Progress**:
    -   Watch "Live Logs" to see the agent cloning, analyzing, and fixing.
    -   If the agent hits a rate limit (429), it will warn you and retry automatically.
4.  **Review Fixes**:
    -   Once complete, click the **Pull Request Link** to view changes on GitHub.

---

## 🏗️ Project Structure

```
autodev-agent/
├── frontend/                 # Next.js 14 Application (UI)
│   ├── src/app/             # Pages & Routes
│   └── src/components/      # UI Components (RepoForm, AuditList)
│
├── backend/                  # FastAPI Application (API)
│   ├── app/api/             # Endpoints
│   ├── app/models/          # SQL Models
│   └── worker/              # Celery Task Worker
│       ├── tasks/           # Audit Logic (Cloning, Git Ops)
│       └── agents/          # AI Logic (GeminiAgent)
│
├── docker-compose.yml       # Service Orchestration
├── start.bat                # Windows Start Script
├── start.sh                 # Mac/Linux Start Script
└── README.md                # Documentation
```

---

## 🛠️ Troubleshooting

### ❌ Git Push Failed (403 Forbidden)
- **Cause**: Your GitHub Token does not have write permissions.
- **Fix**: Regenerate your token and ensure the **`repo`** scope box is checked. Update `.env` or use "Advanced Settings".

### ⚠️ AI Agent is Busy (Rate Limit)
- **Cause**: You exceeded the free tier quota for Gemini API.
- **Fix**: The agent will auto-retry in ~60 seconds. Just wait. OR use a different API key in "Advanced Settings".

### � Docker Issues
- Ensure Docker Desktop is running.
- Run `docker-compose down` followed by `docker-compose up -d --build` to reset.

---

## 📝 License
MIT License.

## 🔄 System Flow Diagram


graph TD
    A[User] -->|Submit Repo URL| B[Frontend (Next.js)]
    B -->|POST /audits| C[Backend API (FastAPI)]
    C -->|Push Job| D[Redis Queue]
    D -->|Pop Job| E[Celery Worker]
    E -->|Git Clone| F[Temp Storage]
    E -->|Analyze Code| G[Gemini AI (2.5 Flash)]
    G -->|Return Issues| E
    E -->|Generate Fixes| G
    E -->|Apply Fixes| F
    E -->|Git Push & PR| H[GitHub]
    H -->|PR Created| A
    E -->|Update Status| I[Postgres DB]
    C -->|Read Status| I
    B -->|Poll Status| C

