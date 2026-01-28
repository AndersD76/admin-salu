from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    property_id = Column(String, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    property = relationship("Property", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint("user_id", "property_id", name="unique_user_property_favorite"),
    )
