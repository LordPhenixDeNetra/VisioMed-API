from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg

# Import nested schemas for response
# We use forward references or strings to avoid circular imports if needed, 
# but usually schema imports are fine if structure is clean.
from app.schemas.acte_type import ActeTypeResponse
from app.schemas.type_prise_charge import TypePriseChargeResponse
# We might need a minimal User/Medecin schema to avoid circular dep with UserResponse if it includes too much
# For now, let's assume we can import a base or use the main one if no cycle.
# To be safe, we can define minimal inner classes or use the ones from user.py if no cycle.
# Actually user.py imports Role, not ActeMedical, so we are safe to import UserResponse here?
# UserResponse imports RoleResponse. 
# ActeMedicalResponse imports UserResponse (for medecin).
# No cycle yet.

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
    
    # Nested objects for "linked information"
    acte_type: Optional[ActeTypeResponse] = None
    type_prise_charge: Optional[TypePriseChargeResponse] = None
    # We use 'object' or forward ref for User/Medecin to avoid circular imports if User imports this
    # But User doesn't import ActeMedical. So we can import UserResponse.
    # However, to keep it lightweight, maybe just name/id? 
    # Let's try to import UserResponse, but inside the file to allow Pydantic to resolve.
    
    # Using generic dict or specific schema if available. 
    # Let's rely on ORM loading these relations.
    # Note: The ORM model must have these relationships defined.
    
    model_config = ConfigDict(from_attributes=True)
