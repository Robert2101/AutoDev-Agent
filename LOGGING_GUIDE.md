# 📊 Logging & Monitoring Guide

## 🔍 How to Check Logs

When you submit a repository and it shows "pending", here's how to check what's happening:

---

## Quick Commands

### View All Logs (Real-time)
```bash
docker-compose logs -f
```

### View Specific Service Logs

```bash
# Worker logs (to see AI processing)
docker-compose logs -f worker

# Backend logs (to see API requests)
docker-compose logs -f backend

# Frontend logs (to see UI issues)
docker-compose logs -f frontend

# Database logs
docker-compose logs -f db

# Redis logs
docker-compose logs -f redis
```

### View Last N Lines

```bash
# Last 50 lines from worker
docker-compose logs --tail=50 worker

# Last 100 lines from backend
docker-compose logs --tail=100 backend
```

### Search Logs

```bash
# Search for errors in worker
docker-compose logs worker | grep -i error

# Search for a specific audit ID
docker-compose logs worker | grep "audit_id: 123"

# Find POST requests to create audits
docker-compose logs backend | grep "POST /api/audits"
```

---

## 🎯 Common Scenarios

### 1. Repository Stays "Pending"

**Check worker logs**:
```bash
docker-compose logs -f worker
```

**What to look for**:
- ✅ `Connected to redis` - Worker is connected
- ✅ `celery@... ready` - Worker is running
- ✅ `Received task:` - Task was received
- ❌ `TypeError`, `Exception` - There's an error

**Common issues**:
- Worker not receiving tasks → Check Redis connection
- Task failing → Look for error messages
- API keys missing → Check .env file

### 2. Repository Fails During Cloning

**Check worker logs**:
```bash
docker-compose logs worker | grep -A 20 "clone"
```

**Common issues**:
- Repository URL invalid
- Branch doesn't exist
- Repository is private (needs authentication)

### 3. API Returns 500 Error

**Check backend logs**:
```bash
docker-compose logs backend | grep -A 30 "500"
```

**What to look for**:
- Traceback showing the error
- Database connection issues
- Validation errors

### 4. Frontend Not Loading Data

**Check browser console** (F12 → Console tab):
- CORS errors
- Network errors
- 404/500 responses

**Check backend logs**:
```bash
docker-compose logs backend | grep "GET /api"
```

---

## 📋 Log Monitoring Workflow

### Step-by-Step: Debugging a Pending Audit

1. **Submit a repository** via the frontend

2. **Open worker logs in real-time**:
   ```bash
   docker-compose logs -f worker
   ```

3. **Watch for**:
   ```
   [INFO] Starting audit for <owner>/<repo>
   [INFO] Step 1: Cloning repository...
   [INFO] Step 2: Analyzing files...
   [INFO] Found 15 files to analyze
   [INFO] Processed 1/15 files
   ...
   [INFO] Step 3: Applying fixes
   [INFO] Step 4: Creating Pull Request
   [INFO] Audit completed successfully
   ```

4. **If you see errors**, note the error message and check:
   - Missing API keys in `.env`
   - Invalid repository URL
   - Network connectivity issues

---

## 🐛 Troubleshooting Common Issues

### Issue: "Task not received by worker"

**Check**:
```bash
# Verify worker is running
docker-compose ps worker

# Check worker logs
docker-compose logs worker | tail -50

# Check Redis connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

**Fix**:
```bash
# Restart worker
docker-compose restart worker
```

### Issue: "Missing API key errors"

**Check .env file**:
```bash
cat .env | grep -E "GEMINI|GITHUB"
```

**Should see**:
```
GEMINI_API_KEY=AIza... (actual key, not placeholder)
GITHUB_TOKEN=ghp_... (actual token, not placeholder)
```

**Fix**:
1. Edit `.env` with real keys
2. Restart services:
   ```bash
   docker-compose restart
   ```

### Issue: "Database connection failed"

**Check database**:
```bash
# Check if DB is running
docker-compose ps db

# Test connection
docker-compose exec db psql -U autodev -d autodev_db -c "SELECT 1;"
```

**Fix**:
```bash
# Restart database
docker-compose restart db

# If data is corrupted, reset (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

---

## 📊 Monitoring Dashboard

### View Service Status
```bash
docker-compose ps
```

