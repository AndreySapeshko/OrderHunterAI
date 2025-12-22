from datetime import datetime

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from backend.app.db.base import Base


class LeadAI(Base):
    __tablename__ = "lead_ai"

    lead_id = Column(UUID, ForeignKey("leads.id"), primary_key=True)

    is_relevant = Column(Boolean, index=True)
    relevance_reason = Column(String)
    category = Column(String, index=True)

    extracted = Column(JSONB)
    score = Column(Integer, index=True)

    model = Column(String)
    prompt_version = Column(String)

    analyzed_at = Column(DateTime, default=datetime.utcnow)
