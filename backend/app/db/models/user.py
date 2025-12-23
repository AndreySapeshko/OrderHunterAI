import uuid

from sqlalchemy import UUID, BigInteger, Boolean, Column, String

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(BigInteger, unique=True, index=True, nullable=True)
    username = Column(String, nullable=True)
    is_active = Column(Boolean, index=True, default=True)
    password = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
