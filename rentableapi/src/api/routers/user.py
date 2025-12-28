"""A module containing user endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from src.container import Container
from src.core.domain.user import UserIn
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService

router = APIRouter()

@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for registering new user

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if new_user := await service.register_user(user):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )


@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )


@router.get("/all", response_model=Iterable[UserDTO], status_code=200)
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[dict]:
    """An endpoint for getting all users.

    Args:
        service (IUserService, optional): The injected user service.

    Returns:
        Iterable[dict]: The list of user DTOs.
    """
    users = await service.get_all_users()
    return [UserDTO(**dict(user)).model_dump() for user in users]


@router.get("/{user_id}", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_id(
    user_id: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for getting user by id.

    Args:
        user_id (UUID4): The user UUID4.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        dict: The user DTO.
    """
    if user := await service.get_user_by_uuid(user_id):
        return UserDTO(**dict(user)).model_dump()

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )


@router.get("/email/{email}", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_email(
    email: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for getting user by email.

    Args:
        email (str): The user email.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        dict: The user DTO.
    """
    if user := await service.get_user_by_email(email):
        return UserDTO(**dict(user)).model_dump()

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )