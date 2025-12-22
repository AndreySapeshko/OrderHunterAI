from sqlalchemy import UUID, Column, ForeignKey

from backend.app.db.base import Base


class LeadSourceLink(Base):
    __tablename__ = "lead_source_links"

    lead_id = Column(UUID, ForeignKey("leads.id"), primary_key=True)
    raw_item_id = Column(UUID, ForeignKey("raw_items.id"), primary_key=True)
