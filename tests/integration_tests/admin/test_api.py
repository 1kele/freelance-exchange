from src.schemas.order import OrderStatus
from src.schemas.user import AllRoles


async def test_get_all_users_filter_by(auth_ac_admin):
    response = await auth_ac_admin.get("/admin")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert "data" in response.json()

async def test_assign_user_admin(auth_ac_admin):
    response = await auth_ac_admin.patch("/admin/assign/4", json={"role": AllRoles.freelancer})

    assert response.status_code == 200
    assert response.json()["status"] == "OK"

async def test_block_unblock_user(auth_ac_admin, db):
    response = await auth_ac_admin.patch("/admin/block/4", params={"is_blocked": True})
    user = await db.user.get_one(id=4)

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert user.is_blocked == True

async def test_get_orders(auth_ac_admin):
    response = await auth_ac_admin.get("/admin/orders", params={"status": OrderStatus.in_progress.value})

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert "data" in response.json()

async def test_delete_order(auth_ac_admin):
    response = await auth_ac_admin.delete("/admin/orders/3/delete")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"