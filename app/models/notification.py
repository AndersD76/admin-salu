"""
Notification model - Sistema de notificacoes do app
"""
from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
import uuid
from app.core.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class NotificationType(enum.Enum):
    # Imoveis
    NEW_PROPERTY = "NEW_PROPERTY"
    PRICE_DROP = "PRICE_DROP"
    PROPERTY_REMOVED = "PROPERTY_REMOVED"

    # Propostas
    PROPOSAL_RECEIVED = "PROPOSAL_RECEIVED"
    PROPOSAL_APPROVED = "PROPOSAL_APPROVED"
    PROPOSAL_REJECTED = "PROPOSAL_REJECTED"
    PROPOSAL_ASSIGNED = "PROPOSAL_ASSIGNED"
    PROPOSAL_UPDATE = "PROPOSAL_UPDATE"
    PROPOSAL_ACCEPTED = "PROPOSAL_ACCEPTED"

    # Documentos
    DOCUMENT_REQUESTED = "DOCUMENT_REQUESTED"
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    DOCUMENT_APPROVED = "DOCUMENT_APPROVED"
    DOCUMENT_REJECTED = "DOCUMENT_REJECTED"

    # Contatos e visitas
    CONTACT_REPLY = "CONTACT_REPLY"
    VISIT_SCHEDULED = "VISIT_SCHEDULED"
    VISIT_CONFIRMED = "VISIT_CONFIRMED"
    VISIT_CANCELLED = "VISIT_CANCELLED"
    VISIT_REMINDER = "VISIT_REMINDER"

    # Sistema
    SYSTEM = "SYSTEM"
    PROMOTION = "PROMOTION"
    WELCOME = "WELCOME"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    link = Column(String, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=_utcnow, nullable=False)

    # Contexto adicional (IDs relacionados)
    proposal_id = Column(String, nullable=True)
    document_id = Column(String, nullable=True)
    property_id = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")
