from app.db.models.role import Permission
from app.schemas.role import PermissionCreate, PermissionUpdate
from app.repositories.base import BaseRepository

class PermissionRepository(BaseRepository[Permission, PermissionCreate, PermissionUpdate]):
    pass

permission = PermissionRepository(Permission)
