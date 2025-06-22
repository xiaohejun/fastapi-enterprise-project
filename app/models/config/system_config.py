from enum import Enum
from typing import Optional
from sqlmodel import Relationship
from app.models.base import ConfigBaseSQLModel


class SystemTypeEnum(str, Enum):
    NPU = "npu"
    GPU = "gpu"


class SystemConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "system_configs"

    type: SystemTypeEnum

    # 关系
    user: "User" = Relationship(back_populates="system_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="system_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )
