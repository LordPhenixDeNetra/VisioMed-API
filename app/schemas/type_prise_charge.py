from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg
from datetime import datetime

class TypePriseChargeBase(BaseModel):
    nom: str
    taux_couverture: float # Pourcentage, ex: 80.0 pour 80%
    description: Optional[str] = None
    est_actif: bool = True

class TypePriseChargeCreate(TypePriseChargeBase):
    pass

class TypePriseChargeUpdate(BaseModel):
    nom: Optional[str] = None
    taux_couverture: Optional[float] = None
    description: Optional[str] = None
    est_actif: Optional[bool] = None

class TypePriseChargeResponse(TypePriseChargeBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
