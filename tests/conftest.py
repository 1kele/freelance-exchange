import pytest
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient, ASGITransport
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.db_manager import DBManager
from src.main import app
from src.models import *
from src.config import settings
from src.schemas.user import AdminUserUpdate, AllRoles


@pytest.fixture(scope="session",autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture()
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture()
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/auth/register", json={
            "email": "customer@gmail.com",
            "password": "123123",
            "username": "customer_user",
            "first_name": "Customer",
            "last_name": "Test",
            "middle_name": "Test",
            "role": "customer"
        })
        await ac.post("/auth/register", json={
            "email": "freelancer@gmail.com",
            "password": "123123",
            "username": "freelancer_user",
            "first_name": "Freelancer",
            "last_name": "Test",
            "middle_name": "Test",
            "role": "freelancer"
        })

        await ac.post("/auth/register", json={
            "email": "admin@gmail.com",
            "password": "123123",
            "username": "super_admin",
            "first_name": "Admin",
            "last_name": "ADMINISTRATOR",
            "middle_name": "administrator",
            "role": "customer"
        })

        await ac.post("/auth/register", json={
            "email": "prosto@test.com",
            "password": "123123",
            "username": "123123",
            "first_name": "qwerty",
            "last_name": "qwerty",
            "middle_name": "qwerty",
            "role": "customer"
        })

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.user.edit(
            AdminUserUpdate(role=AllRoles.admin),
            email="admin@gmail.com"
        )
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def auth_ac_customer(register_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "customer@gmail.com",
                "password": "123123",
            }
        )
        yield ac

@pytest.fixture(scope="session")
async def auth_ac_freelancer(register_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "freelancer@gmail.com",
                "password": "123123",
            }
        )
        yield ac

@pytest.fixture(scope="session")
async def auth_ac_admin(register_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "admin@gmail.com",
                "password": "123123",
            }
        )
        yield ac