"""Module containing reservation service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.reservation import Reservation, ReservationIn

class IReservationService(ABC):
    """An abstract class representing protocol of reservation service."""
    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The abstract getting a reservation from the repository.
        
        Args:
            reservation_id (int): The id of the reservation.
        
        Returns:
            Reservation | None: The reservation data if exists.
        """
    
    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Reservation]:
        """The abstract getting all reservations from the repository.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """

    @abstractmethod
    async def get_all_reservations_by_user(self, user_id: UUID4) -> Iterable[Reservation]:
        """The method getting all reservations from the repository based on its user ID.

        Args:
            user_id (UUID4): The UUID of the user.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """

    @abstractmethod
    async def get_all_reservation_by_category_id(
        self, category_id: int
    ) -> Iterable[Reservation]:
        """The method getting all reservations from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """

    @abstractmethod
    async def get_all_reservation_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Reservation]:
        """The method getting all reservations from the repository.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
    
    @abstractmethod
    async def get_all_reservations_by_equipment_id(
        self, equipment_id: int
    ) -> Iterable[Reservation]:
        """The method getting all reservations from the repository based on equipment ID.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The abstract adding new reservation to the repository.
        
        Args:
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Reservation | None: The newly created reservation.
        """

    @abstractmethod
    async def update_reservation(self, reservation_id: int, data: ReservationIn) -> Reservation | None:
        """The abstract updating reservation data in the repository.
        
        Args:
            reservation_id (int): The reservation id.
            data (ReservationIn): The attributes of the reservation.
        
        Returns:
            Reservation | None: The updated reservation.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract deleting reservation from the repository.
        
        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: The success of the operation.
        """
    
    @abstractmethod
    async def get_most_rented_equipment_ids(self, limit: int) -> Iterable[dict]:
        """The method getting most rented equipment IDs from the repository.

        Args:
            limit (int): The limit of the most rented equipment IDs.

        Returns:
            Iterable[dict]: The collection of the most rented equipment IDs with their finished reservation count.
        """