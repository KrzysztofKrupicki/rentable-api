"""A module containing DTO models for equipment."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict

from src.infrastructure.dto.categorydto import CategoryDTO
from src.infrastructure.dto.subcategorydto import SubcategoryDTO


class EquipmentDTO(BaseModel):
    """A model representing DTO for equipment data."""

    id: int
    name: str
    description: Optional[str] = None
    category: CategoryDTO
    subcategory: SubcategoryDTO
    equipment_owner_id: UUID4
    price_per_day: float
    is_available: bool

    model_config = ConfigDict(
        from_attributes=True, extra="ignore", arbitrary_types_allowed=True
    )

    @classmethod
    def from_domain(cls, record: Record) -> "EquipmentDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            EquipmentDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            description=record_dict.get("description"),  # type: ignore
            category_id=CategoryDTO.from_domain(record.category_id),
            subcategory_id=SubcategoryDTO.from_domain(record.subcategory_id),
            equipment_owner_id=record_dict.get("equipment_owner_id"),  # type: ignore
            price_per_day=record_dict.get("price_per_day"),  # type: ignore
            is_available=record_dict.get("is_available"),  # type: ignore
        )
