from fastapi import APIRouter

from src.api.dependencies import DBDep, CurrentUserDep
from decimal import Decimal

from src.exceptions import PermissionDeniedException, PermissionDeniedHTTPException, ObjectNotFoundException, \
    ObjectNotFoundHTTPException, OrderNotInProgressException, OrderNotInProgressHTTPException, \
    AlreadyRespondedHTTPException, AlreadyRespondedException, AlreadyRejectedException, AlreadyRejectedHTTPException, \
    AlreadyAcceptedException, AlreadyAcceptedHTTPException
from src.schemas.order import OrderAddRequest, OrderPatch
from src.schemas.response import ResponseAdd
from src.services.orders import OrderService
from src.services.responses import ResponsesService

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get("")
async def get_orders_filter_by(
    db: DBDep,
    category: str | None = None,
    price_to: Decimal | None = None,
):
    return await OrderService(db).get_free_orders(category, price_to)


@router.get("/my_orders")
async def get_my_orders(
    db: DBDep,
    current_user: CurrentUserDep
):
    result = await OrderService(db).get_my_orders(current_user)
    return {"status": "OK", "data": result}


@router.get("/{order_id}")
async def get_order_by_id(
    db: DBDep,
    order_id: int
):
    try:
        result = await OrderService(db).get_one_order(order_id)
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException

    return {"status": "OK", "data": result}

@router.post("")
async def create_order(
    db: DBDep,
    data: OrderAddRequest,
    current_user: CurrentUserDep
):
    try:
        await OrderService(db).create_order(data, current_user)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException

    return {"status": "OK"}


@router.patch("/{order_id}/cancel")
async def cancel_order(
    db: DBDep,
    order_id: int,
    current_user:CurrentUserDep
):
    try:
        await OrderService(db).check_order_ownership(order_id, current_user.id)
        await OrderService(db).cancel_order(order_id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{order_id}")
async def update_order(
    db: DBDep,
    order_id: int,
    data: OrderPatch,
    current_user: CurrentUserDep
):
    try:
        await OrderService(db).check_order_ownership(order_id, current_user.id)
        await OrderService(db).update_order(order_id, data)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{order_id}")
async def delete_my_order(
    db: DBDep,
    order_id: int,
    current_user: CurrentUserDep
):
    try:
        await OrderService(db).check_order_ownership(order_id, current_user.id)
        await OrderService(db).delete_order(order_id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"status": "OK"}

@router.patch("/{order_id}/complete")
async def complete_order(
    db: DBDep,
    order_id: int,
    current_user: CurrentUserDep
):
    try:
        is_customer = await db.order.is_customer_order(order_id, current_user.id)
        is_freelancer = await db.order.is_freelancer_order(order_id, current_user.id)
        if not is_customer and not is_freelancer:
            raise PermissionDeniedException
        await OrderService(db).complete_order(order_id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    except OrderNotInProgressException:
        raise OrderNotInProgressHTTPException
    return {"status": "OK"}


@router.post(
    "/{order_id}/responses",
    tags=["Отклики"]
)
async def respond_to_order(
    db: DBDep,
    order_id: int,
    current_user: CurrentUserDep,
    data: ResponseAdd
):
    try:
        await ResponsesService(db).respond_to_order(order_id, current_user.id, data)
    except AlreadyRespondedException:
        raise AlreadyRespondedHTTPException
    return {"status": "OK"}

@router.get("/{order_id}/responses", tags=["Отклики"])
async def get_all_responses_by_order_id(
    db: DBDep,
    order_id:int,
    current_user: CurrentUserDep
):
    try:
        await OrderService(db).check_order_ownership(order_id, current_user.id)
        result = await ResponsesService(db).get_all_responses_by_order_id(order_id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException

    return {"status": "OK", "data": result}

@router.patch("/response/{response_id}/accept", tags=["Отклики"])
async def accept_response(
    db: DBDep,
    response_id: int,
    current_user: CurrentUserDep,
):
    try:
        await ResponsesService(db).accept_response(response_id, current_user.id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    except AlreadyAcceptedException:
        raise AlreadyAcceptedHTTPException

    return {"status": "OK"}

@router.patch("/response/{response_id}/rejected", tags=["Отклики"])
async def reject_response(
    db: DBDep,
    response_id: int,
    current_user: CurrentUserDep,
):
    try:
        await ResponsesService(db).reject_response(response_id, current_user.id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    except AlreadyRejectedException:
        raise AlreadyRejectedHTTPException

    return {"status": "OK"}