Output:
```
NAME                STATUS
autodev-db          Up (healthy)
autodev-redis       Up (healthy)
autodev-backend     Up
autodev-worker      Up
autodev-frontend    Up
```

### Check Resource Usage
```bash
docker stats
```

Shows CPU, Memory, Network usage for each container.

### Check Disk Space
```bash
docker system df
```

---

## 🎯 Advanced Debugging

### Follow a Specific Audit

1. **Get audit ID** from frontend URL:
   ```
   http://localhost:3000/audit/123
   ```

2. **Watch worker logs for that audit**:
   ```bash
   docker-compose logs -f worker | grep "audit.*123"
   ```

### View Database Records

```bash
# Connect to database
docker-compose exec db psql -U autodev -d autodev_db

# View audits
SELECT id, status, created_at FROM audits;

# View issues for an audit
SELECT file_path, issue_type, severity FROM issues WHERE audit_id = 1;

# Exit
\q
```

### Check Celery Queue

```bash
# See pending tasks
docker-compose exec redis redis-cli LLEN celery

# View task details
docker-compose exec redis redis-cli LRANGE celery 0 -1
```

---

## 📝 Useful Log Patterns

### Worker Processing Flow

```
✅ Good flow:
[INFO] Connected to redis
[INFO] celery@... ready
[INFO] Received task: process_repository_audit
[INFO] Starting audit for user/repo
[INFO] Step 1: Cloning repository
[INFO] Step 2: Analyzing files
[INFO] Found 10 files
[INFO] Processed 10/10 files
[INFO] Step 3: Applying fixes
[INFO] Step 4: Creating Pull Request
[INFO] Audit completed successfully

❌ Error flow:
[ERROR] Task process_repository_audit failed
[ERROR] TypeError: ...
[ERROR] Audit failed: ...
```

### Backend API Flow

```
✅ Good flow:
INFO: POST /api/audits/ HTTP/1.1 201 Created
INFO: GET /api/audits/1 HTTP/1.1 200 OK

❌ Error flow:
INFO: POST /api/audits/ HTTP/1.1 500 Internal Server Error
ERROR: Exception in ASGI application
Traceback...
```

---

## 🚨 Emergency Commands

### Restart Everything
```bash
docker-compose restart
```

### Stop and Start Fresh
```bash
docker-compose down
docker-compose up -d
```

### Reset Database (DANGER: Deletes all data!)
```bash
docker-compose down -v
docker-compose up -d
```

### Rebuild Containers
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 Quick Reference

| Issue | Command | What to Look For |
|-------|---------|------------------|
| Pending audit | `docker-compose logs -f worker` | Task received, processing steps |
| 500 error | `docker-compose logs backend \| grep 500` | Exception traceback |
| Cloning fails | `docker-compose logs worker \| grep clone` | Git errors |
| No PR created | `docker-compose logs worker \| grep PR` | GitHub API errors |
| Worker not starting | `docker-compose logs worker` | Redis connection, imports |
| Database issues | `docker-compose logs db` | Connection refused, auth failed |

---

## 💡 Pro Tips

1. **Use `-f` flag** for real-time logs:
   ```bash
   docker-compose logs -f worker
   ```

2. **Combine grep with colors**:
   ```bash
   docker-compose logs worker | grep --color=always -i error
   ```

3. **Save logs to file** for analysis:
   ```bash
   docker-compose logs worker > worker-logs.txt
   ```

4. **Watch multiple services**:
   ```bash
   docker-compose logs -f worker backend
   ```

5. **Filter by timestamp**:
   ```bash
   docker-compose logs --since 5m worker
   docker-compose logs --until 2026-01-31T14:00:00 worker
   ```

---

## ✅ Current Fix Applied

**Issue**: Repository stays in "pending" status  
**Root Cause**: Celery task signature expected `db` parameter  
**Fix**: Changed task to accept `**kwargs` and extract `db` from it  
**Status**: ✅ FIXED - Try submitting a new repository now!

---

## 🎯 Next Steps

1. **Submit a new repository** (the previous one won't auto-retry)
2. **Watch the logs**: `docker-compose logs -f worker`
3. **See the magic happen**! 🎉

---

*Remember: Logs are your best friend when debugging! 📊*
