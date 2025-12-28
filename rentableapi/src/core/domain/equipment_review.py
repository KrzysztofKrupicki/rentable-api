"""Module representing equipment review-related domain models."""

from pydantic import ConfigDict, UUID4

from src.core.domain.review import ReviewIn


class EquipmentReviewIn(ReviewIn):
    """Model representing equipment review DTO attributes."""

    equipment_id: int


class EquipmentReview(EquipmentReviewIn):
    """Model representing equipment review attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
