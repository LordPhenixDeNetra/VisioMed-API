from app.db.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.repositories.base import BaseRepository

class ServiceRepository(BaseRepository[Service, ServiceCreate, ServiceUpdate]):
    pass

service = ServiceRepository(Service)
