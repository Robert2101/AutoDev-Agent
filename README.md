# AutoDev Agent - The Self-Healing Repository 🤖

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> An autonomous AI agent that audits GitHub repositories, detects bugs and security vulnerabilities using the Gemini API, and automatically opens Pull Requests with code fixes.

## 🎯 Elevator Pitch

Imagine a world where bugs fix themselves. **AutoDev Agent** is an autonomous AI-powered system that:

- 🔍 **Audits** your GitHub repositories automatically
- 🐛 **Detects** bugs, security vulnerabilities, and code smells
- 🤖 **Fixes** issues using Gemini 1.5 Pro AI
- 🔄 **Opens** Pull Requests with verified fixes
- ✅ **Validates** fixes before proposing changes

## 🏗️ Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Next.js    │─────▶│   FastAPI    │─────▶│    Redis     │
│   Frontend   │      │   Backend    │      │    Queue     │
└──────────────┘      └──────────────┘      └──────────────┘
                                                    │
                                                    ▼
                                             ┌──────────────┐
                                             │    Celery    │
                                             │    Worker    │
                                             └──────────────┘
                                                    │
                                                    ▼
                                             ┌──────────────┐
                                             │   Gemini     │
                                             │   1.5 Pro    │
                                             └──────────────┘
```

### Task Queue Architecture

Instead of synchronous processing (user waiting on loading screen), we use a **message queue**:

1. **User Input**: Submit GitHub URL via frontend
2. **Queueing**: Backend pushes job to Redis
3. **Worker Execution**: Background worker processes the repository
4. **Validation**: Worker verifies fixes don't break the build
5. **Action**: Creates branch and opens Pull Request
6. **Notification**: User notified via WebSocket

## 🚀 Tech Stack

### Frontend
- **Next.js 14** - Modern React framework
- **TailwindCSS** - Utility-first styling
- **Socket.io** - Real-time updates
- **Framer Motion** - Smooth animations

### Backend
- **FastAPI** - High-performance Python API
- **PostgreSQL** - Robust database
- **Redis + Celery** - Task queue system
- **SQLAlchemy** - ORM

### AI & Integrations
- **Google Gemini 1.5 Pro** - Large context window for code analysis
- **PyGithub** - GitHub API integration

### DevOps
- **Docker Compose** - Multi-container orchestration
- **Git** - Version control with conventional commits

## 📁 Project Structure

```
autodev-agent/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   └── lib/             # Utilities
│   └── Dockerfile
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Configuration
│   │   ├── models/          # Database models
│   │   └── services/        # Business logic
│   └── Dockerfile
│
├── worker/                   # Celery worker
│   ├── tasks/               # Background tasks
│   └── agents/              # AI agent logic
│
├── docker-compose.yml
└── README.md
```

## 🎨 Key Features

### 1. Intelligent Context Retrieval (RAG)
- Skips irrelevant files (node_modules, .git, images)
- Reads package.json/requirements.txt for dependency awareness
- Priority-based file processing

### 2. Safety Valve (Pull Request vs. Commit)
- **Never commits directly to main**
- Creates feature branches (e.g., `fix/ai-auto-patch-001`)
- Opens Pull Requests for human review

### 3. Secret Scanning
- Detects hardcoded API keys
- Identifies exposed credentials
- Scans for SQL injection vulnerabilities

### 4. Code Validation
- Runs build/lint commands before PR
- Ensures fixes don't break the build
- Rollback on validation failure

## 🔧 Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Git
- Gemini API Key
- GitHub Personal Access Token

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/autodev-agent.git
cd autodev-agent
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Start with Docker Compose**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 Usage

1. Navigate to http://localhost:3000
2. Enter a GitHub repository URL
3. Click "Analyze Repository"
4. Monitor real-time progress
5. Review the Pull Request created by the agent

## 🧠 Prompt Engineering Strategy

The agent uses a **Chain of Thought** approach:

```
You are a Senior Software Engineer. I am providing you with a file server.js.

1. Analyze the code for logic errors, race conditions, or syntax errors.
2. Explain the bug strictly.
3. Provide the full corrected code block.
4. Do not remove comments unless necessary.
```

## 🐳 Docker Services

| Service    | Port | Description                    |
|------------|------|--------------------------------|
| Frontend   | 3000 | Next.js web application        |
| Backend    | 8000 | FastAPI server                 |
| Worker     | -    | Celery background worker       |
| Redis      | 6379 | Message broker                 |
| PostgreSQL | 5432 | Database                       |

## 🔐 Environment Variables

```env
# Backend
DATABASE_URL=postgresql://user:pass@db:5432/autodev
REDIS_URL=redis://redis:6379/0
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Worker Development
```bash
cd backend
celery -A worker.worker worker --loglevel=info
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 Success Metrics

- ✅ Successfully clone and analyze repositories
- ✅ Detect syntax, logic, and security bugs
- ✅ Generate valid code fixes
- ✅ Create Pull Requests automatically
- ✅ Provide real-time status updates
- ✅ Handle errors gracefully

## 🚧 Roadmap

- [ ] Multi-language support (JS, Python, Go, Rust)
- [ ] Custom rule configuration
- [ ] Team collaboration features
- [ ] Analytics dashboard
- [ ] GitHub App integration
- [ ] CI/CD integration
- [ ] Slack/Discord notifications

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini Team for the amazing AI API
- FastAPI for the robust Python framework
- Next.js team for the excellent React framework

## 📧 Contact

For questions or support, open an issue or contact the maintainers.

---

**Built with ❤️ using AI-powered development**
