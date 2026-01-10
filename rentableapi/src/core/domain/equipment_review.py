"""Module representing equipment review-related domain models."""

from pydantic import ConfigDict, UUID4
from pydantic import BaseModel, Field
from typing import Optional


class EquipmentReviewIn(BaseModel):
    """Model representing equipment review DTO attributes."""

    rating: int = Field(ge=0, le=10)
    comment: Optional[str]
    equipment_id: int


class EquipmentReviewBroker(EquipmentReviewIn):
    """Model representing equipment review broker."""

    reviewer_id: UUID4


class EquipmentReview(EquipmentReviewBroker):
    """Model representing equipment review attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
