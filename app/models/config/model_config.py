from typing import Optional
from sqlmodel import Field, Relationship
from app.models.base import ConfigBaseSQLModel


class ModelConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "model_configs"

    type: str = Field(max_length=50)

    # 关系
    user: "User" = Relationship(back_populates="model_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="model_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )
