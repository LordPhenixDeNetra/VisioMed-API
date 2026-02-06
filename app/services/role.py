from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Role, Permission
from app.schemas.role import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate
from app.repositories.role import RoleRepository, PermissionRepository
from app.services.base import BaseService
from app.repositories import role as role_repo, permission as permission_repo

class RoleService(BaseService[Role, RoleCreate, RoleUpdate, RoleRepository]):
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Role]:
        return await self.repository.get_by_name(db, name=name)

class PermissionService(BaseService[Permission, PermissionCreate, PermissionUpdate, PermissionRepository]):
    pass

role_service = RoleService(role_repo)
permission_service = PermissionService(permission_repo)
