"""
GitHub service - Handles repository operations and PR creation.
"""
from github import Github, GithubException
from app.core.config import settings
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class GitHubService:
    """Service for interacting with GitHub API."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub API client."""
        self.github = Github(token or settings.GITHUB_TOKEN)
    
    def create_pull_request(
        self,
        repo_full_name: str,
        branch_name: str,
        title: str,
        body: str,
        base_branch: str = "main"
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Create a pull request.
        
        Args:
            repo_full_name: Full repository name (owner/repo)
            branch_name: Name of the branch with fixes
            title: PR title
            body: PR description
            base_branch: Base branch to merge into
            
        Returns:
            Tuple of (PR URL, PR number) or (None, None) on failure
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            
            pr = repo.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base=base_branch
            )
            
            logger.info(f"Created PR #{pr.number} for {repo_full_name}")
            return pr.html_url, pr.number
            
        except GithubException as e:
            logger.error(f"Failed to create PR: {e}")
            return None, None
    
    def fork_repository(self, repo_full_name: str) -> Optional[str]:
        """
        Fork a repository to the authenticated user's account.
        
        Args:
            repo_full_name: Full repository name (owner/repo)
            
        Returns:
            Forked repository full name or None on failure
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            fork = self.github.get_user().create_fork(repo)
            
            logger.info(f"Forked {repo_full_name} to {fork.full_name}")
            return fork.full_name
            
        except GithubException as e:
            logger.error(f"Failed to fork repository: {e}")
            return None


# Create global instance
github_service = GitHubService()
