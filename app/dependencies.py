# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
# from app.repositories import (InferenceRuntimeConfigBaseRepository,
#                               InferenceTaskBaseRepository, ModelConfigBaseRepository,
#                               SystemConfigBaseRepository,
#                               TrainRuntimeConfigBaseRepository,
#                               TrainTaskBaseRepository, UserRepository)
# from app.services import ConfigService, TaskService, UserService


# async def get_user_service(
#     session: AsyncSession = Depends(get_async_session),
# ) -> UserService:
#     return UserService(session)


# async def get_config_service(
#     session: AsyncSession = Depends(get_async_session),
# ) -> ConfigService:
#     return ConfigService(session)


# async def get_task_service(
#     session: AsyncSession = Depends(get_async_session),
# ) -> TaskService:
#     return TaskService(session)
