"""Module containing equipment review repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.equipment_review import (
    EquipmentReview,
    EquipmentReviewIn,
)


class IEquipmentReviewRepository(ABC):
    """The abstract class representing protocol of equipment reviews repository."""

    @abstractmethod
    async def get_all_equipment_reviews(self) -> Iterable[EquipmentReview]:
        """The abstract method getting all equipment reviews from the data storage.

        Returns:
            Iterable[EquipmentReview]: Equipment reviews in the data storage.
        """

    @abstractmethod
    async def get_equipment_review_by_id(
        self, equipment_review_id: int
    ) -> EquipmentReview | None:
        """The abstract method getting equipment review by provided id.

        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns:
            EquipmentReview | None: The equipment review details.
        """

    @abstractmethod
    async def get_reviews_by_equipment_id(
        self, equipment_id: int
    ) -> Iterable[EquipmentReview] | None:
        """The abstract method getting all equipment reviews by provided equipment id.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Iterable[EquipmentReview]: The collection of the all equipment reviews for provided equipment.
        """

    @abstractmethod
    async def get_reviews_by_reviewer_id(
        self, reviewer_id: UUID4
    ) -> Iterable[EquipmentReview] | None:
        """The abstract method getting all equipment reviews by provided reviewer id.

        Args:
            reviewer_id (UUID4): The id of the reviewer.

        Returns:
            Iterable[EquipmentReview]: The collection of the all equipment reviews from provided reviewer.
        """

    @abstractmethod
    async def get_average_rating_for_equipment(self, equipment_id: int) -> float | None:
        """The abstract method getting average rating for the equipment by provided equipment id.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            float | None: The average rating for the equipment.
        """

    @abstractmethod
    async def add_equipment_review(self, data: EquipmentReviewIn) -> EquipmentReview | None:
        """The abstract method adding new equipment review to the data storage.

        Args:
            data (EquipmentReviewIn): The details of the new equipment review.

        Returns:
            EquipmentReview | None: The newly created equipment review.
        """

    @abstractmethod
    async def delete_equipment_review(self, equipment_review_id: int) -> bool:
        """The abstract method remmoving equipment review from the data storage.

        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns:
            bool: Success of the operation.
        """
