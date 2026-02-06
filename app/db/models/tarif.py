from datetime import date
from typing import Optional
from sqlalchemy import ForeignKey, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

class Tarif(Base, TimestampMixin, UUIDMixin):
    """
    Pricing rule.
    Defines the cost of an ActeType for a specific Service and TypePriseCharge.
    Allows temporal validity (date_debut, date_fin).
    """
    __tablename__ = "tarifs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign Keys
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    acte_id: Mapped[int] = mapped_column(ForeignKey("actes_types.id", ondelete="CASCADE"), nullable=False, index=True)
    type_prise_charge_id: Mapped[int] = mapped_column(ForeignKey("types_prise_charge.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Financials
    montant: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, comment="Montant en FCFA")
    
    # Validity Period
    date_debut: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    date_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    service: Mapped["Service"] = relationship("Service")
    acte: Mapped["ActeType"] = relationship("ActeType")
    type_prise_charge: Mapped["TypePriseCharge"] = relationship("TypePriseCharge")

    # Constraints to prevent overlapping active tariffs for same combination would be complex in SQL
    # but we add a unique constraint for start date to avoid duplicates
    __table_args__ = (
        UniqueConstraint('service_id', 'acte_id', 'type_prise_charge_id', 'date_debut', name='uq_tarif_version'),
    )

    def __repr__(self):
        return f"<Tarif {self.montant} ({self.date_debut})>"
