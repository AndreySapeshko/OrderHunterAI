import uuid

from datetime import datetime
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    llm_analyzed = Column(Boolean, default=False, nullable=False)

    raw_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("raw_items.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    raw_item = relationship(
        "RawItem",
        back_populates="lead",
        lazy="joined",
    )
