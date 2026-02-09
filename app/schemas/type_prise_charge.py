from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class TypePriseChargeBase(BaseModel):
    code: str
    libelle: str
    description: Optional[str] = None
    is_active: bool = True

class TypePriseChargeCreate(TypePriseChargeBase):
    pass

class TypePriseChargeUpdate(BaseModel):
    code: Optional[str] = None
    libelle: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class TypePriseChargeResponse(TypePriseChargeBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
