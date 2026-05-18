from datetime import date
from decimal import Decimal

from sqlalchemy.exc import NoResultFound

from src.api.dependencies import CurrentUserDep
from src.exceptions import PermissionDeniedException, ObjectNotFoundException, OrderNotInProgressException
from src.schemas.order import OrderPatchStatus, OrderAddRequest, OrderAdd, OrderPatch, OrderStatus, Order, OrderCancel
from src.schemas.user import User, PublicRole
from src.services.base import BaseService


class OrderService(BaseService):

    async def check_order_ownership(self, order_id: int, current_user_id: int) -> None:
        result = await self.db.order.is_customer_order(order_id, current_user_id)
        if not result:
            raise PermissionDeniedException

    async def check_freelancer_order_ownership(self, order_id: int, current_user_id: int) -> None:
        result = await self.db.order.is_freelancer_order(order_id, current_user_id)
        if not result:
            raise PermissionDeniedException

    async def cancel_order(self, order_id: int) -> None:
        try:
            await self.db.order.edit(OrderCancel(status=OrderStatus.cancelled), id=order_id)
            await self.db.commit()
        except NoResultFound:
            raise ObjectNotFoundException

    async def complete_order(self, order_id: int) -> None:
        order = await self.db.order.get_one(id=order_id)
        if order.status != OrderStatus.in_progress:
            raise OrderNotInProgressException
        try:
            is_overdue = date.today() > order.deadline_date if order.deadline_date else False
            await self.db.order.edit(OrderPatchStatus(status=OrderStatus.completed,is_overdue=is_overdue), id=order_id)
            await self.db.commit()
        except NoResultFound:
            raise ObjectNotFoundException



    async def get_free_orders(
        self,
        category: str | None = None,
        price_to: Decimal | None = None,
    ) -> list[Order]:
        return await self.db.order.get_orders_with_filters(category=category, price_to=price_to)

    async def get_my_orders(self, current_user: User) -> list[Order]:
        result = []
        if current_user.role == PublicRole.freelancer:
            result = await self.db.order.get_filter_by(freelancer_id=current_user.id)
        elif current_user.role == PublicRole.customer:
            result = await self.db.order.get_filter_by(customer_id=current_user.id)

        return result

    async def get_one_order(self, order_id: int) -> Order:
        result = await self.db.order.get_one(id=order_id)
        if not result:
            raise ObjectNotFoundException
        return result

    async def create_order(
        self,
        data: OrderAddRequest,
        current_user: CurrentUserDep
    ) -> None:
        if current_user.role == PublicRole.freelancer:
            raise PermissionDeniedException
        new_data = OrderAdd(**data.model_dump(), customer_id=current_user.id)
        await self.db.order.add(new_data)
        await self.db.commit()

    async def update_order(
        self,
        order_id: int,
        data: OrderPatch,
    ):
        try:
            await self.db.order.edit(data, id=order_id)
            await self.db.commit()
        except NoResultFound:
            raise ObjectNotFoundException

    async def delete_order(
        self,
        order_id: int,
    ) -> None:
        try:
            await self.db.order.delete(id=order_id)
            await self.db.commit()
        except NoResultFound:
            raise ObjectNotFoundException