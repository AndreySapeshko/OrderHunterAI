import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, String

from backend.app.db.base import Base


class SystemState(Base):
    __tablename__ = "system_states"

    system_state_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    value = Column(String)
    limited_to = Column(DateTime, default=datetime.utcnow)
