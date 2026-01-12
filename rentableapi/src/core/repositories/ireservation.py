"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable

from pydantic import UUID4

from src.core.domain.reservation import Reservation, ReservationIn


class IReservationRepository(ABC):
    """The abstract class representing protocol of reservation repository."""

    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Reservation]:
        """The abstract method getting all reservations from the data storage.

        Returns:
            Iterable[Reservation]: The collection of the all reservations in the data storage.
        """

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The abstract method getting reservation by provided id from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Reservation | None: The reservation details.
        """

    @abstractmethod
    async def get_all_reservations_by_equipment_id(
        self, equipment_id: int
    ) -> Iterable[Reservation]:
        """The abstract method getting all reservations by provided equipment id from the data storage.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Iterable[Reservation]: The collection of the all reservations from provided equipment in the data storage.
        """

    @abstractmethod
    async def get_all_reservations_by_user(
        self, user_id: UUID4
    ) -> Iterable[Reservation]:
        """The abstract method getting all reservations by provided user id from the data storage.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[Reservation]: The collection of the all reservations from privided user in the data storage.
        """

    @abstractmethod
    async def get_all_reservations_by_category_id(
        self, category_id: int
    ) -> Iterable[Reservation]:
        """The abstract method getting all reservations by provided category id from the data storage.

        Args:
            category_id (int): The id of the user.

        Returns:
            Iterable[Reservation]: The collection of the all reservations from provided category in the data storage.
        """

    @abstractmethod
    async def get_all_reservations_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Reservation]:
        """The abstract method getting all reservations by provided subcategory id from the data storage.

        Args:
            subcategory_id (int): The id of the user.

        Returns:
            Iterable[Reservation]: The collection of the all reservations from provided subcategory in the data storage.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The abstract method adding new reservation to the data storage.

        Args:
            data (ReservationIn): The details of the new reservation.

        Returns:
            Reservation | None: The newly created reservation.
        """

    @abstractmethod
    async def update_reservation(
        self, reservation_id: int, data: ReservationIn
    ) -> Reservation | None:
        """The abstract method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationIn): The details of the updated reservation.

        Returns:
            Reservation | None: The updated reservation details.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract method remmoving reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_most_rented_equipment_ids(self, limit: int) -> Iterable[dict]:
        """The abstract method getting most rented equipment IDs from the data storage.

        Args:
            limit (int): The number of items to return.

        Returns:
            Iterable[dict]: The collection of the all equipment IDs.
        """

    @abstractmethod
    async def calculate_total_price(
        self, equipment_id: int, start_date: date, end_date: date
    ) -> float:
        """The abstract method calculating total price of the reservation.

        Args:
            equipment_id (int): The id of the equipment.
            start_date (date): The start date of the reservation.
            end_date (date): The end date of the reservation.

        Returns:
            float: The total price of the reservation.
        """
