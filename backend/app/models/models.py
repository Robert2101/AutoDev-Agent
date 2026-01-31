"""
Database models for the AutoDev Agent.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class AuditStatus(str, enum.Enum):
    """Enumeration for audit job statuses."""
    PENDING = "pending"
    CLONING = "cloning"
    ANALYZING = "analyzing"
    FIXING = "fixing"
    VALIDATING = "validating"
    CREATING_PR = "creating_pr"
    COMPLETED = "completed"
    FAILED = "failed"


class IssueSeverity(str, enum.Enum):
    """Enumeration for issue severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueType(str, enum.Enum):
    """Enumeration for issue types."""
    SYNTAX_ERROR = "syntax_error"
    LOGIC_ERROR = "logic_error"
    SECURITY_VULNERABILITY = "security_vulnerability"
    CODE_SMELL = "code_smell"
    PERFORMANCE_ISSUE = "performance_issue"
    SECRET_EXPOSURE = "secret_exposure"


class Repository(Base):
    """Model for GitHub repositories being audited."""
    
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    owner = Column(String, nullable=False)
    name = Column(String, nullable=False)
    branch = Column(String, default="main")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    audits = relationship("Audit", back_populates="repository", cascade="all, delete-orphan")


class Audit(Base):
    """Model for audit jobs."""
    
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    status = Column(Enum(AuditStatus), default=AuditStatus.PENDING, index=True)
    task_id = Column(String, unique=True, index=True)  # Celery task ID
    
    # Metadata
    total_files = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    issues_found = Column(Integer, default=0)
    fixes_applied = Column(Integer, default=0)
    
    # Results
    pr_url = Column(String, nullable=True)
    pr_number = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    logs = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    repository = relationship("Repository", back_populates="audits")
    issues = relationship("Issue", back_populates="audit", cascade="all, delete-orphan")


class Issue(Base):
    """Model for detected issues."""
    
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False)
    
    # Issue details
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)
    issue_type = Column(Enum(IssueType), nullable=False)
    severity = Column(Enum(IssueSeverity), nullable=False)
    
    # Content
    description = Column(Text, nullable=False)
    original_code = Column(Text, nullable=True)
    fixed_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    
    # Status
    is_fixed = Column(Integer, default=0)  # Boolean as integer
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    audit = relationship("Audit", back_populates="issues")
