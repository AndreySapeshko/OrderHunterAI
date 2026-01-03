from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AdminUserOut(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
