"""Module containing category service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.category import Category, CategoryIn

class ICategoryService(ABC):
    """An abstract class representing protocol of category service."""
    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Category | None:
        """The method getting a category from the repository.
        
        Args:
            category_id (int): The id of the category.
        
        Returns:
            Category | None: The category data if exists.
        """
    
    @abstractmethod
    async def get_all_categories(self) -> Iterable[Category]:
        """The method getting all categories from the repository.

        Returns:
            Iterable[Category]: The collection of the all categories.
        """
    
    @abstractmethod
    async def add_category(self, data: CategoryIn) -> Category | None:
        """The method adding new category to the repository.
        
        Args:
            data (CategoryIn): The attributes of the category.

        Returns:
            Category | None: The newly created category.
        """
    @abstractmethod
    async def update_category(self, category_id: int, data: CategoryIn) -> Category | None:
        """The method updating category data in the repository.
        
        Args:
            category_id (int): The category id.
            data (CategoryIn): The attributes of the category.
        
        Returns:
            Category | None: The updated category.
        """

    @abstractmethod
    async def delete_category(self, category_id: int) -> bool:
        """The method deleting category from the repository.
        
        Args:
            category_id (int): The category id.

        Returns:
            bool: The success of the operation.
        """