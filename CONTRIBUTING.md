# Contributing to AutoDev Agent

Thank you for your interest in contributing to AutoDev Agent! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Docker version, etc.)

### Suggesting Features

We welcome feature suggestions! Please:
- Check if it's already been suggested
- Provide a clear use case
- Explain the expected behavior
- Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Write clear commit messages
   - Add tests if applicable

4. **Commit with conventional commits**
   ```bash
   git commit -m "feat(backend): add secret scanning feature"
   ```

   Conventional commit types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, etc.)
   - `refactor`: Code refactoring
   - `test`: Adding tests
   - `chore`: Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Code Style:**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

**Testing:**
```bash
pytest
```

### Frontend (TypeScript/React)

```bash
cd frontend
npm install
npm run dev
```

**Code Style:**
- Follow TypeScript best practices
- Use functional components with hooks
- Keep components small and focused
- Use meaningful variable names

**Linting:**
```bash
npm run lint
```

### Docker Development

```bash
# Build specific service
docker-compose build backend

# View logs
docker-compose logs -f backend

# Execute commands in container
docker-compose exec backend bash
```

## Project Structure

```
autodev-agent/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   └── worker/          # Celery worker
├── frontend/            # Next.js frontend
│   └── src/
│       ├── app/         # Pages
│       ├── components/  # React components
│       └── lib/         # Utilities
└── docker-compose.yml   # Orchestration
```

## Coding Standards

### Python

```python
def process_repository(repo_url: str) -> dict:
    """
    Process a GitHub repository for audit.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Dictionary with audit results
    """
    # Implementation
    pass
```

### TypeScript

```typescript
interface Repository {
  id: number;
  url: string;
  owner: string;
  name: string;
}

export function formatRepoName(repo: Repository): string {
  return `${repo.owner}/${repo.name}`;
}
```

## Commit Message Guidelines

Format: `<type>(<scope>): <subject>`

Examples:
```
feat(worker): add support for Rust language analysis
fix(frontend): resolve issue with audit list pagination
docs(readme): update installation instructions
refactor(backend): improve database query performance
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
docker-compose up -d
# Run integration tests
docker-compose down
```

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment-related changes
- Add inline comments for complex logic
- Update API documentation if endpoints change

## Release Process

1. Update version in package.json / __init__.py
2. Update CHANGELOG.md
3. Create a PR to main
4. After merge, create a GitHub release
5. Tag the release (e.g., v1.0.0)

## Getting Help

- 📖 Read the [README](README.md)
- 💬 [Discussions](https://github.com/your-org/autodev-agent/discussions)
- 🐛 [Issues](https://github.com/your-org/autodev-agent/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏
