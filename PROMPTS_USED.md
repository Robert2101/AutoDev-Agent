# 🧠 Prompts Used to Build AutoDev Agent

The following is a collection of the high-level engineering prompts used to architect and implement the AutoDev Agent. These prompts demonstrate a "Chain of Thought" approach to building complex AI-driven systems.

## Phase 1: System Architecture & Design

### Prompt 01: Core Architecture Design
> **Role**: Senior System Architect
> **Context**: We are building "AutoDev Agent", an autonomous code auditing system that fixes bugs automatically.
> **Requirement**: Design a scalable, microservices-based architecture.
> **Constraints**:
> - Use Docker Compose for orchestration.
> - Backend: FastAPI (Python) for speed and async capabilities.
> - Frontend: Next.js 14 for a modern, reactive UI.
> - Task Queue: Celery + Redis for handling long-running AI analysis jobs.
> - Database: PostgreSQL for persistent audit logs.
> **Output**: Provide a comprehensive `IMPLEMENTATION_PLAN.md` including:
> 1. High-level diagram (ASCII).
> 2. Database Schema (SQLAlchemy models).
> 3. API Endpoints definition.
> 4. Celery Task definitions (Audit, Analyze, Fix, PR).

### Prompt 02: AI Agent Logic Design
> **Role**: AI Engineer
> **Task**: Design the core `GeminiAgent` class that handles code analysis.
> **Requirements**:
> - The agent must take a file content and a system prompt.
> - It must output purely structured JSON (no markdown fluff).
> - It needs to handle "Chain of Thought" reasoning before outputting the fix.
> - Include a method `scan_for_secrets()` using a specialized security prompt.
> **Output**: Python class structure with type hints and detailed Docstrings.

---

## Phase 2: Backend Implementation

### Prompt 03: Celery Worker & Git Operations
> **Role**: Backend Developer (Python Expert)
> **Task**: Implement the `process_repository_audit` Celery task.
> **Logic Flow**:
> 1. Receive a GitHub URL.
> 2. Clone the repo to a temporary directory (`/tmp/clones`).
> 3. Walk through all files (respecting `.gitignore`).
> 4. For each file, invoke `GeminiAgent.analyze()`.
> 5. If issues are found, apply the JSON-based fixes to the file system.
> 6. Create a new git branch `fix/ai-patch-{id}`.
> 7. Push changes and open a PR.
> **Security**: Ensure GITHUB_TOKEN is handled securely and never logged in plain text.

### Prompt 04: Rate Limiting & Robustness
> **Role**: DevOps Engineer
> **Problem**: The Gemini API throws `429 Too Many Requests`.
> **Task**: Implement a robust Exponential Backoff retry mechanism in the `GeminiAgent`.
> **Details**:
> - Catch `429` errors specifically.
> - Wait 60 seconds before retrying.
> - Retry up to 3 times.
> - Log warnings to the database so the frontend can display a "Waiting..." status.

---

## Phase 3: Frontend Development

### Prompt 05: Modern Audit Dashboard
> **Role**: Frontend Developer (React/Tailwind Specialist)
> **Task**: Build the main `AuditDetail` page.
> **Design Requirements**:
> - **Dark Mode**: Use a "Glassmorphism" aesthetic with slate/zinc colors.
> - **Live Logs**: A real-time terminal-like window showing Celery logs.
> - **Issue Cards**: Render each detected issue as a card with a "Diff View" (Original vs Fixed Code).
> - **Status Badges**: Animated pills for "Analyzing", "Fixing", "Completed".
> **Tech Stack**: Next.js 14 (App Router), Lucide React (Icons), TailwindCSS.

---

## Phase 4: DevOps & Documentation

### Prompt 06: Automated Setup Script
> **Role**: Release Engineer
> **Task**: Write a "One-Button" start script (`start.sh`).
> **Requirements**:
> - It should check if Docker is running.
> - It should spin up the entire stack (`docker-compose up -d`).
> - It should print pretty ASCII art and clickable local URLs (Backend, Frontend).
> - Include a `DEVELOPER_GUIDE.md` explaining how to reload the worker container after code changes.

### Prompt 07: Troubleshooting Guide
> **Role**: Technical Writer
> **Task**: Create a `TOKEN_SCOPE_ISSUE.md` to help users fix 403 Git errors.
> **Content**:
> - explain WHY the error happens (missing `repo` scope).
> - Provide a numbered list of steps to generate the correct GitHub Personal Access Token.
> - Explain how to update the `.env` file and restart.
