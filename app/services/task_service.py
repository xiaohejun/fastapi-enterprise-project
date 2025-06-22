# from uuid import UUID

# from app.data_models import InferenceSimTask, SimTaskStatusEnum, TrainSimTask
# from app.repositories.task_repo import (InferenceTaskBaseRepository,
#                                         TrainTaskBaseRepository)
# from app.services.base import BaseService


# class TaskService:
#     def __init__(self, session):
#         self.inference_repo = InferenceTaskBaseRepository(session)
#         self.train_repo = TrainTaskBaseRepository(session)

#     async def create_inference_task(
#         self,
#         user_id: UUID,
#         name: str,
#         model_config_id: UUID,
#         system_config_id: UUID,
#         runtime_config_id: UUID,
#     ) -> InferenceSimTask:
#         task = InferenceSimTask(
#             user_id=user_id,
#             name=name,
#             model_config_id=model_config_id,
#             system_config_id=system_config_id,
#             runtime_config_id=runtime_config_id,
#             status=SimTaskStatusEnum.PENDING,
#         )
#         return await self.inference_repo.repo.create(task)

#     async def create_train_task(
#         self,
#         user_id: UUID,
#         name: str,
#         model_config_id: UUID,
#         system_config_id: UUID,
#         runtime_config_id: UUID,
#     ) -> TrainSimTask:
#         task = TrainSimTask(
#             user_id=user_id,
#             name=name,
#             model_config_id=model_config_id,
#             system_config_id=system_config_id,
#             runtime_config_id=runtime_config_id,
#             status=SimTaskStatusEnum.PENDING,
#         )
#         return await self.train_repo.repo.create(task)

#     async def update_task_status(
#         self, task_id: UUID, status: str, is_inference: bool = True
#     ) -> bool:
#         repo = self.inference_repo if is_inference else self.train_repo
#         task = await repo.update_status(task_id, status)
#         return task is not None

#     async def get_user_tasks(self, user_id: UUID) -> dict:
#         inference_tasks = await self.inference_repo.get_by_user(user_id)
#         train_tasks = await self.train_repo.get_by_user(user_id)
#         return {"inference_tasks": inference_tasks, "train_tasks": train_tasks}
