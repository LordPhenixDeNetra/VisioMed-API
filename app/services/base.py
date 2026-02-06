from typing import Any, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.base import Base
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepositoryType]):
    def __init__(self, repository: RepositoryType):
        self.repository = repository

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        return await self.repository.get(db, id)

    async def get_by_uuid(self, db: AsyncSession, uuid: UUID) -> Optional[ModelType]:
        return await self.repository.get_by_uuid(db, uuid)

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(db, obj_in=obj_in)

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        return await self.repository.remove(db, id=id)
