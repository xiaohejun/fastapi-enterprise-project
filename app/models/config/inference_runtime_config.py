from typing import Optional
from sqlmodel import Relationship
from app.models.base import ConfigBaseSQLModel


class InferenceRuntimeConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "inference_runtime_configs"

    # 关系
    user: "User" = Relationship(back_populates="inference_runtime_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="runtime_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )
