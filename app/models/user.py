from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from app.core.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class UserRole(enum.Enum):
    USER = "USER"  # Comprador/Inquilino
    OWNER = "OWNER"  # Proprietario
    BROKER = "BROKER"  # Corretor
    ADMIN = "ADMIN"  # Administrador


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    email_verified = Column(DateTime, nullable=True)
    password = Column(String, nullable=True)
    image = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    # Relationships
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    broker_profile = relationship("Broker", back_populates="user", uselist=False)
