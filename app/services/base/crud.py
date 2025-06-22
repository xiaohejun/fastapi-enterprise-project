
from typing import Any, ClassVar, Generic, Type
from app.models.base.base import TBaseSQLModel
from app.repositories.base.base import BaseRepository
from app.repositories.base.crud import CreateBaseRepository
from app.schemas.base.base import TBaseCreateSchema, TBasePublicSchema
from app.services.base.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

class CreateBaseService:
    def __init__(self, session: AsyncSession, sqlmodel_cls: Type[TBaseSQLModel], create_schema_cls: Type[TBaseCreateSchema], public_schema_cls: Type[TBasePublicSchema]):
        self.sqlmodel_cls = sqlmodel_cls
        self.create_schema_cls = create_schema_cls
        self.public_schema_cls = public_schema_cls
        self.repo = CreateBaseRepository(session, self.sqlmodel_cls)
    
    async def create(self, create_data: TBaseCreateSchema) -> TBasePublicSchema:
        instance = create_data.to_sqlmodel(self.sqlmodel_cls)
        instance = await self.repo.create(instance)
        return self.public_schema_cls.from_sqlmodel(instance)

class CRUDBaseService(Generic[TBaseSQLModel, TBaseCreateSchema, TBasePublicSchema]):
    sqlmodel_cls: ClassVar[Type[TBaseSQLModel]]
    create_schema_cls: ClassVar[Type[TBaseCreateSchema]]
    public_schema_cls: ClassVar[Type[TBasePublicSchema]]

    def __init__(self, session: AsyncSession):
        assert self.sqlmodel_cls, "sqlmodel_cls must be set"
        assert self.create_schema_cls, "create_schema_cls must be set"
        assert self.public_schema_cls, "public_schema_cls must be set"
        self.create_service = CreateBaseService(session, self.sqlmodel_cls, self.create_schema_cls, self.public_schema_cls)

    async def create(self, create_data: TBaseCreateSchema) -> TBasePublicSchema:
        return await self.create_service.create(create_data)
