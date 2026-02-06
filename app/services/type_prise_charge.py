from app.db.models.type_prise_charge import TypePriseCharge
from app.schemas.type_prise_charge import TypePriseChargeCreate, TypePriseChargeUpdate
from app.repositories.type_prise_charge import TypePriseChargeRepository
from app.services.base import BaseService
from app.repositories import type_prise_charge as tpc_repo

class TypePriseChargeService(BaseService[TypePriseCharge, TypePriseChargeCreate, TypePriseChargeUpdate, TypePriseChargeRepository]):
    pass

type_prise_charge_service = TypePriseChargeService(tpc_repo)
