from src.exceptions import UserAlreadyHasRoleException
from src.schemas.user import AllRoles, AdminUserUpdate, UserBlock, UserForAdmin
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_user_pagination(
        self,
        limit: int,
        offset: int,
        role: AllRoles | None = None,
    ) -> list[UserForAdmin]:

        return await self.db.user.get_pagination(limit=limit, offset=offset, role=role)

    async def assign_role(self, user_id: int, role: AllRoles) -> None:
        user = await self.db.user.get_one(id=user_id)
        if user.role == role:
            raise UserAlreadyHasRoleException
        await self.db.user.edit(AdminUserUpdate(role=role), id=user_id)
        await self.db.commit()

    async def block_unblock_user(self, user_id: int, is_blocked: bool) -> None:
        await self.db.user.edit(UserBlock(is_blocked=is_blocked), id=user_id)
        await self.db.commit()

    async def get_orders(
        self,
        order_id: int | None = None,
        status: str | None = None,
        category: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        if order_id:
            return await self.db.order.get_one(id=order_id)

        return await self.db.order.get_orders_for_admin(status, category, limit, offset)

    async def delete_order(self, order_id: int):
        await self.db.order.delete(id=order_id)
        await self.db.commit()
