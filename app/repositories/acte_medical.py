from typing import List, Any, Optional, Union
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.acte_medical import ActeMedical
from app.schemas.acte_medical import ActeMedicalCreate, ActeMedicalUpdate
from app.repositories.base import BaseRepository

class ActeMedicalRepository(BaseRepository[ActeMedical, ActeMedicalCreate, ActeMedicalUpdate]):
    
    def _get_load_options(self):
        """Options de chargement eager pour les relations"""
        return [
            selectinload(ActeMedical.acte_type),
            selectinload(ActeMedical.type_prise_charge)
        ]

    async def get(self, db: AsyncSession, id: Any) -> Optional[ActeMedical]:
        query = select(ActeMedical).options(*self._get_load_options()).where(ActeMedical.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ActeMedical]:
        query = select(ActeMedical).options(*self._get_load_options()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def create(self, db: AsyncSession, *, obj_in: ActeMedicalCreate) -> ActeMedical:
        # Création standard
        db_obj = await super().create(db, obj_in=obj_in)
        # Rechargement avec les relations pour éviter DetachedInstanceError lors de la réponse API
        return await self.get(db, db_obj.id)

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ActeMedical,
        obj_in: Union[ActeMedicalUpdate, dict[str, Any]]
    ) -> ActeMedical:
        # Mise à jour standard
        db_obj = await super().update(db, db_obj=db_obj, obj_in=obj_in)
        # Rechargement avec les relations
        return await self.get(db, db_obj.id)

    async def get_by_patient(self, db: AsyncSession, *, nom: str, prenom: str) -> List[ActeMedical]:
        query = select(ActeMedical).options(*self._get_load_options()).where(
            ActeMedical.nom_patient.ilike(f"%{nom}%"),
            ActeMedical.prenom_patient.ilike(f"%{prenom}%")
        )
        result = await db.execute(query)
        return list(result.scalars().all())
        
    async def get_by_medecin(self, db: AsyncSession, *, medecin_id: int) -> List[ActeMedical]:
        query = select(ActeMedical).options(*self._get_load_options()).where(ActeMedical.medecin_id == medecin_id)
        result = await db.execute(query)
        return list(result.scalars().all())

acte_medical = ActeMedicalRepository(ActeMedical)
