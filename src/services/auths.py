from sqlalchemy.exc import IntegrityError

from src.api.dependencies import CurrentUserDep
from src.exceptions import WrongPasswordException, ObjectNotFoundException, PermissionDeniedException, \
    UserIsBlockedException, UserAlreadyExistsException
from src.schemas.user import UserAddRequest, UserAdd, UserLogin, UserResponse, UserPatch
from src.services.auth import Authentication
from src.services.base import BaseService
from fastapi import Response
class AuthenticationService(BaseService):

    async def register(
        self,
        data: UserAddRequest,
    ):
        hashed_password = Authentication.get_password_hash(data.password)
        new_data = UserAdd(hashed_password=hashed_password, **data.model_dump(exclude={"password"}))
        try:
            await self.db.user.add(new_data)
            await self.db.commit()
        except IntegrityError:
            raise UserAlreadyExistsException

    async def login(
            self,
            data: UserLogin,
            response: Response,
    ):
        current_user = await self.db.user.get_one(email=data.email)
        if not current_user:
            raise ObjectNotFoundException
        if current_user.is_blocked:
            raise UserIsBlockedException
        if not Authentication.password_hash.verify(data.password, current_user.hashed_password):
            raise WrongPasswordException
        access_token = Authentication.create_access_token({"user_id": current_user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def get_me(
            self,
            current_user: CurrentUserDep
    ):
        return UserResponse.model_validate(current_user)

    async def partially_update_profile(
            self,
            user_id: int,
            data: UserPatch,
    ):
        await self.db.user.edit(data, id=user_id)
        await self.db.commit()

    async def logout(
            self,
            response: Response
    ):
        response.delete_cookie("access_token")