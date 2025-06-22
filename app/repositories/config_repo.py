from typing import Type, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.data_models import (InferenceRuntimeConfig, ModelConfig,
                             SystemConfig, TrainRuntimeConfig)

from .base import BaseRepository

ConfigType = Union[
    ModelConfig, SystemConfig, InferenceRuntimeConfig, TrainRuntimeConfig
]


class ConfigBaseRepository:
    def __init__(self, session: AsyncSession, model: Type[ConfigType]):
        self.repo = BaseRepository(session, model)

    async def get_by_name(self, name: str) -> ConfigType | None:
        result = await self.repo.session.execute(
            select(self.repo.model).where(self.repo.model.name == name)
        )
        return result.scalars().first()

    async def get_templates(self) -> list[ConfigType]:
        result = await self.repo.session.execute(
            select(self.repo.model).where(self.repo.model.is_template == True)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: UUID) -> list[ConfigType]:
        result = await self.repo.session.execute(
            select(self.repo.model).where(self.repo.model.user_id == user_id)
        )
        return result.scalars().all()


class ModelConfigBaseRepository(ConfigBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ModelConfig)


class SystemConfigBaseRepository(ConfigBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SystemConfig)


class InferenceRuntimeConfigBaseRepository(ConfigBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InferenceRuntimeConfig)


class TrainRuntimeConfigBaseRepository(ConfigBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TrainRuntimeConfig)
