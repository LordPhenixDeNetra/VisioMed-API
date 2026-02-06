from app.db.models.acte_type import ActeType
from app.schemas.acte_type import ActeTypeCreate, ActeTypeUpdate
from app.repositories.acte_type import ActeTypeRepository
from app.services.base import BaseService
from app.repositories import acte_type as acte_type_repo

class ActeTypeService(BaseService[ActeType, ActeTypeCreate, ActeTypeUpdate, ActeTypeRepository]):
    pass

acte_type_service = ActeTypeService(acte_type_repo)
