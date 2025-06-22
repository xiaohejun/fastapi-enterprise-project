from enum import Enum
from typing import List
from sqlmodel import Field, Relationship
from app.models.base import BaseSQLModel


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseSQLModel, table=True):
    __tablename__ = "users"

    username: str = Field(
        unique=True,
        index=True,
        max_length=50
    )
    password_hash: str
    is_active: bool = Field(default=True)
    role: RoleEnum = Field(default=RoleEnum.USER)

    # User 和 Config 的对应关系 (一对多)
    model_configs: List["ModelConfig"] = Relationship(back_populates="user")
    system_configs: List["SystemConfig"] = Relationship(back_populates="user")
    inference_runtime_configs: List["InferenceRuntimeConfig"] = Relationship(
        back_populates="user"
    )
    # train_runtime_configs: List["TrainRuntimeConfig"] = Relationship(
    #     back_populates="user"
    # )

    # # User 和 Task 的对应关 (一对多)
    # inference_sim_tasks: List["InferenceSimTask"] = Relationship(
    #     back_populates="user"
    # )
