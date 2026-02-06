from app.db.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.repositories.service import ServiceRepository
from app.services.base import BaseService
from app.repositories import service as service_repo

class MedicalServiceService(BaseService[Service, ServiceCreate, ServiceUpdate, ServiceRepository]):
    pass

service_service = MedicalServiceService(service_repo)
