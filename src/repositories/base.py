from typing import Any, ClassVar

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete

from src.exceptions import ObjectNotFoundException


class BaseRepositories:
    model: ClassVar[Any] = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_filter_by(self, **filter_by) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_date_range(
        self, date_from, date_to, **filter_by
    ) -> Any:
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .where(self.model.created_at <= date_to, self.model.created_at >= date_from)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one(self, **filter_by) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalar_one_or_none()
        if obj is None:
            raise ObjectNotFoundException
        return obj

    async def add(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def edit(self, data: BaseModel, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        result = delete(self.model).filter_by(**filter_by)
        await self.session.execute(result)
