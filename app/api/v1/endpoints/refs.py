from typing import Annotated, List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.schemas.acte_type import ActeTypeCreate, ActeTypeUpdate, ActeTypeResponse
from app.services.role import role_service
from app.services.service import service_service
from app.services.acte_type import acte_type_service
from app.db.models.user import User

router = APIRouter()

# --- Roles ---
@router.get("/roles", response_model=List[RoleResponse])
async def read_roles(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await role_service.get_multi(db, skip=skip, limit=limit)

@router.post("/roles", response_model=RoleResponse)
async def create_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_in: RoleCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    return await role_service.create(db, obj_in=role_in)

@router.patch("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    role = await role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await role_service.update(db, db_obj=role, obj_in=role_in)

@router.delete("/roles/{role_id}", response_model=RoleResponse)
async def delete_role(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    role_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    role = await role_service.remove(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# --- Services ---
@router.get("/services", response_model=List[ServiceResponse])
async def read_services(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await service_service.get_multi(db, skip=skip, limit=limit)

@router.post("/services", response_model=ServiceResponse)
async def create_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_in: ServiceCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    return await service_service.create(db, obj_in=service_in)

@router.patch("/services/{service_id}", response_model=ServiceResponse)
async def update_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_id: int,
    service_in: ServiceUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    service = await service_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return await service_service.update(db, db_obj=service, obj_in=service_in)

@router.delete("/services/{service_id}", response_model=ServiceResponse)
async def delete_service(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    service_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    service = await service_service.remove(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

# --- Acte Types ---
@router.get("/actes-types", response_model=List[ActeTypeResponse])
async def read_actes_types(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await acte_type_service.get_multi(db, skip=skip, limit=limit)

@router.post("/actes-types", response_model=ActeTypeResponse)
async def create_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_in: ActeTypeCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    return await acte_type_service.create(db, obj_in=acte_type_in)

@router.patch("/actes-types/{acte_type_id}", response_model=ActeTypeResponse)
async def update_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_id: int,
    acte_type_in: ActeTypeUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    acte_type = await acte_type_service.get(db, id=acte_type_id)
    if not acte_type:
        raise HTTPException(status_code=404, detail="Acte Type not found")
    return await acte_type_service.update(db, db_obj=acte_type, obj_in=acte_type_in)

@router.delete("/actes-types/{acte_type_id}", response_model=ActeTypeResponse)
async def delete_acte_type(
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    acte_type_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    acte_type = await acte_type_service.remove(db, id=acte_type_id)
    if not acte_type:
        raise HTTPException(status_code=404, detail="Acte Type not found")
    return acte_type
