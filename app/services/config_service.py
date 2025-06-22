from uuid import UUID

from app.data_models import (InferenceRuntimeConfig, ModelConfig,
                             SystemConfig, TrainRuntimeConfig)
from app.repositories.config_repo import (InferenceRuntimeConfigBaseRepository,
                                          ModelConfigBaseRepository,
                                          SystemConfigBaseRepository,
                                          TrainRuntimeConfigBaseRepository)
from app.services.base.base import BaseService


class ConfigService:
    def __init__(self, session):
        self.model_config_repo = ModelConfigBaseRepository(session)
        self.system_config_repo = SystemConfigBaseRepository(session)
        self.inference_runtime_repo = InferenceRuntimeConfigBaseRepository(session)
        self.train_runtime_repo = TrainRuntimeConfigBaseRepository(session)

    # ModelConfig 服务方法
    async def create_model_config(self, config_data: dict) -> ModelConfig:
        return await self.model_config_repo.repo.create(ModelConfig(**config_data))

    async def get_model_config(self, config_id: UUID) -> ModelConfig | None:
        return await self.model_config_repo.repo.get(config_id)

    async def get_model_templates(self) -> list[ModelConfig]:
        return await self.model_config_repo.get_templates()

    # SystemConfig 服务方法
    async def create_system_config(self, config_data: dict) -> SystemConfig:
        return await self.system_config_repo.repo.create(SystemConfig(**config_data))

    async def get_system_config(self, config_id: UUID) -> SystemConfig | None:
        return await self.system_config_repo.repo.get(config_id)

    # 其他配置类型的方法类似...

    # 运行时配置服务
    async def create_inference_runtime(
        self, config_data: dict
    ) -> InferenceRuntimeConfig:
        return await self.inference_runtime_repo.repo.create(
            InferenceRuntimeConfig(**config_data)
        )

    async def create_train_runtime(self, config_data: dict) -> TrainRuntimeConfig:
        return await self.train_runtime_repo.repo.create(
            TrainRuntimeConfig(**config_data)
        )
