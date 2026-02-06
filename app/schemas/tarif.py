from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg

class TarifBase(BaseModel):
    service_id: int
    acte_id: int
    type_prise_charge_id: int
    montant: float
    date_debut: date = date.today()
    date_fin: Optional[date] = None

class TarifCreate(TarifBase):
    pass

class TarifUpdate(BaseModel):
    service_id: Optional[int] = None
    acte_id: Optional[int] = None
    type_prise_charge_id: Optional[int] = None
    montant: Optional[float] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None

class TarifResponse(TarifBase):
    id: int
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
