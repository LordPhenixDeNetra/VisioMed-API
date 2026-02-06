from app.db.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate
from app.repositories.base import BaseRepository

# AuditLog usually doesn't need Update schema as logs are immutable
class AuditLogRepository(BaseRepository[AuditLog, AuditLogCreate, AuditLogCreate]):
    pass

audit_log = AuditLogRepository(AuditLog)
