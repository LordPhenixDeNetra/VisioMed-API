from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class ServiceBase(BaseModel):
    nom: str
    description: Optional[str] = None
    est_actif: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    est_actif: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
