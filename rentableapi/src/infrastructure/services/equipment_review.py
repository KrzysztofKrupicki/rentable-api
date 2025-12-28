"""Module containing equipment review implementation."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.equipment_review import EquipmentReview, EquipmentReviewIn
from src.core.repositories.iequipment_review import IEquipmentReviewRepository
from src.infrastructure.services.iequipment_review import IEquipmentReviewService

class EquipmentReviewService(IEquipmentReviewService):
    """A class implementing the equipment review service."""

    _repository: IEquipmentReviewRepository

    def __init__(self, repository: IEquipmentReviewRepository) -> None:
        """The initializer of the equipment review service.
        
        Args:
            repository (IEquipmentReviewRepository): The reference to the repository.
        """
        self._repository = repository
    
    async def get_equipment_review_by_id(self, equipment_review_id: int) -> EquipmentReview | None:
        """The method getting an equipment review from the repository.
        
        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns: 
            EquipmentReview | None: The equipment review data if exists.
        """
        return await self._repository.get_equipment_review_by_id(equipment_review_id)

    async def get_all_equipment_reviews(self) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the repository.

        Returns:
            Iterable[EquipmentReview]: The collection of all equipment reviews.
        """
        return await self._repository.get_all_equipment_reviews()

    async def get_reviews_by_equipment_id(self, equipment_id: int) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the repository.

        Args:
            equipment_id (int): The equipment id.

        Returns:
            Iterable[EquipmentReview]: The collection of all equipment reviews.
        """
        return await self._repository.get_reviews_by_equipment_id(equipment_id)
    
    async def get_reviews_by_reviewer_id(self, reviewer_id: UUID4) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the repository.

        Args:
            reviewer_id (UUID4): The reviewer id.

        Returns:
            Iterable[EquipmentReview]: The collection of all equipment reviews.
        """
        return await self._repository.get_reviews_by_reviewer_id(reviewer_id)

    async def get_average_rating_for_equipment(self, equipment_id: int) -> float | None:
        """The method getting average rating for equipment from the repository.

        Args:
            equipment_id (int): The equipment id.

        Returns:
            float | None: The average rating for equipment.
        """
        return await self._repository.get_average_rating_for_equipment(equipment_id)

    async def add_equipment_review(self, data: EquipmentReviewIn) -> EquipmentReview | None:
        """The method adding new equipment review to the repository.
        
        Args:
            data (EquipmentReviewIn): The attributes of the equipment review.

        Returns:
            EquipmentReview | None: The newly created equipment review.
        """
        return await self._repository.add_equipment_review(data)
    
    async def delete_equipment_review(self, equipment_review_id: int) -> bool:
        """The method deleting equipment review from the repository.
        
        Args:
            equipment_review_id (int): The equipment review id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_equipment_review(equipment_review_id)