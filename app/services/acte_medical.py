from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.acte_medical import ActeMedical
from app.schemas.acte_medical import ActeMedicalCreate, ActeMedicalUpdate
from app.repositories.acte_medical import ActeMedicalRepository
from app.services.base import BaseService
from app.repositories import acte_medical as acte_medical_repo

class ActeMedicalService(BaseService[ActeMedical, ActeMedicalCreate, ActeMedicalUpdate, ActeMedicalRepository]):
    
    async def get_by_patient(self, db: AsyncSession, *, nom: str, prenom: str) -> List[ActeMedical]:
        return await self.repository.get_by_patient(db, nom=nom, prenom=prenom)
        
    async def get_by_medecin(self, db: AsyncSession, *, medecin_id: int) -> List[ActeMedical]:
        return await self.repository.get_by_medecin(db, medecin_id=medecin_id)

acte_medical_service = ActeMedicalService(acte_medical_repo)
