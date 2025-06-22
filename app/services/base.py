from typing import Generic, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from app.repositories.base import BaseRepository
from app.schemas.base import BaseCreateSchema, BasePublicSchema


class BaseService:
    def __init__(self, BaseRepository: BaseRepository, create_schema: BaseCreateSchema, publish_schema: BasePublicSchema):
        self.create_schema = create_schema
        self.public_schema = publish_schema
        self.repo = BaseRepository

    async def create(self, create_data: BaseCreateSchema) -> BaseModel:
        data = self.create_schema.model_validate(create_data)
        return self.public_schema.model_validate(await self.repo.create(data))
