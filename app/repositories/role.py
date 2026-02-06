from typing import Any, List, Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Role, Permission
from app.schemas.role import RoleCreate, RoleUpdate
from app.repositories.base import BaseRepository

class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    
    async def create(self, db: AsyncSession, *, obj_in: RoleCreate) -> Role:
        # Extract permissions IDs
        permissions_ids = obj_in.permissions
        
        # Create Role object without permissions first
        db_obj = Role(name=obj_in.name, description=obj_in.description)
        
        if permissions_ids:
            # Fetch permissions
            result = await db.execute(select(Permission).where(Permission.id.in_(permissions_ids)))
            permissions = result.scalars().all()
            db_obj.permissions = list(permissions)
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Role,
        obj_in: Union[RoleUpdate, dict[str, Any]]
    ) -> Role:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        # Handle permissions update if present
        if "permissions" in update_data:
            permissions_ids = update_data.pop("permissions")
            if permissions_ids is not None:
                result = await db.execute(select(Permission).where(Permission.id.in_(permissions_ids)))
                permissions = result.scalars().all()
                db_obj.permissions = list(permissions)
        
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

role = RoleRepository(Role)
