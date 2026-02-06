from .base import BaseRepository
from .user import user
from .role import role, permission
from .service import service
from .acte_type import acte_type
from .type_prise_charge import type_prise_charge
from .tarif import tarif
from .acte_medical import acte_medical
from .audit_log import audit_log

__all__ = [
    "BaseRepository",
    "user",
    "role",
    "permission",
    "service",
    "acte_type",
    "type_prise_charge",
    "tarif",
    "acte_medical",
    "audit_log",
]
