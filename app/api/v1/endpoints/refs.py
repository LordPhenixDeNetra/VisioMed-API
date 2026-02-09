from typing import Annotated, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.schemas.acte_type import ActeTypeCreate, ActeTypeUpdate, ActeTypeResponse
from app.schemas.type_prise_charge import TypePriseChargeCreate, TypePriseChargeUpdate, TypePriseChargeResponse
from app.schemas.tarif import TarifCreate, TarifUpdate, TarifResponse
from app.services.role import role_service
from app.services.service import service_service
from app.services.acte_type import acte_type_service
from app.services.type_prise_charge import type_prise_charge_service
from app.services.tarif import tarif_service
from app.db.models.user import User

router = APIRouter()

# --- Roles ---
@router.get("/roles", response_model=List[RoleResponse], summary="Lister les rôles", description="Récupère la liste de tous les rôles fonctionnels disponibles.")
async def read_roles(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne la liste des rôles (ex: Admin, Médecin, Secrétaire) définis dans le système.
    """
    return await role_service.get_multi(db, skip=skip, limit=limit)

@router.post("/roles", response_model=RoleResponse, summary="Créer un rôle", description="Ajoute un nouveau rôle fonctionnel.")
async def create_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_in: RoleCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Permet de créer un nouveau rôle avec ses permissions associées.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    return await role_service.create(db, obj_in=role_in)

@router.patch("/roles/{role_id}", response_model=RoleResponse, summary="Mettre à jour un rôle", description="Modifie un rôle existant.")
async def update_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour le nom, la description ou les permissions d'un rôle.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    role = await role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await role_service.update(db, db_obj=role, obj_in=role_in)

@router.delete("/roles/{role_id}", response_model=RoleResponse, summary="Supprimer un rôle", description="Supprime un rôle fonctionnel.")
async def delete_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un rôle du système. Attention si des utilisateurs possèdent encore ce rôle.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    role = await role_service.remove(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# --- Services ---
@router.get("/services", response_model=List[ServiceResponse], summary="Lister les services", description="Récupère la liste des services médicaux.")
async def read_services(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne la liste des services (ex: Cardiologie, Pédiatrie).
    """
    return await service_service.get_multi(db, skip=skip, limit=limit)

@router.post("/services", response_model=ServiceResponse, summary="Créer un service", description="Ajoute un nouveau service médical.")
async def create_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_in: ServiceCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Crée un nouveau service hospitalier.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    return await service_service.create(db, obj_in=service_in)

@router.patch("/services/{service_id}", response_model=ServiceResponse, summary="Mettre à jour un service", description="Modifie les informations d'un service.")
async def update_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_id: int,
    service_in: ServiceUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour le nom, la description ou le chef de service.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    service = await service_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return await service_service.update(db, db_obj=service, obj_in=service_in)

@router.delete("/services/{service_id}", response_model=ServiceResponse, summary="Supprimer un service", description="Supprime un service médical.")
async def delete_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un service.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    service = await service_service.remove(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

# --- Acte Types ---
@router.get("/actes-types", response_model=List[ActeTypeResponse], summary="Lister les types d'actes", description="Récupère la liste des types d'actes médicaux.")
async def read_actes_types(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne la liste des types d'actes (ex: Consultation, Chirurgie, Analyse).
    """
    return await acte_type_service.get_multi(db, skip=skip, limit=limit)

@router.post("/actes-types", response_model=ActeTypeResponse, summary="Créer un type d'acte", description="Définit un nouveau type d'acte médical.")
async def create_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_in: ActeTypeCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Crée une nouvelle catégorie d'acte médical.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    return await acte_type_service.create(db, obj_in=acte_type_in)

@router.patch("/actes-types/{acte_type_id}", response_model=ActeTypeResponse, summary="Mettre à jour un type d'acte", description="Modifie un type d'acte existant.")
async def update_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_id: int,
    acte_type_in: ActeTypeUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour le nom ou la description d'un type d'acte.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    acte_type = await acte_type_service.get(db, id=acte_type_id)
    if not acte_type:
        raise HTTPException(status_code=404, detail="Acte Type not found")
    return await acte_type_service.update(db, db_obj=acte_type, obj_in=acte_type_in)

@router.delete("/actes-types/{acte_type_id}", response_model=ActeTypeResponse, summary="Supprimer un type d'acte", description="Supprime un type d'acte médical.")
async def delete_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un type d'acte.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    acte_type = await acte_type_service.remove(db, id=acte_type_id)
    if not acte_type:
        raise HTTPException(status_code=404, detail="Acte Type not found")
    return acte_type


# --- Types de Prise en Charge ---
@router.get("/types-prise-charge", response_model=List[TypePriseChargeResponse], summary="Lister les types de prise en charge", description="Récupère la liste des types de couverture (ex: Assurance, Espèces).")
async def read_types_prise_charge(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne la liste des types de prise en charge disponibles avec leur taux de couverture.
    """
    return await type_prise_charge_service.get_multi(db, skip=skip, limit=limit)


@router.post("/types-prise-charge", response_model=TypePriseChargeResponse, summary="Créer un type de prise en charge", description="Ajoute un nouveau type de couverture.")
async def create_type_prise_charge(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tpc_in: TypePriseChargeCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Crée un nouveau type de prise en charge (ex: IPM, Assurance privée).
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    return await type_prise_charge_service.create(db, obj_in=tpc_in)


@router.patch("/types-prise-charge/{tpc_id}", response_model=TypePriseChargeResponse, summary="Mettre à jour un type de prise en charge", description="Modifie un type de couverture existant.")
async def update_type_prise_charge(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tpc_id: int,
    tpc_in: TypePriseChargeUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour le nom, le taux de couverture ou le statut actif/inactif.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    tpc = await type_prise_charge_service.get(db, id=tpc_id)
    if not tpc:
        raise HTTPException(status_code=404, detail="Type de prise en charge non trouvé")
    return await type_prise_charge_service.update(db, db_obj=tpc, obj_in=tpc_in)


@router.delete("/types-prise-charge/{tpc_id}", response_model=TypePriseChargeResponse, summary="Supprimer un type de prise en charge", description="Supprime un type de couverture.")
async def delete_type_prise_charge(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tpc_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un type de prise en charge.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    tpc = await type_prise_charge_service.remove(db, id=tpc_id)
    if not tpc:
        raise HTTPException(status_code=404, detail="Type de prise en charge non trouvé")
    return tpc

# --- Tarifs ---
@router.get("/tarifs", response_model=List[TarifResponse], summary="Lister les tarifs", description="Récupère la liste des tarifs (prix).")
async def read_tarifs(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne la liste complète des tarifs configurés.
    """
    return await tarif_service.get_multi(db, skip=skip, limit=limit)

@router.get("/tarifs/search", response_model=Optional[TarifResponse], summary="Rechercher un tarif", description="Récupère le tarif applicable pour une combinaison donnée.")
async def search_tarif(
    service_id: int,
    acte_id: int,
    type_prise_charge_id: int,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Permet de trouver le tarif en vigueur pour un acte spécifique, dans un service donné, avec un type de prise en charge particulier.
    
    Retourne le tarif applicable (montant, validité) si trouvé.
    """
    return await tarif_service.get_active_tarif(
        db, 
        service_id=service_id, 
        acte_id=acte_id, 
        type_prise_charge_id=type_prise_charge_id
    )

@router.post("/tarifs", response_model=TarifResponse, summary="Créer un tarif", description="Définit un nouveau prix pour une combinaison Service/Acte/Prise en charge.")
async def create_tarif(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tarif_in: TarifCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Crée une nouvelle règle tarifaire.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    return await tarif_service.create(db, obj_in=tarif_in)

@router.patch("/tarifs/{tarif_id}", response_model=TarifResponse, summary="Mettre à jour un tarif", description="Modifie un tarif existant.")
async def update_tarif(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tarif_id: int,
    tarif_in: TarifUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour le montant ou les dates de validité d'un tarif.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    tarif = await tarif_service.get(db, id=tarif_id)
    if not tarif:
        raise HTTPException(status_code=404, detail="Tarif non trouvé")
    return await tarif_service.update(db, db_obj=tarif, obj_in=tarif_in)

@router.delete("/tarifs/{tarif_id}", response_model=TarifResponse, summary="Supprimer un tarif", description="Supprime une règle tarifaire.")
async def delete_tarif(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    tarif_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un tarif de la base de données.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    tarif = await tarif_service.remove(db, id=tarif_id)
    if not tarif:
        raise HTTPException(status_code=404, detail="Tarif non trouvé")
    return tarif
