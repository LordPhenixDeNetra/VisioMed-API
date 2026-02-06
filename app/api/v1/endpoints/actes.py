from typing import Annotated, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
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
    return await acte_medical_service.create(db, obj_in=acte_in)

@router.patch("/{acte_id}", response_model=ActeMedicalResponse)
async def update_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_id: int,
    acte_in: ActeMedicalUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a medical act.
    """
    acte = await acte_medical_service.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte Medical not found")
    
    # Check permissions if needed (e.g. only creator or admin can update)
    # For now, allow logged in users (or refine to medecin/admin)
    
    return await acte_medical_service.update(db, db_obj=acte, obj_in=acte_in)

@router.delete("/{acte_id}", response_model=ActeMedicalResponse)
async def delete_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    acte = await acte_medical_service.remove(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte Medical not found")
    return acte

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
