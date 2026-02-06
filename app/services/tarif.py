from typing import Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tarif import Tarif
from app.schemas.tarif import TarifCreate, TarifUpdate
from app.repositories.tarif import TarifRepository
from app.services.base import BaseService
from app.repositories import tarif as tarif_repo

class TarifService(BaseService[Tarif, TarifCreate, TarifUpdate, TarifRepository]):
    
    async def get_active_tarif(
        self, 
        db: AsyncSession, 
        *, 
        service_id: int, 
        acte_id: int, 
        type_prise_charge_id: int,
        date_ref: date = date.today()
    ) -> Optional[Tarif]:
        """
        Get the active tariff for a specific combination.
        """
        return await self.repository.get_active_tarif(
            db, 
            service_id=service_id, 
            acte_id=acte_id, 
            type_prise_charge_id=type_prise_charge_id,
            date_ref=date_ref
        )

tarif_service = TarifService(tarif_repo)
