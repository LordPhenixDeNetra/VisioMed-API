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

@router.get(
    "/",
    response_model=List[ActeMedicalResponse],
    summary="Lister les actes médicaux",
    description="Récupère une liste paginée des actes médicaux. Permet de filtrer par nom de patient."
)
async def read_actes(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    nom_patient: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère les actes médicaux.

    - **skip**: Nombre d'enregistrements à sauter (pagination).
    - **limit**: Nombre maximum d'enregistrements à retourner.
    - **nom_patient**: Filtre optionnel pour rechercher par nom de patient.
    
    Retourne la liste des actes médicaux trouvés.
    """
    if nom_patient:
        return await acte_medical_service.get_by_patient(db, nom=nom_patient, prenom="")
    return await acte_medical_service.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=ActeMedicalResponse,
    summary="Créer un acte médical",
    description="Crée un nouvel acte médical avec les informations fournies (type, patient, médecin, etc.)."
)
async def create_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_in: ActeMedicalCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Crée un nouvel acte médical.

    - **acte_in**: Les données de création de l'acte médical.
    
    Retourne l'acte médical créé.
    """
    return await acte_medical_service.create(db, obj_in=acte_in)


@router.get(
    "/{acte_id}",
    response_model=ActeMedicalResponse,
    summary="Récupérer un acte médical",
    description="Récupère les détails d'un acte médical spécifique par son ID."
)
async def read_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère un acte médical par son ID.

    - **acte_id**: L'identifiant unique de l'acte médical.
    
    Retourne l'acte médical si trouvé, sinon lève une erreur 404.
    """
    acte = await acte_medical_service.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte médical non trouvé")
    return acte


@router.put(
    "/{acte_id}",
    response_model=ActeMedicalResponse,
    summary="Mettre à jour un acte médical",
    description="Met à jour les informations d'un acte médical existant."
)
async def update_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_id: int,
    acte_in: ActeMedicalUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Met à jour un acte médical.

    - **acte_id**: L'identifiant unique de l'acte médical à modifier.
    - **acte_in**: Les données à mettre à jour.
    
    Retourne l'acte médical mis à jour.
    """
    acte = await acte_medical_service.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte médical non trouvé")
    return await acte_medical_service.update(db, db_obj=acte, obj_in=acte_in)


@router.delete(
    "/{acte_id}",
    response_model=ActeMedicalResponse,
    summary="Supprimer un acte médical",
    description="Supprime un acte médical spécifique de la base de données."
)
async def delete_acte(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Supprime un acte médical.

    - **acte_id**: L'identifiant unique de l'acte médical à supprimer.
    
    Retourne l'acte médical supprimé.
    """
    acte = await acte_medical_service.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte médical non trouvé")
    return await acte_medical_service.remove(db, id=acte_id)

@router.get(
    "/tarif-actif",
    response_model=Optional[TarifResponse],
    summary="Obtenir le tarif actif",
    description="Récupère le tarif actif applicable pour un service, un acte et un type de prise en charge donnés, utile pour les simulations de prix."
)
async def get_active_tarif(
    service_id: int,
    acte_id: int,
    type_prise_charge_id: int,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère le tarif actif pour une simulation de prix.

    - **service_id**: ID du service.
    - **acte_id**: ID de l'acte médical.
    - **type_prise_charge_id**: ID du type de prise en charge.
    
    Retourne le tarif applicable si trouvé.
    """
    return await tarif_service.get_active_tarif(
        db, 
        service_id=service_id, 
        acte_id=acte_id, 
        type_prise_charge_id=type_prise_charge_id
    )
