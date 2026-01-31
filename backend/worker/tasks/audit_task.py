"""
Main repository audit task - The orchestrator of the self-healing process.
"""
from celery import Task
from sqlalchemy.orm import Session
import git
import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

from worker.worker import celery_app
from app.core.database import SessionLocal
from app.core.config import settings
from app.models import Audit, Repository, Issue, AuditStatus, IssueType, IssueSeverity
from worker.agents import gemini_agent, github_service

logger = logging.getLogger(__name__)

# File extensions to analyze
SUPPORTED_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.jsx': 'javascript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.go': 'go',
    '.rs': 'rust',
    '.cpp': 'cpp',
    '.c': 'c',
    '.rb': 'ruby',
    '.php': 'php',
}

# Files/directories to skip (RAG - Intelligent Context Retrieval)
SKIP_PATTERNS = {
    'node_modules', '.git', '__pycache__', 'venv', 'env', '.venv',
    'dist', 'build', 'target', '.idea', '.vscode', 'coverage',
    '.next', 'out', '.cache', 'vendor', 'pkg'
}


class AuditTask(Task):
    """Custom Celery task class with database session management."""
    
    def __call__(self, *args, **kwargs):
        """Override call to manage database sessions."""
        db = SessionLocal()
        try:
            return super().__call__(*args, db=db, **kwargs)
        finally:
            db.close()


def append_log(audit, db, level: str, message: str):
    """
    Append a log entry to the audit.
    
    Args:
        audit: Audit model instance
        db: Database session
        level: Log level (INFO, WARNING, ERROR, SUCCESS)
        message: Log message
    """
    from datetime import datetime
    
    if audit.logs is None:
        audit.logs = []
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'level': level,
        'message': message
    }
    
    # Append to logs
    audit.logs = audit.logs + [log_entry]
    db.commit()
    
    # Also log to console
    logger.log(
        logging.INFO if level == 'INFO' else 
        logging.WARNING if level == 'WARNING' else 
        logging.ERROR if level == 'ERROR' else 
        logging.INFO,
        message
    )


