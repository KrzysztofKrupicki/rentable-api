"""Module containing reservation-related domain models."""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4

class ReservationIn(BaseModel):
    """Model representing reservation's DTO attributes."""

    equipment_id: int
    start_date: date
    end_date: date
    total_price: float
    status: str = "pending"
    """
    possible statuses:
    "pending"
    "waiting_for_payment"
    "confirmed"
    "canceled"
    "finished"
    """

class ReservationBroker(ReservationIn):
    """Model representing reservation's attributes in the database."""

    user_id: UUID4

class Reservation(ReservationBroker):
    """Model representing reservation's attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
