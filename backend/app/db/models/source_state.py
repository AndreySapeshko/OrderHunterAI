from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.app.db.base import Base


class SourceStateModel(Base):
    __tablename__ = "source_state"

    source_id = Column(String, primary_key=True)
    cursor = Column(String, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)
    last_success_at = Column(DateTime, nullable=True)
    error_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
