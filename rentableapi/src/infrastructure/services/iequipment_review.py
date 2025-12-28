"""Module containing equipment review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.equipment_review import EquipmentReview, EquipmentReviewIn

class IEquipmentReviewService(ABC):
    """An abstract class representing protocol of equipment review service."""
    @abstractmethod
    async def get_equipment_review_by_id(self, equipment_review_id: int) -> EquipmentReview | None:
        """The method getting an equipment review from the repository.
        
        Args:
            equipment_review_id (int): The id of the equipment review.
        
        Returns:
            EquipmentReview | None: The equipment review data if exists.
        """
    
    @abstractmethod
    async def get_all_equipment_reviews(self) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the repository.

        Returns:
            Iterable[EquipmentReview]: The collection of all equipment reviews.
        """

    @abstractmethod
    async def get_reviews_by_equipment_id(
        self, equipment_id: int
    ) -> Iterable[EquipmentReview] | None:
        """The method getting all equipment reviews from the repository based on provided equipment id.

        Args:
            equipment_id (int): The id of the equipment

        Returns:
            Iterable[EquipmentReview] | None: The collection of all equipment reviews if exists.
        """

    @abstractmethod
    async def get_reviews_by_reviewer_id(
        self, reviewer_id: UUID4
    ) -> Iterable[EquipmentReview] | None:
        """The method getting all equipment reviews from the repository based on provided reviewer id.

        Args:
            reviewer_id (UUID4): The UUID of the reviewer

        Returns:
            Iterable[EquipmentReview] | None: The collection of all equipment reviews if exists.
        """
    
    @abstractmethod
    async def get_average_rating_for_equipment(self, equipment_id: int) -> float | None:
        """The method getting average rating for equipment from the repository based on provided equipment id.

        Args:
            equipment_id (int): The id of the equipment

        Returns:
            float | None: The average rating if exists.
        """

    @abstractmethod
    async def add_equipment_review(self, data: EquipmentReviewIn) -> EquipmentReview | None:
        """The method adding new equipment review to the repository.

        Args:
            data (EquipmentReviewIn): The attributes of the equipment review.

        Returns:
            EquipmentReview | None: The newly created equipment review if exists.
        """

    async def delete_equipment_review(self, equipment_review_id: int) -> bool:
        """The method removing equipment review from the repository.

        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns:
            bool: Success of the operation.
        """