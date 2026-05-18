import pytest


async def test_add_review_customer(auth_ac_customer):
    response = await auth_ac_customer.post(
        "/reviews",
        json={
            "order_id": 2,
            "target_id": 2,
            "rating": 5,
            "text": "",
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


async def test_add_review_freelancer(auth_ac_freelancer):
    response = await auth_ac_freelancer.post(
        "/reviews",
        json={
            "order_id": 2,
            "target_id": 1,
            "rating": 4,
            "text": "Хороший заказчик",
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


@pytest.mark.parametrize("order_id, target_id, rating, text, status_code", [
    (1, 2, 5, "Все нормально", 404),
    (2, 2, 4, "Ну нормуль", 409),
    (3, 2, 4, "", 400),
    (2, 1, 5, "Отзыв на себя", 400),
    (99, 2, 5, "", 404),
])
async def test_add_review_errors(auth_ac_customer, order_id, target_id, rating, text, status_code):
    response = await auth_ac_customer.post(
        "/reviews",
        json={
            "order_id": order_id,
            "target_id": target_id,
            "rating": rating,
            "text": text,
        }
    )
    assert response.status_code == status_code


async def test_get_reviews_nonexistent_user(auth_ac_customer):
    response = await auth_ac_customer.get(
        "/reviews",
        params={"user_id": 999}
    )
    assert response.status_code == 404