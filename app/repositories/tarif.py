from typing import Optional
from datetime import date
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tarif import Tarif
from app.schemas.tarif import TarifCreate, TarifUpdate
from app.repositories.base import BaseRepository

class TarifRepository(BaseRepository[Tarif, TarifCreate, TarifUpdate]):
    
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
        Get the active tariff for a specific combination on a given date.
        """
        query = select(Tarif).where(
            and_(
                Tarif.service_id == service_id,
                Tarif.acte_id == acte_id,
                Tarif.type_prise_charge_id == type_prise_charge_id,
                Tarif.date_debut <= date_ref,
                or_(
                    Tarif.date_fin.is_(None),
                    Tarif.date_fin >= date_ref
                )
            )
        ).order_by(Tarif.date_debut.desc())
        
        result = await db.execute(query)
        return result.scalars().first()

tarif = TarifRepository(Tarif)
