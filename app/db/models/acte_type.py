from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.db.models.service import Service

class ActeType(Base, TimestampMixin, UUIDMixin):
    """
    Type of medical act (e.g., "Consultation Généraliste", "Echographie Abdominale").
    Linked to a specific Service.
    """
    __tablename__ = "actes_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Code unique par service (ex: CS-GEN)")
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    # Foreign Keys
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    service: Mapped["Service"] = relationship("Service", backref="actes_types")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('code', 'service_id', name='uq_acte_type_code_service'),
    )

    def __repr__(self):
        return f"<ActeType {self.code} - {self.nom}>"
