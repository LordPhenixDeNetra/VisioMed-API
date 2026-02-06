from app.db.models.acte_type import ActeType
from app.schemas.acte_type import ActeTypeCreate, ActeTypeUpdate
from app.repositories.base import BaseRepository

class ActeTypeRepository(BaseRepository[ActeType, ActeTypeCreate, ActeTypeUpdate]):
    pass

acte_type = ActeTypeRepository(ActeType)
