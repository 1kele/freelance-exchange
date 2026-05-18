import pytest

from src.database import async_session_maker_null_pool
from src.db_manager import DBManager
from src.schemas.user import PublicRole, UserBlock


@pytest.mark.parametrize(
    "email, username, password, first_name, last_name, middle_name, role, status_code",
    [
        ("norma@mail.ru", "1kele_32", "123123", "Mikhail", "Ivanovich", "Peredernov", PublicRole.customer, 200),
        ("1@mail.ru", "1ke23le", "123112323", "Ail", "Ivanovich", "Peredernov", PublicRole.freelancer, 200),
        ("blocked@mail.ru", "qwerty", "barmaley", "Ivanov", "Ivan", "Ivanovich", PublicRole.freelancer, 200),
        ("normaad.ru", "AWQ", "qweqwe", "Shreck", "Victor", "Dudka", PublicRole.freelancer, 422),
        ("", "qweqeeqweq", "123123", "Zavar", "Zikin", "Vilanch", PublicRole.customer, 422),
        ("norma@mail.ru", "45612", "delivery", "Bebra", "Irina", "Pavlovna", PublicRole.customer, 409),
        ("awdeev@mail.ru", "1ke23le", "Kirill", "boroda1337", "Sarichev", "Pavlov", PublicRole.customer, 409),
    ]
)
async def test_register(
    ac,
    email,
    username,
    password,
    first_name,
    last_name,
    middle_name,
    role,
    status_code
):

    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "role": role
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()["status"] == "OK"


@pytest.fixture(scope="session")
async def setup_blocked_user():
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        user = await db_.user.get_one(email="blocked@mail.ru")
        await db_.user.edit(UserBlock(is_blocked=True), id=user.id)
        await db_.commit()

@pytest.mark.parametrize("email, password, status_code", [
    ("norma@mail.ru", "123123", 200),
    ("1@mail.ru", "Ail", 401),
    ("13221@mail.ru", "A3il", 404),
    ("13221il.com", "123123", 422),
    ("blocked@mail.ru", "qwerty", 403),
])
async def test_login(
    ac,
    email,
    password,
    status_code,
    setup_blocked_user
):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert isinstance(response.json()["access_token"], str)


async def test_get_me(auth_ac_customer):
    response = await auth_ac_customer.get("/auth/get_me")
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "customer@gmail.com"


async def test_partially_update_profile(auth_ac_customer):
    response = await auth_ac_customer.patch(
        "/auth/me",
        json={
            "first_name": "NewName",
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"

async def test_partially_update_profile_unauthorized(ac):
    response = await ac.patch(
        "/auth/me",
        json={
            "first_name": "NewName",
        }
    )

    assert response.status_code == 401