from sqlalchemy import Column, String, DateTime, Integer, Text
from datetime import datetime, timezone
from app.core.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(String, primary_key=True, index=True)
    started_at = Column(DateTime, default=_utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # success, error, running
    source = Column(String, nullable=True)  # ValueGaia, ChavesNaMao, etc
    properties_count = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
