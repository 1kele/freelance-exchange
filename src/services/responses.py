from typing import Sequence

from src.exceptions import (
    AlreadyRespondedException,
    PermissionDeniedException,
    AlreadyAcceptedException,
)
from src.models import ResponsesOrm
from src.schemas.order import OrderAccept, OrderStatus
from src.schemas.response import (
    ResponseAdd,
    ResponseAddRequest,
    ResponseStatusRequest,
    ResponseStatus,
    Response,
)
from src.schemas.user import PublicRole
from src.services.base import BaseService
from src.services.orders import OrderService
from datetime import date, timedelta


class ResponsesService(BaseService):
    async def _change_response_status(
        self, response_id: int, current_user_id: int, new_status: ResponseStatus
    ) -> None:
        response = await self.db.response.get_one(id=response_id)
        if response.status == new_status:
            raise AlreadyAcceptedException
        await OrderService(self.db).check_order_ownership(
            response.order_id, current_user_id
        )
        await self.db.response.edit(
            ResponseStatusRequest(status=new_status), id=response_id
        )
        await self.db.commit()

    async def respond_to_order(
        self, order_id: int, user_id: int, data: ResponseAdd
    ) -> None:
        freelancer = await self.db.response.get_filter_by(
            order_id=order_id, freelancer_id=user_id
        )
        if freelancer:
            raise AlreadyRespondedException
        new_data = ResponseAddRequest(
            order_id=order_id, freelancer_id=user_id, **data.model_dump()
        )
        await self.db.response.add(new_data)
        await self.db.commit()

    async def get_all_responses_by_order_id(
        self,
        order_id: int,
    ) -> list[Response]:
        result = await self.db.response.get_filter_by(order_id=order_id)
        return result

    async def accept_response(self, response_id: int, current_user_id: int) -> None:
        response = await self.db.response.get_one(id=response_id)
        await self._change_response_status(
            response_id, current_user_id, ResponseStatus.accepted
        )
        order = await self.db.order.get_one(id=response.order_id)
        deadline_date = date.today() + timedelta(days=order.deadline_days)
        await self.db.order.edit(
            OrderAccept(
                freelancer_id=response.freelancer_id,
                status=OrderStatus.in_progress,
                deadline_date=deadline_date,
            ),
            id=response.order_id,
        )
        await self.db.commit()

    async def reject_response(self, response_id: int, current_user_id: int) -> None:
        await self._change_response_status(
            response_id, current_user_id, ResponseStatus.rejected
        )
        await self.db.commit()

    async def get_all_my_responses(
        self, current_user_role: str, current_user_id: int
    ) -> Sequence[ResponsesOrm]:
        if current_user_role != PublicRole.freelancer:
            raise PermissionDeniedException

        result = await self.db.response.get_filter_by(freelancer_id=current_user_id)
        return result