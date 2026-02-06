from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

# Permission Schemas
class PermissionBase(BaseModel):
    resource: str
    action: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    resource: Optional[str] = None
    action: Optional[str] = None
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Role Schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permissions: Optional[List[int]] = [] # List of permission IDs

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[int]] = None

class RoleResponse(RoleBase):
    id: int
    uuid: uuid_pkg.UUID
    permissions: List[PermissionResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
