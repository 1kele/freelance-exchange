from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.exceptions import UserNotFoundException, UserNotFoundHTTPException
from src.services.profiles import ProfileService

router = APIRouter(prefix="/profiles", tags=["Профили"])


@router.get("/{user_id}")
async def get_profile(
    db: DBDep,
    user_id: int,
):
    try:
        return await ProfileService(db).get_profile(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.get("/{user_id}/reviews")
async def get_user_review(db: DBDep, user_id: int):
    try:
        return await ProfileService(db).get_user_review(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
