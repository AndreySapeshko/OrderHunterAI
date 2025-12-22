import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, String, Text

from backend.app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    description = Column(Text)

    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
