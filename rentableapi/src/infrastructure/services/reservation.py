"""Module containing reservation service implementation."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.reservation import Reservation, ReservationIn
from src.core.repositories.ireservation import IReservationRepository
from src.infrastructure.services.ireservation import IReservationService

class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _repository: IReservationRepository

    def __init__(self, repository: IReservationRepository) -> None:
        """The initializer of the reservation service.
        
        Args:
            repository (IReservationRepository): The reference to the repository.
        """
        self._repository = repository
    
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting a reservation from the repository.
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns: 
            Reservation | None: The reservation data if exists.
        """
        return await self._repository.get_reservation_by_id(reservation_id)

    async def get_all_reservations(self) -> Iterable[Reservation]:
        """The method getting all reservations from the repository.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        return await self._repository.get_all_reservations()

    async def get_all_reservations_by_user(self, user_id: UUID4) -> Iterable[Reservation] | None:
        """The method getting all reservations by user from the repository.
        
        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[Reservation] | None: The collection of the reservations if exists.
        """
        return await self._repository.get_all_reservations_by_user(user_id)

    async def get_all_reservations_by_equipment_id(self, equipment_id: int) -> Iterable[Reservation] | None:
        """The method getting all reservations by equipment id from the repository.
        
        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Iterable[Reservation] | None: The collection of the reservations if exists.
        """
        return await self._repository.get_all_reservations_by_equipment_id(equipment_id)

    async def get_all_reservation_by_category_id(self, category_id: int) -> Iterable[Reservation] | None:
        """The method getting all reservations by category id from the repository.
        
        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Reservation] | None: The collection of the reservations if exists.
        """
        return await self._repository.get_all_reservations_by_category_id(category_id)

    async def get_all_reservation_by_subcategory_id(self, subcategory_id: int) -> Iterable[Reservation] | None:
        """The method getting all reservations by subcategory id from the repository.
        
        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Reservation] | None: The collection of the reservations if exists.
        """
        return await self._repository.get_all_reservations_by_subcategory_id(subcategory_id)

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The method adding new reservation to the repository.
        
        Args:
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Reservation | None: The newly created reservation.
        """
        return await self._repository.add_reservation(data)

    async def update_reservation(self, reservation_id: int, data: ReservationIn) -> Reservation | None:
        """The method updating reservation data in the repository.
        
        Args:
            reservation_id (int): The reservation id.
            data (ReservationIn): The attributes of the reservation.
        
        Returns:
            Reservation | None: The updated reservation.
        """
        return await self._repository.update_reservation(reservation_id=reservation_id, data=data)
    
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method deleting reservation from the repository.
        
        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_reservation(reservation_id)

    async def get_most_rented_equipment_ids(self, limit: int) -> Iterable[dict]:
        """The method getting most rented equipment IDs from the repository.
        
        Args:
            limit (int): The limit of the most rented equipment IDs.

        Returns:
            Iterable[dict]: The collection of the most rented equipment IDs.
        """
        return await self._repository.get_most_rented_equipment_ids(limit)