from typing import Optional, List, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectin_polymorphic

from app.db.models.user import User, Medecin, Secretaire, Visualiseur, Administrateur
from app.repositories.base import BaseRepository, CreateSchemaType, UpdateSchemaType


class UserRepository(BaseRepository[User, CreateSchemaType, UpdateSchemaType]):
    """
    User specific repository operations.
    """

    def _get_polymorphic_options(self):
        return selectin_polymorphic(User, [Medecin, Secretaire, Visualiseur, Administrateur])

    async def get(self, db: AsyncSession, id: Any) -> Optional[User]:
        query = select(User).options(self._get_polymorphic_options()).where(User.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        query = select(User).options(self._get_polymorphic_options()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).options(self._get_polymorphic_options()).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        query = select(User).options(self._get_polymorphic_options()).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    async def authenticate(
        self, db: AsyncSession, *, identifier: str
    ) -> Optional[User]:
        """
        Find user by email OR username.
        Does not verify password here (done in Service layer).
        """
        # Try by email first
        user = await self.get_by_email(db, email=identifier)
        if user:
            return user
            
        # Try by username
        return await self.get_by_username(db, username=identifier)


user: UserRepository = UserRepository(User)
