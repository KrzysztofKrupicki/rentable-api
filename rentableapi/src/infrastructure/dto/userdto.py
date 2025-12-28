"""A module containing user DTO model."""

from typing import Optional

from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict


class UserDTO(BaseModel):
    """A DTO model for user."""

    id: UUID4
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_domain(cls, record: Record) -> "UserDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            UserDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            email=record_dict.get("email"),  # type: ignore
        )
