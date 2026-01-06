from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, UniqueConstraint

from backend.app.db.base import Base


class LeadNotification(Base):
    __tablename__ = "lead_notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    lead_id = Column(UUID, ForeignKey("leads.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("lead_id", "user_id", name="uq_lead_user_notification"),)
