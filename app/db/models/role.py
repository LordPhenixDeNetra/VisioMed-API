from typing import List
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

# Association table for User <-> Role (Many-to-Many)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

# Association table for Role <-> Permission (Many-to-Many)
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class Permission(Base, TimestampMixin, UUIDMixin):
    """
    Fine-grained permission (e.g., 'user:create', 'report:view').
    """
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="Identifiant unique (ex: user.create)")
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"<Permission {self.slug}>"


class Role(Base, TimestampMixin, UUIDMixin):
    """
    Functional Role (e.g., 'SuperAdmin', 'BillingManager').
    A user can have multiple functional roles in addition to their Identity (User Type).
    """
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    permissions: Mapped[List["Permission"]] = relationship(secondary=role_permissions, lazy="selectin")

    def __repr__(self):
        return f"<Role {self.name}>"
