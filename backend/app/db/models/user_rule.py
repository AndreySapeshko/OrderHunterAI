import uuid
from datetime import datetime

from sqlalchemy import ARRAY, UUID, Boolean, Column, DateTime, Integer, String

from backend.app.db.base import Base


class UserRule(Base):
    __tablename__ = "user_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, index=True)

    min_score = Column(Integer, default=0)
    categories = Column(ARRAY(String), nullable=True)

    include_keywords = Column(ARRAY(String), nullable=True)
    exclude_keywords = Column(ARRAY(String), nullable=True)

    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
