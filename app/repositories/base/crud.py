from typing import Generic, Type, TypeVar

from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base.base import TBaseSQLModel


class CreateBaseRepository(BaseRepository[TBaseSQLModel]):
    def __init__(self, session: AsyncSession, sqlmodel_cls: Type[TBaseSQLModel]):
        super().__init__(session, sqlmodel_cls)

    async def create(self, instance: TBaseSQLModel) -> TBaseSQLModel:
        self.session.add(instance)
        # 将数据发送到数据库（生成ID等），但不提交事务
        await self.session.flush()
        return instance


class CRUDBaseRepository(Generic[TBaseSQLModel]):
    sql_model_cls: Type[TBaseSQLModel]

    def __init__(self, session: AsyncSession):
        assert self.sql_model_cls, "sql_model_cls must be set"
        self.create_service = CreateBaseRepository(session, self.sql_model_cls)

    async def create(self, create_data: TBaseSQLModel) -> TBaseSQLModel:
        return await self.create_service.create(create_data)


TCRUDBaseRepository = TypeVar("TCRUDBaseRepository", bound=CRUDBaseRepository)
