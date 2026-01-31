"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from app.models import AuditStatus, IssueSeverity, IssueType


# =============================================================================
# Repository Schemas
# =============================================================================

class RepositoryCreate(BaseModel):
    """Schema for creating a repository audit request."""
    url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(default="main", description="Branch to analyze")


class RepositoryResponse(BaseModel):
    """Schema for repository response."""
    id: int
    url: str
    owner: str
    name: str
    branch: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# Issue Schemas
# =============================================================================

class IssueResponse(BaseModel):
    """Schema for issue response."""
    id: int
    file_path: str
    line_number: Optional[int]
    issue_type: IssueType
    severity: IssueSeverity
    description: str
    original_code: Optional[str]
    fixed_code: Optional[str]
    explanation: Optional[str]
    is_fixed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# Audit Schemas
# =============================================================================

class AuditResponse(BaseModel):
    """Schema for audit response."""
    id: int
    repository_id: int
    status: AuditStatus
    task_id: Optional[str] = None  # Can be None initially
    total_files: int
    processed_files: int
    issues_found: int
    fixes_applied: int
    pr_url: Optional[str]
    pr_number: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AuditDetailResponse(AuditResponse):
    """Schema for detailed audit response with issues."""
    repository: RepositoryResponse
    issues: List[IssueResponse] = []
    
    class Config:
        from_attributes = True


class AuditCreateResponse(BaseModel):
    """Schema for audit creation response."""
    audit_id: int
    task_id: Optional[str] = None
    status: AuditStatus
    message: str


# =============================================================================
# Status Schemas
# =============================================================================

class StatusResponse(BaseModel):
    """Schema for real-time status updates."""
    audit_id: int
    status: AuditStatus
    progress: float = Field(..., ge=0.0, le=100.0)
    current_step: str
    message: str
    timestamp: datetime


# =============================================================================
# Statistics Schemas
# =============================================================================

class StatisticsResponse(BaseModel):
    """Schema for dashboard statistics."""
    total_audits: int
    completed_audits: int
    failed_audits: int
    pending_audits: int
    total_issues_found: int
    total_fixes_applied: int
    total_prs_created: int
