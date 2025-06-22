from typing import Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from app.models.base.config_base import ConfigBaseSQLModel
# from app.models.sim_task.inference_sim_task import InferenceSimTask


class ModelConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "model_configs"

    type: str = Field(max_length=50)

    # 关系
    user: "User" = Relationship(back_populates="model_configs")

    # 一对一关系 (可空)
    # 修改点2：简化外键定义
    task_id: Optional[UUID] = Field(
        default=None, 
        foreign_key="inference_sim_tasks.id",
        unique=True
    )
    
    # 修改点3：使用字符串引用
    task: Optional["InferenceSimTask"] = Relationship(back_populates="model_config")
