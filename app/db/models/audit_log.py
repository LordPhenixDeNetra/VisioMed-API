from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.db.models.user import User

class AuditLog(Base, TimestampMixin, UUIDMixin):
    """
    Audit Log.
    Tracks all critical actions in the system for security and traceability.
    """
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Actor
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True) # IPv6 ready
    
    # Action
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # ActeMedical, User, etc.
    resource_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # ID of the affected resource
    
    # Data Changes (using JSONB in Postgres for efficiency)
    changes: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.resource_type} by {self.user_id}>"
