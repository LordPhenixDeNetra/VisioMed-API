from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg

class ActeMedicalBase(BaseModel):
    nom_patient: str
    prenom_patient: str
    numero_bc: Optional[str] = None
    date_acte: datetime = datetime.now()
    cotation: Optional[str] = None
    observations: Optional[str] = None
    montant: float
    statut: str = "NON_PAYE"
    
    acte_id: int
    type_prise_charge_id: int
    medecin_id: int

class ActeMedicalCreate(ActeMedicalBase):
    pass

class ActeMedicalUpdate(BaseModel):
    nom_patient: Optional[str] = None
    prenom_patient: Optional[str] = None
    numero_bc: Optional[str] = None
    date_acte: Optional[datetime] = None
    cotation: Optional[str] = None
    observations: Optional[str] = None
    montant: Optional[float] = None
    statut: Optional[str] = None
    
    acte_id: Optional[int] = None
    type_prise_charge_id: Optional[int] = None
    medecin_id: Optional[int] = None

class ActeMedicalResponse(ActeMedicalBase):
    id: int
    uuid: uuid_pkg.UUID
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
