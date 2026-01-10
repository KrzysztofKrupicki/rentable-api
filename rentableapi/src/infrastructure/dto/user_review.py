"""A module containing DTO models for user reviews."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict, Field


class UserReviewDTO(BaseModel):
    """A model representing DTO for user reviews data."""

    id: int
    reviewed_user_id: UUID4
    reviewer_id: UUID4
    rating: int = Field(ge=0, le=10)
    comment: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_domain(cls, record: Record) -> "UserReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            UserReviewDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            reviewed_user_id=record_dict.get("reviewed_user_id"),  # type: ignore
            reviewer_id=record_dict.get("reviewer_id"),  # type: ignore
            rating=record_dict.get("rating"),  # type: ignore
            comment=record_dict.get("comment"),  # type: ignore
        )
