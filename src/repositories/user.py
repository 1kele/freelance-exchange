from sqlalchemy.testing.pickleable import User
from sqlalchemy import insert,select

from src.exceptions import RoleNotFoundException
from src.models.users import UserOrm
from src.repositories.base import BaseRepositories
from src.schemas.user import UserAddRequest, AllRoles, PublicRole, UserForAdmin


class UserRepository(BaseRepositories):
    model = UserOrm
    schema = User

    async def add(self, data: UserAddRequest):
        role = data.model_dump()['role'].lower()
        if role != PublicRole.customer and role != PublicRole.freelancer:
            raise RoleNotFoundException
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def get_pagination(
            self,
            limit: int,
            offset: int,
            role:AllRoles | None = None
    ):
        if role:
            query = select(self.model).filter_by(role=role)
        else:
            query = select(self.model)

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        return [UserForAdmin.model_validate(u, from_attributes=True) for u in result.scalars().all()]