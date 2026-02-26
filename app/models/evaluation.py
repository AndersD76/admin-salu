from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean, Text
from datetime import datetime
from app.core.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, index=True)

    # Dados do imovel avaliado
    city = Column(String, nullable=False, index=True)
    neighborhood = Column(String, nullable=True)
    property_type = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    usable_area = Column(Float, nullable=False)
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Integer, default=0)
    parking_spaces = Column(Integer, default=0)

    # Diferenciais
    has_pool = Column(Boolean, default=False)
    has_gym = Column(Boolean, default=False)
    has_elevator = Column(Boolean, default=False)
    has_security = Column(Boolean, default=False)

    # Resultado da avaliacao
    estimated_price = Column(Float, nullable=True)
    price_per_sqm = Column(Float, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    confidence = Column(String, nullable=True)
    similar_count = Column(Integer, default=0)
    data_sources = Column(Text, nullable=True)

    # Analytics
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
