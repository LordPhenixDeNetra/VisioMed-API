from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate
from app.repositories.audit_log import AuditLogRepository
from app.services.base import BaseService
from app.repositories import audit_log as audit_log_repo

class AuditLogService(BaseService[AuditLog, AuditLogCreate, AuditLogCreate, AuditLogRepository]):
    
    async def log_action(
        self,
        db: AsyncSession,
        *,
        action: str,
        resource_type: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        resource_id: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Helper to create an audit log entry easily.
        """
        log_in = AuditLogCreate(
            action=action,
            resource_type=resource_type,
            user_id=user_id,
            ip_address=ip_address,
            resource_id=resource_id,
            changes=changes
        )
        return await self.create(db, obj_in=log_in)

audit_log_service = AuditLogService(audit_log_repo)
