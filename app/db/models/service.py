from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.db.models.user import Medecin

# Association table for Medecin <-> Service (Many-to-Many)
# Doctors can work in multiple services
medecin_services = Table(
    "medecin_services",
    Base.metadata,
    Column("medecin_id", Integer, ForeignKey("medecins.id", ondelete="CASCADE"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
)


class Service(Base, TimestampMixin, UUIDMixin):
    """
    Medical Service / Department (e.g., Cardiologie, Endoscopie).
    """
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    
    # Head of department (Chef de service) - Optional
    chef_service_id: Mapped[Optional[int]] = mapped_column(ForeignKey("medecins.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    # Note: 'Medecin' is imported as string to avoid circular imports, but we need to ensure it resolves at runtime
    medecins: Mapped[List["Medecin"]] = relationship(
        "Medecin",
        secondary=medecin_services,
        backref="services" # Adds .services to Medecin model
    )
    
    chef_service: Mapped[Optional["Medecin"]] = relationship(
        "Medecin",
        foreign_keys=[chef_service_id],
        backref="services_managed" # Adds .services_managed to Medecin model
    )

    def __repr__(self):
        return f"<Service {self.code} - {self.nom}>"
