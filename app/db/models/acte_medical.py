from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.db.models.acte_type import ActeType
    from app.db.models.type_prise_charge import TypePriseCharge
    from app.db.models.user import Medecin, User

class ActeMedical(Base, TimestampMixin, UUIDMixin):
    """
    Medical Act Record.
    The central entity representing a performed medical service on a patient.
    """
    __tablename__ = "actes_medicaux"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Patient Info
    nom_patient: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    prenom_patient: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    numero_bc: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True, comment="Numéro Bon de Commande / Prise en charge")
    
    # Act Details
    date_acte: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    cotation: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="Cotation de l'acte (ex: K20)")
    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Financial Snapshot (Stored at creation time to preserve history even if tariffs change)
    montant: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    statut: Mapped[str] = mapped_column(String(20), default="NON_PAYE", index=True, comment="Statut paiement: NON_PAYE, PAYE, GRATUIT")
    
    # Foreign Keys
    acte_id: Mapped[int] = mapped_column(ForeignKey("actes_types.id", ondelete="RESTRICT"), nullable=False, index=True)
    type_prise_charge_id: Mapped[int] = mapped_column(ForeignKey("types_prise_charge.id", ondelete="RESTRICT"), nullable=False)
    medecin_id: Mapped[int] = mapped_column(ForeignKey("medecins.id", ondelete="RESTRICT"), nullable=False, index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    acte_type: Mapped["ActeType"] = relationship("ActeType")
    type_prise_charge: Mapped["TypePriseCharge"] = relationship("TypePriseCharge")
    medecin: Mapped["Medecin"] = relationship("Medecin", foreign_keys=[medecin_id])
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<ActeMedical {self.nom_patient} {self.prenom_patient} - {self.date_acte}>"
