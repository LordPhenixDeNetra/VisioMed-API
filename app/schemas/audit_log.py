from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
