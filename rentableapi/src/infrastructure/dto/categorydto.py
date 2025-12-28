"""A module containing DTO models for category."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class CategoryDTO(BaseModel):
    """A model representing DTO for category data."""

    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, extra="ignore", arbitrary_types_allowed=True
    )

    @classmethod
    def from_domain(cls, record: Record) -> "CategoryDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CategoryDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            description=record_dict.get("description"),  # type: ignore
        )
