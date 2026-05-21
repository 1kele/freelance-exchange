import pytest

from src.schemas.order import OrderCategory


async def test_get_orders_filter_by(auth_ac_customer):
    response = await auth_ac_customer.get(
        "/orders", params={"category": OrderCategory.design}
    )

    assert response.status_code == 200


async def test_get_my_orders(auth_ac_customer):
    response = await auth_ac_customer.get(
        "/orders/my_orders",
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert "data" in response.json()


@pytest.mark.parametrize(
    "id, title, description, price, category, deadline_days, status_code",
    [
        (
            1,
            "Сделать лого",
            "Нужен логотип для стартапа",
            5000,
            OrderCategory.design,
            7,
            200,
        ),
        (
            2,
            "Разработать сайт",
            "Лендинг на React",
            30000,
            OrderCategory.development,
            14,
            200,
        ),
        (
            3,
            "Написать статью",
            "SEO статья 3000 слов",
            2000,
            OrderCategory.copywriting,
            3,
            200,
        ),
        (4, "", "Пустой заголовок", 1000, OrderCategory.design, 5, 422),
        (5, "Нормальный заказ", "Описание", -100, OrderCategory.design, 5, 422),
    ],
)
async def test_create_order(
    auth_ac_customer,
    id,
    title,
    description,
    price,
    category,
    deadline_days,
    status_code,
):
    response = await auth_ac_customer.post(
        "/orders",
        json={
            "title": title,
            "description": description,
            "price": price,
            "category": category,
            "deadline_days": deadline_days,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    order = await auth_ac_customer.get(f"/orders/{id}")

    assert order.json()["data"]["title"] == title
    assert order.json()["data"]["description"] == description
    assert order.json()["data"]["price"] == price
    assert order.json()["data"]["category"] == category
    assert order.json()["data"]["deadline_days"] == deadline_days


async def test_get_order_by_id(auth_ac_customer):
    response = await auth_ac_customer.get("/orders/1")
    assert response.status_code == 200


async def test_cancel_order(auth_ac_customer):
    response = await auth_ac_customer.patch("/orders/1/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"

    order = await auth_ac_customer.get("/orders/1")
    assert order.json()["data"]["status"] == "cancelled"


async def test_update_order(auth_ac_customer):
    response = await auth_ac_customer.patch(
        "/orders/1", json={"title": "Да ничего не нужно"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"


async def test_delete_my_order(auth_ac_customer):
    response = await auth_ac_customer.delete("/orders/1")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
