"""A module containing DTO models for reservation."""

from datetime import date

from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict

from src.infrastructure.dto.equipmentdto import EquipmentDTO


class ReservationDTO(BaseModel):
    """A model representing DTO for reservation data."""

    id: int
    equipment: EquipmentDTO
    user_id: UUID4
    start_date: date
    end_date: date
    status: str
    total_price: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_domain(cls, record: Record) -> "ReservationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            Reservation: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            equipment_id=EquipmentDTO.from_domain(record.equipment_id),
            user_id=record_dict.get("user_id"),  # type: ignore
            start_date=record_dict.get("start_date"),  # type: ignore
            end_date=record_dict.get("end_date"),  # type: ignore
            status=record_dict.get("status"),  # type: ignore
            total_price=record_dict.get("total_price"),  # type: ignore
        )
