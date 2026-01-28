from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Broker(Base):
    __tablename__ = "brokers"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=True)
    external_code = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    photo = Column(String, nullable=True)
    creci = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    # Localizacao para distribuicao de leads
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, nullable=True, index=True)
    neighborhood = Column(String, nullable=True)

    # Controle de rodizio de leads
    is_active = Column(Boolean, default=True, nullable=False)
    last_lead_assigned_at = Column(DateTime, nullable=True)
    lead_count = Column(Integer, default=0, nullable=False)

    # Redes sociais
    facebook = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)

    # Estatisticas
    total_sales = Column(Integer, default=0, nullable=False)
    total_rentals = Column(Integer, default=0, nullable=False)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="broker_profile")
    properties = relationship("Property", back_populates="broker")
    contacts = relationship("Contact", back_populates="broker")
