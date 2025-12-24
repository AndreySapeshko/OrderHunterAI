import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, String, Text, func

from backend.app.db.base import Base


class RawItem(Base):
    __tablename__ = "raw_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(String, index=True)
    external_id = Column(String, nullable=True)
    url = Column(Text, nullable=True)
    title = Column(Text)
    content = Column(Text)
    author = Column(String, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)

    content_hash = Column(String, index=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
