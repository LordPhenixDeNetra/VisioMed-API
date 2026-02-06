from app.db.models.type_prise_charge import TypePriseCharge
from app.schemas.type_prise_charge import TypePriseChargeCreate, TypePriseChargeUpdate
from app.repositories.base import BaseRepository

class TypePriseChargeRepository(BaseRepository[TypePriseCharge, TypePriseChargeCreate, TypePriseChargeUpdate]):
    pass

type_prise_charge = TypePriseChargeRepository(TypePriseCharge)
