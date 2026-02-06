from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin

class TypePriseCharge(Base, TimestampMixin, UUIDMixin):
    """
    Type of coverage/payment method (e.g., "IPM", "PCC", "Gratuité").
    """
    __tablename__ = "types_prise_charge"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    def __repr__(self):
        return f"<TypePriseCharge {self.code}>"
