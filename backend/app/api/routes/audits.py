"""
API routes for repository audits.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import re

from app.core.database import get_db
from app.models import Repository, Audit, AuditStatus
from app.schemas import (
    RepositoryCreate,
    AuditCreateResponse,
    AuditResponse,
    AuditDetailResponse,
)
from worker.tasks.audit_task import process_repository_audit

router = APIRouter(prefix="/api/audits", tags=["audits"])


def parse_github_url(url: str) -> tuple:
    """Parse GitHub URL to extract owner and repo name."""
    patterns = [
        r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$",
        r"github\.com/([^/]+)/([^/]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            owner, name = match.groups()
            # Remove .git suffix if present
            name = name.replace(".git", "")
            return owner, name
    
    raise ValueError("Invalid GitHub URL format")


@router.post("/", response_model=AuditCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_audit(
    repo_data: RepositoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new repository audit job.
    
    This endpoint:
    1. Validates the GitHub URL
    2. Creates or retrieves the repository record
    3. Creates an audit job
    4. Queues the job for processing
    """
    try:
        # Parse GitHub URL
        owner, name = parse_github_url(repo_data.url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Check if repository exists
    repository = db.query(Repository).filter(Repository.url == repo_data.url).first()
    
    if not repository:
        # Create new repository
        repository = Repository(
            url=repo_data.url,
            owner=owner,
            name=name,
            branch=repo_data.branch
        )
        db.add(repository)
        db.commit()
        db.refresh(repository)
    
    # Create audit job
    audit = Audit(
        repository_id=repository.id,
        status=AuditStatus.PENDING
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    
    # Queue the audit task
    task = process_repository_audit.delay(audit.id)
    
    # Update audit with task ID
    audit.task_id = task.id
    db.commit()
    
    return AuditCreateResponse(
        audit_id=audit.id,
        task_id=task.id,
        status=audit.status,
        message=f"Audit job created for {owner}/{name}. Processing started."
    )


@router.get("/", response_model=List[AuditResponse])
async def list_audits(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List all audit jobs with pagination.
    """
    audits = db.query(Audit).order_by(Audit.created_at.desc()).offset(skip).limit(limit).all()
    return audits


@router.get("/{audit_id}", response_model=AuditDetailResponse)
async def get_audit(
    audit_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific audit job.
    """
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    
    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit with ID {audit_id} not found"
        )
    
    return audit


@router.delete("/{audit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audit(
    audit_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an audit job and all associated issues.
    """
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    
    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit with ID {audit_id} not found"
        )
    
    db.delete(audit)
    db.commit()
    
    return None
