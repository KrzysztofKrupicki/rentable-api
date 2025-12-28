"""Module containing subcategory service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.subcategory import Subcategory, SubcategoryIn

class ISubcategoryService(ABC):
    """An abstract class representing protocol of subcategory service."""
    @abstractmethod
    async def get_subcategory_by_id(self, subcategory_id: int) -> Subcategory | None:
        """The method getting a subcategory from the repository.
        
        Args:
            subcategory_id (int): The id of the subcategory.
        
        Returns:
            Subcategory | None: The subcategory data if exists.
        """
    
    @abstractmethod
    async def get_all_subcategories(self) -> Iterable[Subcategory]:
        """The method getting all subcategory from the repository.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories.
        """
    
    @abstractmethod
    async def add_subcategory(self, data: SubcategoryIn) -> Subcategory | None:
        """The method adding new subcategory to the repository.
        
        Args:
            data (SubcategoryIn): The attributes of the subcategory.

        Returns:
            Subcategory | None: The newly created subcategory.
        """
    @abstractmethod
    async def update_subcategory(self, subcategory_id: int, data: SubcategoryIn) -> Subcategory | None:
        """The method updating subcountry data in the repository.
        
        Args:
            subcategory_id (int): The subcategory id.
            data (SubcategoryIn): The attributes of the subcategory.
        
        Returns:
            Subcategory | None: The updated subcategory.
        """

    @abstractmethod
    async def delete_subcategory(self, subcategory_id: int) -> bool:
        """The method deleting subcategory from the repository.
        
        Args:
            subcategory_id (int): The subcategory id.

        Returns:
            bool: The success of the operation.
        """