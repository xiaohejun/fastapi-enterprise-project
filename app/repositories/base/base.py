# from typing import TypeVar
# from uuid import UUID

from typing import ClassVar, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlmodel import SQLModel
from app.models.base.base import TBaseSQLModel


class BaseRepository(Generic[TBaseSQLModel]):
    def __init__(self, session: AsyncSession, sqlmodel_cls: Type[TBaseSQLModel]):
        if not isinstance(session, AsyncSession):
            raise TypeError("session must be an instance of AsyncSession, but got {}".format(type(session)))
        self.session = session
        self.sql_model_cls = sqlmodel_cls

    # async def get(self, id: UUID) -> SQLModel | None:
    #     result = await self.session.execute(
    #         select(self.model).where(self.model.id == id)
    #     )
    #     return result.scalars().first()

    # async def get_all(self, skip: int = 0, limit: int = 100) -> list[SQLModel]:
    #     result = await self.session.execute(
    #         select(self.model).offset(skip).limit(limit)
    #     )
    #     return result.scalars().all()

    # async def update(self, id: UUID, update_data: dict) -> SQLModel | None:
    #     instance = await self.get(id)
    #     if not instance:
    #         return None

    #     for key, value in update_data.items():
    #         setattr(instance, key, value)

    #     self.session.add(instance)
    #     await self.session.commit()
    #     await self.session.refresh(instance)
    #     return instance

    # async def delete(self, id: UUID) -> bool:
    #     instance = await self.get(id)
    #     if not instance:
    #         return False

    #     await self.session.delete(instance)
    #     await self.session.commit()
    #     return True


TBaseRepository = TypeVar("TBaseRepository", bound=BaseRepository)
