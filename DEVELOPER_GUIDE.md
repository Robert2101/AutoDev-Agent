# 👨‍💻 AutoDev Agent - Developer Guide

Everything you need to run, modify, and understand the project workflow.

## 🚀 One-Button Start
To start the entire system (Backend, Frontend, DB, Redis, Worker):

```bash
./start.sh
```
Or manually:
```bash
docker-compose up -d
```

- **Dashboard**: [http://localhost:3000](http://localhost:3000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Flower (Celery Monitor)**: [http://localhost:5555](http://localhost:5555) (if enabled)

---

## 🔄 Development Workflow
The system is designed for rapid development. Here is how changes reflect:

### 1. Frontend (`frontend/src/`)
- **Technology**: Next.js 14, TailwindCSS.
- **Reflects**: **Instantly (Hot Reload)**.
- **Action**: Edit any `.tsx` or `.ts` file and check the browser. No restart needed.

### 2. Backend API (`backend/app/`)
- **Technology**: FastAPI.
- **Reflects**: **Instantly (Hot Reload)**.
- **Action**: Edit any route or schema in `backend/app`. Uvicorn will detect changes and reload the server container automatically.

### 3. AI Agent / Worker (`backend/worker/`)
- **Technology**: Celery, Google Gemini.
- **Reflects**: **Requires Restart**.
- **Reason**: Use of Celery workers which load code into memory on startup.
- **Action**: 
  1. Edit `audit_task.py` or `gemini_agent.py`.
  2. Run:
     ```bash
     docker-compose restart worker
     ```
  3. Trigger a new audit to test.

### 4. Database Schema (`backend/app/models/`)
- **Reflects**: **Requires Migration / Restart**.
- **Action**: If you change `models.py`, you must ensure Alembic migrations are run (if configured) or restart the `db` and `backend` containers if using `create_all()`.

---

## 🌊 System Workflow

1.  **User Input**: User submits a GitHub URL (e.g., `https://github.com/owner/repo`) on the Dashboard.
2.  **API**: `POST /audits` creates a record in Postgres (`status: pending`).
3.  **Queue**: API pushes a task to Redis.
4.  **Worker (Celery)**:
    -   Picks up the task.
    -   **Clones** the repository to `/tmp/autodev-clones`.
    -   **Analyzes** files using `GeminiAgent` (Rate limited with backoff).
    -   **Parses** JSON response for issues.
    -   **Generates** fixes.
    -   **Pushes** changes to a new branch (`fix/ai-auto-patch-ID`).
    -   **Creates PR** on GitHub.
    -   updates Database status to `completed`.
5.  **Feedback**: Frontend polls the API and displays Live Logs and Results.

---

## 🛠️ Troubleshooting

### Authentication Errors (403)
If you see "Git Push failed (403)", your token lacks permissions.
- **Fix**: See [TOKEN_SCOPE_ISSUE.md](./TOKEN_SCOPE_ISSUE.md)

### Rate Limit Errors (429)
If the AI stops working:
- The system automatically waits **60 seconds** and retries.
- You will see a yellow warning card in the UI.

### Logs
To see what's happening under the hood:
```bash
docker-compose logs -f worker    # For AI logic
docker-compose logs -f backend   # For API issues
docker-compose logs -f frontend  # For UI issues
```
