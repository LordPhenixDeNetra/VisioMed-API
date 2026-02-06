from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class ActeTypeBase(BaseModel):
    nom: str
    description: Optional[str] = None
    categorie: str # ex: consultation, analyse, imagerie

class ActeTypeCreate(ActeTypeBase):
    pass

class ActeTypeUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None

class ActeTypeResponse(ActeTypeBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
