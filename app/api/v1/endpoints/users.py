from typing import Annotated, List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import user_service
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[UserResponse], summary="Lister les utilisateurs", description="Récupère la liste paginée de tous les utilisateurs enregistrés.")
async def read_users(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Retourne une liste d'utilisateurs avec pagination.
    
    **Permissions :**
    - Réservé aux administrateurs.
    
    **Paramètres :**
    - `skip` : Nombre d'éléments à sauter (pagination).
    - `limit` : Nombre maximum d'éléments à retourner.
    """
    return await user_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, summary="Créer un utilisateur", description="Crée un nouvel utilisateur dans le système.")
async def create_user(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Permet de créer un nouvel utilisateur (médecin, secrétaire, etc.).
    
    **Permissions :**
    - Réservé aux administrateurs.
    
    **Corps de la requête :**
    - Champs obligatoires : email, password, nom, prenom, type.
    - Champs optionnels selon le type : matricule (médecin), desk_number (secrétaire), etc.
    """
    user = await user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = await user_service.create(db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=UserResponse, summary="Obtenir un utilisateur par ID", description="Récupère les détails d'un utilisateur spécifique.")
async def read_user_by_id(
    user_id: int,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    **Description détaillée :**
    Retourne les informations d'un utilisateur donné par son ID.
    
    **Permissions :**
    - L'utilisateur peut consulter son propre profil.
    - Les administrateurs peuvent consulter n'importe quel profil.
    """
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Simple permission check: user can read own profile or admin can read any
    if user.id != current_user.id and current_user.type != "administrateur":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

@router.patch("/{user_id}", response_model=UserResponse, summary="Mettre à jour un utilisateur", description="Met à jour les informations d'un utilisateur existant.")
async def update_user(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Met à jour partiellement les champs d'un utilisateur.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = await user_service.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=UserResponse, summary="Supprimer un utilisateur", description="Supprime définitivement un utilisateur du système.")
async def delete_user(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    user_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    **Description détaillée :**
    Supprime un utilisateur par son ID.
    
    **Permissions :**
    - Réservé aux administrateurs.
    """
    user = await user_service.remove(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
