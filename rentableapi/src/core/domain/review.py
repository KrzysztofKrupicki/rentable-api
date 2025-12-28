"""Module representing review-related domain models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, UUID4


class ReviewIn(BaseModel):
    """Model representing review DTO attributes."""

    rating: int = Field(ge=0, le=10)
    comment: Optional[str]


class ReviewBroker(ReviewIn):
    """Model representing review broker attributes."""

    reviewer_id: UUID4


class Review(ReviewBroker):
    """Model representing review attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
