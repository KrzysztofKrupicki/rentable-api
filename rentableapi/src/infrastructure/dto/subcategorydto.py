"""A module containing DTO models for subcategory."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class SubcategoryDTO(BaseModel):
    """A model representing DTO for subcategory data."""

    id: int
    name: str
    description: Optional[str] = None
    category_id: int

    model_config = ConfigDict(
        from_attributes=True, extra="ignore", arbitrary_types_allowed=True
    )

    @classmethod
    def from_domain(cls, record: Record) -> "SubcategoryDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            SubcategoryDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            description=record_dict.get("description"),  # type: ignore
            category_id=record_dict.get("category_id"),  # type: ignore
        )
