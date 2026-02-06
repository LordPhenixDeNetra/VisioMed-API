from typing import Annotated, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.acte_medical import ActeMedicalCreate, ActeMedicalUpdate, ActeMedicalResponse
from app.schemas.tarif import TarifResponse
from app.services.acte_medical import acte_medical_service
from app.services.tarif import tarif_service
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ActeMedicalResponse])
async def read_actes(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    nom_patient: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve medical acts. Can filter by patient name.
    """
    if nom_patient:
        # Note: simplistic search, assumes nom_patient is full or partial name
        return await acte_medical_service.get_by_patient(db, nom=nom_patient, prenom="") 
    return await acte_medical_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=ActeMedicalResponse)
async def create_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_in: ActeMedicalCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new medical act.
    """
    # Auto-assign created_by_id if we had it in schema, but for now schema doesn't force it
    # We could update schema or handle it in service if needed.
    # For now standard create.
    return await acte_medical_service.create(db, obj_in=acte_in)

@router.get("/tarif-actif", response_model=Optional[TarifResponse])
async def get_active_tarif(
    service_id: int,
    acte_id: int,
    type_prise_charge_id: int,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get active tariff for pricing simulation.
    """
    return await tarif_service.get_active_tarif(
        db, 
        service_id=service_id, 
        acte_id=acte_id, 
        type_prise_charge_id=type_prise_charge_id
    )
