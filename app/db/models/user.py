from typing import Optional, List
from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

# Constants for Roles to ensure consistency
ROLE_ADMIN = "administrateur"
ROLE_MEDECIN = "medecin"
ROLE_SECRETAIRE = "secretaire"
ROLE_VISUALISEUR = "visualiseur"


class User(Base, TimestampMixin, UUIDMixin):
    """
    Base User model.
    Uses Joined Table Inheritance to handle different user roles (subclasses).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", index=True)
    
    # Discriminator column for polymorphism
    role: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": "user",
    }

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Administrateur(User):
    """
    Administrator model.
    Has full system access.
    """
    __tablename__ = "administrateurs"

    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Specific fields for Admin if needed (e.g., admin_level, specific_permissions)
    # For now, inheritance structure is prepared for future extension

    __mapper_args__ = {
        "polymorphic_identity": ROLE_ADMIN,
    }


class Medecin(User):
    """
    Doctor model.
    Can perform medical acts and belongs to services.
    """
    __tablename__ = "medecins"

    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    matricule: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, comment="Matricule professionnel")
    specialite: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Relationships
    # services: Mapped[List["Service"]] = relationship(
    #     secondary="medecin_services", back_populates="medecins"
    # )

    __mapper_args__ = {
        "polymorphic_identity": ROLE_MEDECIN,
    }


class Secretaire(User):
    """
    Secretary model.
    Manages patient intake and billing.
    """
    __tablename__ = "secretaires"

    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Example specific field
    desk_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": ROLE_SECRETAIRE,
    }


class Visualiseur(User):
    """
    Viewer model.
    Read-only access to statistics or specific reports.
    """
    __tablename__ = "visualiseurs"

    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    department_access: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Département accessible en lecture")

    __mapper_args__ = {
        "polymorphic_identity": ROLE_VISUALISEUR,
    }
