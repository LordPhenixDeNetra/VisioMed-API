from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user import UserRepository
from app.services.base import BaseService
from app.core.security import get_password_hash
from app.repositories import user as user_repo

class UserService(BaseService[User, UserCreate, UserUpdate, UserRepository]):
    
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        # Hash the password
        obj_in.password = get_password_hash(obj_in.password)
        return await self.repository.create(db, obj_in=obj_in)
        
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        return await self.repository.get_by_email(db, email=email)

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        return await self.repository.get_by_username(db, username=username)

user_service = UserService(user_repo)
