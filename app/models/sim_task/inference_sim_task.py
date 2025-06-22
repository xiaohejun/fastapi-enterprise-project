from typing import Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from app.models.base.sim_task_base import SimTaskBaseSQLModel


class InferenceSimTask(SimTaskBaseSQLModel, table=True):
    __tablename__ = "inference_sim_tasks"

    # 外键
    model_config_id: UUID = Field(foreign_key="model_configs.id")
    system_config_id: UUID = Field(foreign_key="system_configs.id")
    runtime_config_id: UUID = Field(foreign_key="inference_runtime_configs.id")

    # 关系 - 使用字符串引用
    user: "User" = Relationship(back_populates="inference_sim_tasks")
    model_config: "ModelConfig" = Relationship(back_populates="inference_task")
    system_config: "SystemConfig" = Relationship(back_populates="inference_task")
    runtime_config: "InferenceRuntimeConfig" = Relationship(back_populates="inference_task")
