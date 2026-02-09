from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class ActeTypeBase(BaseModel):
    code: str
    nom: str
    description: Optional[str] = None
    is_active: bool = True
    service_id: int

class ActeTypeCreate(ActeTypeBase):
    pass

class ActeTypeUpdate(BaseModel):
    code: Optional[str] = None
    nom: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    service_id: Optional[int] = None

class ActeTypeResponse(ActeTypeBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
