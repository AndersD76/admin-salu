from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from app.core.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class ContactType(enum.Enum):
    INFO = "INFO"
    VISIT = "VISIT"
    PROPOSAL = "PROPOSAL"
    FINANCING = "FINANCING"
    OTHER = "OTHER"


class ContactStatus(enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    SCHEDULED = "SCHEDULED"
    NEGOTIATING = "NEGOTIATING"
    CONVERTED = "CONVERTED"
    LOST = "LOST"


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    property_id = Column(String, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False, index=True)
    broker_id = Column(String, ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True, index=True)

    # Dados do contato
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    message = Column(Text, nullable=False)

    # Tipo e status
    type = Column(SQLEnum(ContactType), default=ContactType.INFO, nullable=False)
    status = Column(SQLEnum(ContactStatus), default=ContactStatus.NEW, nullable=False, index=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=_utcnow, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="contacts")
    property = relationship("Property", back_populates="contacts")
    broker = relationship("Broker", back_populates="contacts")
