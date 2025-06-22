from typing import Optional
from sqlmodel import Relationship
from app.models.base.sim_task_base import SimTaskBaseSQLModel


class InferenceSimTask(SimTaskBaseSQLModel, table=True):
    __tablename__ = "inference_sim_tasks"

    # # 关系 - 使用字符串引用
    user: "User" = Relationship(back_populates="inference_sim_tasks")

    # 一对一关系：一个任务对应一个模型配置
    model_config: Optional["ModelConfig"] = Relationship(
        back_populates="task",
        # sa_relationship_kwargs={"uselist": False}
    )

    # model_config: "ModelConfig" = Relationship(back_populates="inference_task")
    # system_config: "SystemConfig" = Relationship(back_populates="inference_task")
    # runtime_config: "InferenceRuntimeConfig" = Relationship(back_populates="inference_task")
