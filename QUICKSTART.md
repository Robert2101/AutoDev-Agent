# ⚡ Quick Start - AutoDev Agent

Get AutoDev Agent running in **under 5 minutes**!

## Prerequisites

- Docker & Docker Compose installed
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- GitHub Token ([Generate here](https://github.com/settings/tokens))

## 1️⃣ Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd autodev-agent

# Copy environment template
cp .env.example .env
```

## 2️⃣ Add Your API Keys

Edit `.env` and add:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

## 3️⃣ Start the Application

```bash
# Easy mode - use the start script
./start.sh

# Manual mode
docker-compose up -d
```

## 4️⃣ Access the Dashboard

🌐 Open http://localhost:3000

## 5️⃣ Submit Your First Repository

1. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
2. Click "Start AI Audit"
3. Watch the magic happen! ✨

## 📊 View Progress

- **Dashboard**: Real-time status updates
- **Statistics**: Overview of all audits
- **Details**: Click any audit to see detected issues

## 🔍 What Happens?

1. **Clone**: Repository is cloned locally
2. **Analyze**: AI scans code for bugs and vulnerabilities
3. **Fix**: Automated fixes are generated
4. **PR**: Pull Request is created with fixes

## 🎯 Example Repositories to Try

```
https://github.com/your-username/your-project
```

Small projects work best for testing!

## 🛑 Stop Services

```bash
docker-compose down
```

## 📚 Need Help?

- **Full Docs**: See [README.md](README.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: Check the troubleshooting guide

## 🎉 That's It!

You now have a fully functional AI-powered code auditing system running locally!

---

**Next Steps**:
- Try auditing your own repositories
- Review the generated Pull Requests
- Customize the AI prompts for your needs
- Deploy to production (see DEPLOYMENT.md)

Happy Auditing! 🤖
