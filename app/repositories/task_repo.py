from typing import Type, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.data_models import InferenceSimTask, TrainSimTask

from .base import BaseRepository

TaskType = Union[InferenceSimTask, TrainSimTask]


class TaskBaseRepository:
    def __init__(self, session: AsyncSession, model: Type[TaskType]):
        self.repo = BaseRepository(session, model)

    async def get_by_user(self, user_id: UUID) -> list[TaskType]:
        result = await self.repo.session.execute(
            select(self.repo.model).where(self.repo.model.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_status(self, status: str) -> list[TaskType]:
        result = await self.repo.session.execute(
            select(self.repo.model).where(self.repo.model.status == status)
        )
        return result.scalars().all()

    async def update_status(self, task_id: UUID, status: str) -> TaskType | None:
        return await self.repo.update(task_id, {"status": status})


class InferenceTaskBaseRepository(TaskBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InferenceSimTask)


class TrainTaskBaseRepository(TaskBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TrainSimTask)
