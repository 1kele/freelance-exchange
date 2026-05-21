from decimal import Decimal
from typing import Any


from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.models.orders import OrdersOrm
from src.repositories.base import BaseRepositories
from src.schemas.order import Order, OrderStatus


class OrderRepository(BaseRepositories):
    model = OrdersOrm
    schema = Order

    async def get_orders_with_filters(
        self, category: str | None, price_to: Decimal | None
    ) -> list[Any]:
        query = select(self.model).where(self.model.status == OrderStatus.free)
        if category:
            query = query.where(self.model.category == category)
        if price_to:
            query = query.where(self.model.price <= price_to)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _get_order(self, order_id: int):
        query = select(self.model).filter(self.model.id == order_id)
        result = await self.session.execute(query)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

    async def is_customer_order(self, order_id: int, user_id: int) -> bool:
        order = await self._get_order(order_id)
        return order.customer_id == user_id

    async def is_freelancer_order(self, order_id: int, user_id: int) -> bool:
        order = await self._get_order(order_id)
        return order.freelancer_id == user_id

    async def get_orders_for_admin(
        self,
        status: str | None = None,
        category: str | None = None,
        limit: int | None = 10,
        offset: int | None = 0,
    ):
        query = select(self.model)

        if status:
            query = query.where(self.model.status == status)
        if category:
            query = query.where(self.model.category == category)

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return result.scalars().all()
