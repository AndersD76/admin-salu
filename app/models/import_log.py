from sqlalchemy import Column, String, DateTime, Integer, Text
from datetime import datetime
from app.core.database import Base


class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(String, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # success, error, running
    source = Column(String, nullable=True)  # ValueGaia, ChavesNaMao, etc
    properties_count = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
