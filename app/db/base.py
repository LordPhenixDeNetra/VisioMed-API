from datetime import datetime
from typing import Any
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Includes naming convention for constraints to avoid migration issues.
    """
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    # Automatically generate table name from class name (e.g., UserProfile -> user_profile)
    # But for this project we might want to be explicit, so we can keep it optional
    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return cls.__name__.lower()

    def dict(self) -> dict[str, Any]:
        """Dictionary representation of the model"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    """
    Mixin to add created_at and updated_at columns to a model.
    """
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
        comment="Date de création"
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Date de dernière modification"
    )
