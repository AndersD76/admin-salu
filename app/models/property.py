from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Property(Base):
    __tablename__ = "properties"

    id = Column(String, primary_key=True, index=True)
    external_code = Column(String, unique=True, nullable=False, index=True)
    client_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
    registration_date = Column(DateTime, nullable=True)
    last_update_date = Column(DateTime, nullable=True)

    # Localizacao
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True, index=True)
    neighborhood = Column(String, nullable=True, index=True)
    address = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    condominium_name = Column(String, nullable=True)

    # Tipo e finalidade
    property_type = Column(String, nullable=False, index=True)
    purpose = Column(String, nullable=False, index=True)

    # Caracteristicas
    usable_area = Column(Float, nullable=True)
    total_area = Column(Float, nullable=True)
    bedrooms = Column(Integer, default=0, nullable=False)
    suites = Column(Integer, default=0, nullable=False)
    bathrooms = Column(Integer, default=0, nullable=False)
    parking_spaces = Column(Integer, default=0, nullable=False)

    # Valores
    sale_price = Column(Float, nullable=True, index=True)
    rental_price = Column(Float, nullable=True, index=True)
    iptu_price = Column(Float, nullable=True)
    condominium_price = Column(Float, nullable=True)
    price_per_sqm = Column(Float, nullable=True)

    # Descricao
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    # Features
    has_bbq = Column(Boolean, default=False, nullable=False)
    has_pool = Column(Boolean, default=False, nullable=False)
    has_sauna = Column(Boolean, default=False, nullable=False)
    has_service_area = Column(Boolean, default=False, nullable=False)
    has_balcony = Column(Boolean, default=False, nullable=False)
    has_elevator = Column(Boolean, default=False, nullable=False)
    has_security = Column(Boolean, default=False, nullable=False)
    has_gym = Column(Boolean, default=False, nullable=False)
    has_party_room = Column(Boolean, default=False, nullable=False)
    has_garden = Column(Boolean, default=False, nullable=False)

    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)

    # Estatisticas
    view_count = Column(Integer, default=0, nullable=False)
    contact_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)

    # URLs
    site_url = Column(String, nullable=True)

    # Fonte do XML (ValueGaia, ChavesNaMao, etc)
    xml_source = Column(String, nullable=True, index=True)

    # Foreign Keys
    broker_id = Column(String, ForeignKey("brokers.id"), nullable=True, index=True)

    # Relationships
    photos = relationship("Photo", back_populates="property", cascade="all, delete-orphan")
    broker = relationship("Broker", back_populates="properties")
    favorites = relationship("Favorite", back_populates="property", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="property", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(String, primary_key=True, index=True)
    property_id = Column(String, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False, index=True)
    type = Column(String, nullable=True)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=_utcnow, nullable=False)

    # Relationships
    property = relationship("Property", back_populates="photos")
