from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey

from backend.app.db.base import Base


class LeadNotification(Base):
    __tablename__ = "lead_notifications"

    lead_id = Column(UUID, ForeignKey("leads.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    sent_at = Column(DateTime, default=datetime.utcnow)