@celery_app.task(base=AuditTask, bind=True, name="worker.tasks.audit_task.process_repository_audit")
def process_repository_audit(self, audit_id: int, **kwargs):
    """
    Main task to process a repository audit.
    
    This is the orchestrator that:
    1. Clones the repository
    2. Maps the file structure (with RAG filtering)
    3. Analyzes code with Gemini AI
    4. Generates fixes
    5. Validates fixes
    6. Creates a Pull Request
    
    Args:
        audit_id: ID of the audit job
        **kwargs: Contains db session injected by AuditTask
    """
    db = kwargs.get('db')
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    
    if not audit:
        logger.error(f"Audit {audit_id} not found")
        return
    
    repository = audit.repository
    clone_path = None
    
    try:
        # Update status: Starting
        audit.status = AuditStatus.PENDING
        audit.started_at = datetime.utcnow()
        append_log(audit, db, 'INFO', f'🚀 Starting audit for {repository.owner}/{repository.name}')
        db.commit()
        
        # Step 1: Clone repository
        append_log(audit, db, 'INFO', f'📥 Step 1: Cloning repository...')
        audit.status = AuditStatus.CLONING
        db.commit()
        
        clone_path = clone_repository(repository.url, repository.branch)
        append_log(audit, db, 'SUCCESS', f'✅ Repository cloned successfully')
        
        # Step 2: Analyze files
        append_log(audit, db, 'INFO', f'🔍 Step 2: Discovering files to analyze...')
        audit.status = AuditStatus.ANALYZING
        db.commit()
        
        files_to_analyze = discover_files(clone_path)
        audit.total_files = len(files_to_analyze)
        db.commit()
        
        append_log(audit, db, 'INFO', f'📁 Found {len(files_to_analyze)} files to analyze')
        
        all_issues = []
        
        for idx, (file_path, language) in enumerate(files_to_analyze):
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Skip files that are too large
                if len(content) > settings.MAX_FILE_SIZE:
                    logger.warning(f"Skipping {file_path}: too large")
                    continue
                
                # Get relative path
                rel_path = os.path.relpath(file_path, clone_path)
                
                # Analyze with Gemini
                issues = gemini_agent.analyze_file(rel_path, content, language)
                
                # Save issues to database
                for issue_data in issues:
                    issue = Issue(
                        audit_id=audit.id,
                        file_path=issue_data.get('file_path', rel_path),
                        line_number=issue_data.get('line_number'),
                        issue_type=IssueType(issue_data.get('issue_type', 'code_smell')),
                        severity=IssueSeverity(issue_data.get('severity', 'medium')),
                        description=issue_data.get('description', ''),
                        original_code=issue_data.get('original_code'),
                        fixed_code=issue_data.get('fixed_code'),
                        explanation=issue_data.get('explanation', ''),
                        is_fixed=1 if issue_data.get('fixed_code') else 0
                    )
                    db.add(issue)
                    all_issues.append(issue)
                
                audit.processed_files = idx + 1
                audit.issues_found = len(all_issues)
                db.commit()
                
                if (idx + 1) % 5 == 0 or (idx + 1) == len(files_to_analyze):
                    append_log(audit, db, 'INFO', f'⚙️  Processed {idx + 1}/{len(files_to_analyze)} files ({len(all_issues)} issues found)')
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
                continue
        
        # Step 3: Apply fixes
        if all_issues:
            append_log(audit, db, 'INFO', f'🔧 Step 3: Applying fixes for {len(all_issues)} issues...')
            audit.status = AuditStatus.FIXING
            db.commit()
            
            fixes_applied = apply_fixes(clone_path, all_issues)
            audit.fixes_applied = fixes_applied
            db.commit()
            append_log(audit, db, 'SUCCESS', f'✅ Applied {fixes_applied} fixes')
        
        # Step 4: Create Pull Request
        if audit.fixes_applied > 0:
            append_log(audit, db, 'INFO', f'📤 Step 4: Creating Pull Request...')
            audit.status = AuditStatus.CREATING_PR
            db.commit()
            
            pr_url, pr_number = create_pull_request(
                clone_path,
                repository,
                audit,
                all_issues
            )
            
            if pr_url:
                audit.pr_url = pr_url
                audit.pr_number = pr_number
                append_log(audit, db, 'SUCCESS', f'🎉 Pull Request created: #{pr_number}')
        
        # Mark as completed
        audit.status = AuditStatus.COMPLETED
        audit.completed_at = datetime.utcnow()
        append_log(audit, db, 'SUCCESS', f'✨ Audit completed successfully! Found {audit.issues_found} issues, applied {audit.fixes_applied} fixes')
        db.commit()
        
        logger.info(f"Audit completed successfully for {repository.owner}/{repository.name}")
        
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        append_log(audit, db, 'ERROR', f'❌ Audit failed: {str(e)}')
        audit.status = AuditStatus.FAILED
        audit.error_message = str(e)
        audit.completed_at = datetime.utcnow()
        db.commit()
    
    finally:
        # Cleanup: Remove cloned repository
        if clone_path and os.path.exists(clone_path):
            try:
                shutil.rmtree(clone_path)
                logger.info(f"Cleaned up clone directory: {clone_path}")
            except Exception as e:
                logger.error(f"Failed to cleanup {clone_path}: {e}")


def clone_repository(url: str, branch: str) -> str:
    """
    Clone a repository to local storage with automatic branch fallback.
    
    If the specified branch doesn't exist, tries common alternatives:
    - If 'main' fails, tries 'master'
    - If 'master' fails, tries 'main'
    
    Args:
        url: Repository URL
        branch: Branch to clone
        
    Returns:
        Path to cloned repository
    """
    clone_dir = settings.CLONE_DIR
    os.makedirs(clone_dir, exist_ok=True)
    
    # Generate unique directory name
    repo_name = url.split('/')[-1].replace('.git', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    clone_path = os.path.join(clone_dir, f"{repo_name}_{timestamp}")
    
    logger.info(f"Cloning {url} to {clone_path}")
    
    # Try to clone with specified branch
    try:
        git.Repo.clone_from(url, clone_path, branch=branch, depth=1)
        logger.info(f"Successfully cloned branch '{branch}'")
        return clone_path
    except git.GitCommandError as e:
        # Check if error is due to branch not found
        if "Remote branch" in str(e) and "not found" in str(e):
            logger.warning(f"Branch '{branch}' not found, trying fallback branches...")
            
            # Determine fallback branch
            fallback_branches = []
            if branch == 'main':
                fallback_branches = ['master', 'develop', 'dev']
            elif branch == 'master':
                fallback_branches = ['main', 'develop', 'dev']
            else:
                fallback_branches = ['main', 'master']
            
            # Try each fallback branch
            for fallback in fallback_branches:
                try:
                    logger.info(f"Attempting to clone with branch '{fallback}'...")
                    git.Repo.clone_from(url, clone_path, branch=fallback, depth=1)
                    logger.info(f"✅ Successfully cloned using fallback branch '{fallback}'")
                    return clone_path
                except git.GitCommandError:
                    logger.warning(f"Branch '{fallback}' also not found")
                    continue
            
            # If all fallbacks failed, raise the original error
            logger.error(f"All branch attempts failed for {url}")
            raise
        else:
            # Some other git error, re-raise it
            raise


def discover_files(repo_path: str) -> list:
    """
    Discover files to analyze using RAG (Intelligent Context Retrieval).
    
    Skips:
    - node_modules, .git, etc.
    - Binary files
    - Files larger than MAX_FILE_SIZE
    
    Args:
        repo_path: Path to repository
        
    Returns:
        List of (file_path, language) tuples
    """
    files = []
    
    for root, dirs, filenames in os.walk(repo_path):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_PATTERNS]
        
        for filename in filenames:
            file_path = os.path.join(root, filename)
            ext = Path(filename).suffix.lower()
            
            if ext in SUPPORTED_EXTENSIONS:
                language = SUPPORTED_EXTENSIONS[ext]
                files.append((file_path, language))
    
    # Limit files per repository
    if len(files) > settings.MAX_FILES_PER_REPO:
        logger.warning(f"Repository has {len(files)} files, limiting to {settings.MAX_FILES_PER_REPO}")
        files = files[:settings.MAX_FILES_PER_REPO]
    
    return files


