from src.repositories.order import OrderRepository
from src.repositories.responses import ResponseRepository
from src.repositories.review import ReviewRepository
from src.repositories.user import UserRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(self.session)
        self.order = OrderRepository(self.session)
        self.response = ResponseRepository(self.session)
        self.review = ReviewRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
