"""A module containing DTO models for equipment reviews."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict, Field

from src.infrastructure.dto.equipmentdto import EquipmentDTO


class EquipmentReviewDTO(BaseModel):
    """A model representing DTO for equipment reviews data."""

    id: int
    equipment: EquipmentDTO
    reviewer_id: UUID4
    rating: int = Field(ge=0, le=10)
    comment: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_domain(cls, record: Record) -> "EquipmentReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            EquipmentReviewDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            equipment=EquipmentDTO.from_domain(record.equipment_id),
            reviewer_id=record_dict.get("reviewer_id"),  # type: ignore
            rating=record_dict.get("rating"),  # type: ignore
            comment=record_dict.get("comment"),  # type: ignore
        )
