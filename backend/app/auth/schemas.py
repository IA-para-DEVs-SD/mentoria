from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    has_profile: bool


class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    photo_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
