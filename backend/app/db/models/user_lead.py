import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from backend.app.core.enums import LeadStatus
from backend.app.db.base import Base


class UserLead(Base):
    __tablename__ = "user_leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lead_id = Column(UUID, ForeignKey("leads.id"), index=True, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), index=True, nullable=False)

    heuristic_score = Column(Integer, default=0)
    sent_to_telegram = Column(Boolean, default=False)
    status = Column(String, default=LeadStatus.NEW, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "lead_id"),)
