import uuid
from datetime import datetime

from sqlalchemy import ARRAY, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String

from backend.app.db.base import Base


class UserRule(Base):
    __tablename__ = "user_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), index=True, nullable=False)

    source_id = Column(ARRAY(String), nullable=True, default=list)

    min_score = Column(Integer, default=0)
    min_text_length = Column(Integer, default=0)

    include_keywords = Column(ARRAY(String), nullable=True, default=list)
    exclude_keywords = Column(ARRAY(String), nullable=True, default=list)

    min_score_for_notis = Column(Integer, default=0)
    keyword_for_notis = Column(ARRAY(String), nullable=True, default=list)

    enabled = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
