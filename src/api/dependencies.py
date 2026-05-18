import jwt

from fastapi import Depends, HTTPException, Request,Query
from typing import Annotated

from pydantic import BaseModel

from src.config import settings
from src.database import async_session_maker
from src.db_manager import DBManager
from src.exceptions import ObjectNotFoundException
from src.schemas.user import UserResponse, User, AllRoles


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]


def decode_token(token: str) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Токен не найден")

    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный токен")


async def get_current_user(request: Request, db: DBDep):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    payload = decode_token(token)
    user_id = payload.get("user_id")

    try:
        current_user = await db.user.get_one(id=user_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if current_user.is_blocked:
        raise HTTPException(status_code=403, detail="Ваш аккаунт заблокирован")

    return current_user

CurrentUserDep = Annotated[User, Depends(get_current_user)]


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, description="Номер страницы", ge=1),
        per_page: int = Query(10, description="Количество на одной странице", ge=1, lt=30)
    ):
        self.page = page
        self.per_page = per_page

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


async def get_current_admin(current_user: CurrentUserDep):
    if current_user.role != AllRoles.admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return current_user

AdminDep = Annotated[User, Depends(get_current_admin)]