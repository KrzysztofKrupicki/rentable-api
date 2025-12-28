"""Module containing reservation database repository implementation."""

from datetime import date
from typing import Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4
from sqlalchemy import delete, func, insert, select, update

from src.core.domain.reservation import Reservation, ReservationIn
from src.core.repositories.ireservation import IReservationRepository
from src.db import (
    category_table,
    database,
    equipment_table,
    reservation_table,
    subcategory_table,
    user_table,
)


class ReservationRepository(IReservationRepository):
    """A class implementing the reservation repository."""

    async def get_all_reservations(self) -> Iterable[Reservation]:
        """The method getting all reservations from the database.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        query = select(reservation_table)

        reservations = await database.fetch_all(query)
        return [Reservation(**dict(reservation)) for reservation in reservations]

    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The method getting reservation from the database based on its ID.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Reservation | None: The reservation if exists.
        """
        reservation = await self._get_by_id(reservation_id)
        return Reservation(**dict(reservation)) if reservation else None

    async def get_all_reservations_by_user(self, user_id: UUID4) -> Iterable[Reservation]:
        """The method getting all reservations from the database based on its user ID.

        Args:
            user_id (UUID4): The UUID of the user.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        query = select(reservation_table).where(reservation_table.c.user_id == user_id)
        reservations = await database.fetch_all(query)
        return [Reservation(**dict(reservation)) for reservation in reservations]

    async def get_all_reservations_by_equipment_id(self, equipment_id: int) -> Iterable[Reservation]:
        """The method getting all reservations from the database based on its equipment ID.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        query = select(reservation_table).where(reservation_table.c.equipment_id == equipment_id)
        reservations = await database.fetch_all(query)
        return [Reservation(**dict(reservation)) for reservation in reservations]

    async def get_all_reservations_by_category_id(
        self, category_id: int
    ) -> Iterable[Reservation]:
        """The method getting all reservations from the database based on its category ID.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        query = (
            select(
                reservation_table.c.id,
                reservation_table.c.user_id,
                reservation_table.c.equipment_id,
                reservation_table.c.start_date,
                reservation_table.c.end_date,
                reservation_table.c.status,
                reservation_table.c.total_price,
            )
            .join(equipment_table, reservation_table.c.equipment_id == equipment_table.c.id)
            .where(equipment_table.c.category_id == category_id)
        )
        reservations = await database.fetch_all(query)
        return [Reservation(**dict(reservation)) for reservation in reservations]

    async def get_all_reservations_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Reservation]:
        """The method getting all reservations from the database based on its subcategory ID.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Reservation]: The collection of the all reservations.
        """
        query = (
            select(
                reservation_table.c.id,
                reservation_table.c.user_id,
                reservation_table.c.equipment_id,
                reservation_table.c.start_date,
                reservation_table.c.end_date,
                reservation_table.c.status,
                reservation_table.c.total_price,
            )
            .join(equipment_table, reservation_table.c.equipment_id == equipment_table.c.id)
            .where(equipment_table.c.subcategory_id == subcategory_id)
        )
        reservations = await database.fetch_all(query)
        return [Reservation(**dict(reservation)) for reservation in reservations]

    async def add_reservation(self, data: ReservationIn) -> Reservation | None:
        """The method adding new reservation to the database.

        Args:
            data (ReservationIn): The attributes of the reservation.
        """
        data_dict = data.model_dump()
        if data_dict.get("status") is None:
            del data_dict["status"]
            
        query = insert(reservation_table).values(**data_dict)
        new_reservation_id = await database.execute(query)
        new_reservation = await self._get_by_id(new_reservation_id)
        return Reservation(**dict(new_reservation)) if new_reservation else None

    async def update_reservation(
        self, reservation_id: int, data: ReservationIn
    ) -> Reservation | None:
        """The method updating reservation in the database.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Reservation | None: The updated reservation if exists.
        """
        if await self._get_by_id(reservation_id):
            query = (
                update(reservation_table)
                .where(reservation_table.c.id == reservation_id)
                .values(**data.model_dump(exclude_unset=True))
            )
            await database.execute(query)
            updated_reservation = await self._get_by_id(reservation_id)
            return Reservation(**dict(updated_reservation)) if updated_reservation else None
        return None

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method removing reservation from the database.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """
        if await self._get_by_id(reservation_id):
            query = delete(reservation_table).where(reservation_table.c.id == reservation_id)
            await database.execute(query)
            return True
        return False

    async def get_most_rented_equipment_ids(self, limit: int) -> Iterable[dict]:
        """The method getting most rented equipment IDs from the database.

        Args:
            limit (int): The limit of the most rented equipment IDs.

        Returns:
            Iterable[dict]: The collection of the most rented equipment IDs.
        """
        query = (
            select(
                reservation_table.c.equipment_id,
                func.count(reservation_table.c.id).label("count")
            )
            .where(reservation_table.c.status == "finished")
            .group_by(reservation_table.c.equipment_id)
            .order_by(func.count(reservation_table.c.id).desc())
            .limit(limit)
        )
        results = await database.fetch_all(query)
        return [dict(row) for row in results]

    async def _get_by_id(self, reservation_id: int) -> Record | None:
        """The method getting reservation from the database based on its ID.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Record | None: The reservation record if exists.
        """
        query = select(reservation_table).where(reservation_table.c.id == reservation_id)
        return await database.fetch_one(query)
