from typing import ClassVar, Generic, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from app.models.base.base import TBaseSQLModel
from app.repositories.base import BaseRepository
from app.schemas.base import BaseCreateSchema, BasePublicSchema
from app.schemas.base.base import TBaseCreateSchema, TBasePublicSchema
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService(Generic[TBaseSQLModel, TBaseCreateSchema, TBasePublicSchema]):
    sql_model_cls: ClassVar[Type[TBaseSQLModel]]
    create_schema_cls: ClassVar[Type[TBaseCreateSchema]]
    public_schema_cls: ClassVar[Type[TBasePublicSchema]]
