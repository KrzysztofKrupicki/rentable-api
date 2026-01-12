"""Module containing user service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.user import User, UserIn
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO


class IUserService(ABC):
    """An abstract class representing protocol of user service."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> UserDTO | None:
        """The method registering a new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def get_all_users(self) -> Iterable[User]:
        """The method getting all registered users.

        Returns:
            Iterable[User]: The collection of all registered users
        """

    @abstractmethod
    async def get_user_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """The method getting user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data if exists.
        """

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserDTO | None:
        """The method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data if exists.
        """
