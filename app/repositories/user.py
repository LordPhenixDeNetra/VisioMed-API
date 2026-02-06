from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.base import BaseRepository, CreateSchemaType, UpdateSchemaType


class UserRepository(BaseRepository[User, CreateSchemaType, UpdateSchemaType]):
    """
    User specific repository operations.
    """
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
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