def apply_fixes(repo_path: str, issues: list) -> int:
    """
    Apply fixes to files.
    
    Args:
        repo_path: Path to repository
        issues: List of Issue objects
        
    Returns:
        Number of fixes applied
    """
    fixes_applied = 0
    
    for issue in issues:
        if not issue.fixed_code or not issue.is_fixed:
            continue
        
        try:
            file_path = os.path.join(repo_path, issue.file_path)
            
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                continue
            
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace original with fixed code
            if issue.original_code and issue.original_code in content:
                content = content.replace(issue.original_code, issue.fixed_code)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixes_applied += 1
                logger.info(f"Applied fix to {issue.file_path}")
            
        except Exception as e:
            logger.error(f"Failed to apply fix to {issue.file_path}: {e}")
    
    return fixes_applied


def create_pull_request(repo_path: str, repository: Repository, audit: Audit, issues: list) -> tuple:
    """
    Create a Pull Request with the fixes.
    
    Safety Valve: Never commits to main, always creates a branch.
    
    Args:
        repo_path: Path to repository
        repository: Repository model
        audit: Audit model
        issues: List of Issue objects
        
    Returns:
        Tuple of (PR URL, PR number)
    """
    try:
        repo = git.Repo(repo_path)
        
        # Create new branch
        branch_name = f"fix/ai-auto-patch-{audit.id}"
        repo.git.checkout('-b', branch_name)
        
        # Stage all changes
        repo.git.add('--all')
        
        # Create commit
        commit_message = f"""🤖 AutoDev Agent: Fix {len(issues)} issues

This PR was automatically generated by AutoDev Agent.

Issues fixed:
"""
        
        for issue in issues[:10]:  # Limit to first 10 in commit message
            commit_message += f"- {issue.issue_type.value}: {issue.description}\n"
        
        if len(issues) > 10:
            commit_message += f"- ... and {len(issues) - 10} more\n"
        
        repo.index.commit(commit_message)
        
        # Push to origin
        origin = repo.remote('origin')
        origin.push(branch_name)
        
        # Create PR via GitHub API
        pr_title = f"🤖 AutoDev Agent: Fix {len(issues)} issues"
        pr_body = f"""## AutoDev Agent - Automated Code Fixes

This Pull Request was automatically generated by [AutoDev Agent](https://github.com/your-org/autodev-agent).

### Summary
- **Total Issues Found**: {audit.issues_found}
- **Fixes Applied**: {audit.fixes_applied}

### Issues Fixed

"""
        
        for issue in issues:
            pr_body += f"""
#### {issue.issue_type.value.replace('_', ' ').title()} - {issue.severity.value.upper()}
**File**: `{issue.file_path}`
**Description**: {issue.description}

{f'**Line**: {issue.line_number}' if issue.line_number else ''}

---
"""
        
        pr_body += """

### ⚠️ Important
Please review these changes carefully before merging. While the AI has done its best to provide accurate fixes, human review is essential.

### How to Test
1. Checkout this branch
2. Run your test suite
3. Verify the changes manually
4. Merge if everything looks good

---
*Generated by AutoDev Agent powered by Google Gemini 1.5 Pro*
"""
        
        # Create PR
        pr_url, pr_number = github_service.create_pull_request(
            repo_full_name=f"{repository.owner}/{repository.name}",
            branch_name=branch_name,
            title=pr_title,
            body=pr_body,
            base_branch=repository.branch
        )
        
        return pr_url, pr_number
        
    except Exception as e:
        logger.error(f"Failed to create PR: {e}")
        return None, None
