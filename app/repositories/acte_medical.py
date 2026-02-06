from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.acte_medical import ActeMedical
from app.schemas.acte_medical import ActeMedicalCreate, ActeMedicalUpdate
from app.repositories.base import BaseRepository

class ActeMedicalRepository(BaseRepository[ActeMedical, ActeMedicalCreate, ActeMedicalUpdate]):
    
    async def get_by_patient(self, db: AsyncSession, *, nom: str, prenom: str) -> List[ActeMedical]:
        query = select(ActeMedical).where(
            ActeMedical.nom_patient.ilike(f"%{nom}%"),
            ActeMedical.prenom_patient.ilike(f"%{prenom}%")
        )
        result = await db.execute(query)
        return list(result.scalars().all())
        
    async def get_by_medecin(self, db: AsyncSession, *, medecin_id: int) -> List[ActeMedical]:
        query = select(ActeMedical).where(ActeMedical.medecin_id == medecin_id)
        result = await db.execute(query)
        return list(result.scalars().all())

acte_medical = ActeMedicalRepository(ActeMedical)
