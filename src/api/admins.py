from fastapi import APIRouter

from src.api.dependencies import DBDep, PaginationDep, AdminDep
from src.exceptions import PermissionDeniedException, PermissionDeniedHTTPException, UserAlreadyHasRoleHTTPException, \
    UserAlreadyHasRoleException, ObjectNotFoundException, ObjectNotFoundHTTPException
from src.schemas.order import OrderStatus, OrderCategory
from src.schemas.user import AllRoles, AdminUserUpdate
from src.services.admins import AdminService
from src.services.orders import OrderService

router = APIRouter(prefix="/admin", tags=["Админ"])

@router.get("")
async def get_all_users_filter_by(
    db: DBDep,
    pagination: PaginationDep,
    current_user: AdminDep,
    role: AllRoles | None = None,
):
    try:
        result = await AdminService(db).get_user_pagination(
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
            role=role
    )
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    return {"status": "OK", "data": result}

@router.patch("/assign/{user_id}")
async def assign_user_admin(
    user_id: int,
    db: DBDep,
    current_user: AdminDep,
    data: AdminUserUpdate
):
    try:
        await AdminService(db).assign_role(user_id, data.role)
    except UserAlreadyHasRoleException:
        raise UserAlreadyHasRoleHTTPException

    return {"status": "OK"}


@router.patch("/block/{user_id}")
async def block_unblock_user(
    user_id: int,
    db: DBDep,
    current_user: AdminDep,
    is_blocked: bool
):
    await AdminService(db).block_unblock_user(user_id, is_blocked)
    return {"status": "OK"}

@router.get("/orders")
async def get_orders(
    db: DBDep,
    current_user: AdminDep,
    pagination: PaginationDep,
    order_id: int | None = None,
    status: OrderStatus | None = None,
    category: OrderCategory | None = None
):
    try:
        result = await AdminService(db).get_orders(
            order_id=order_id,
            status=status,
            category=category,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"status": "OK", "data": result}

@router.delete("/orders/{order_id}/delete")
async def delete_order(
    order_id: int,
    db: DBDep,
    current_user: AdminDep,
):
    await AdminService(db).delete_order(order_id)
    return {"status": "OK"}