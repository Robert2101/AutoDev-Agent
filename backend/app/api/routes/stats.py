"""
API routes for statistics and dashboard data.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models import Audit, Issue, AuditStatus
from app.schemas import StatisticsResponse

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get overall statistics for the dashboard.
    """
    total_audits = db.query(func.count(Audit.id)).scalar()
    
    completed_audits = db.query(func.count(Audit.id)).filter(
        Audit.status == AuditStatus.COMPLETED
    ).scalar()
    
    failed_audits = db.query(func.count(Audit.id)).filter(
        Audit.status == AuditStatus.FAILED
    ).scalar()
    
    pending_audits = db.query(func.count(Audit.id)).filter(
        Audit.status.in_([
            AuditStatus.PENDING,
            AuditStatus.CLONING,
            AuditStatus.ANALYZING,
            AuditStatus.FIXING,
            AuditStatus.VALIDATING,
            AuditStatus.CREATING_PR,
        ])
    ).scalar()
    
    total_issues_found = db.query(func.sum(Audit.issues_found)).scalar() or 0
    total_fixes_applied = db.query(func.sum(Audit.fixes_applied)).scalar() or 0
    
    total_prs_created = db.query(func.count(Audit.id)).filter(
        Audit.pr_url.isnot(None)
    ).scalar()
    
    return StatisticsResponse(
        total_audits=total_audits or 0,
        completed_audits=completed_audits or 0,
        failed_audits=failed_audits or 0,
        pending_audits=pending_audits or 0,
        total_issues_found=total_issues_found,
        total_fixes_applied=total_fixes_applied,
        total_prs_created=total_prs_created or 0,
    )
