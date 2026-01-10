"""Module representing user review-related domain models."""

from pydantic import ConfigDict, UUID4
from pydantic import BaseModel, Field
from typing import Optional


class UserReviewIn(BaseModel):
    """Model representing user review DTO attributes."""

    rating: int = Field(ge=0, le=10)
    comment: Optional[str]
    reviewed_user_id: UUID4


class UserReviewBroker(UserReviewIn):
    """Model representing user review broker."""

    reviewer_id: UUID4


class UserReview(UserReviewBroker):
    """Model representing user review attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
