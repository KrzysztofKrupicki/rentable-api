"""A module containing DTO model for token details."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TokenDTO(BaseModel):
    """A model representing DTO for token details."""
    token_type: str
    user_token: str
    expires: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )