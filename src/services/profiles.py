from src.exceptions import UserNotFoundException, ObjectNotFoundException
from src.schemas.user import PublicUserInformation
from src.services.base import BaseService


class ProfileService(BaseService):


    async def get_profile(self, user_id: int) -> PublicUserInformation:
        try:
            user = await self.db.user.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        public_data = PublicUserInformation.model_validate(user, from_attributes=True)
        return public_data

    async def get_user_review(self, user_id: int) -> PublicUserInformation:
        try:
            await self.db.user.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        user_review = await self.db.review.get_filter_by(target_id=user_id)
        return user_review