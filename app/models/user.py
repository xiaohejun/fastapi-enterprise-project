from enum import Enum
from typing import List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from app.models.base.base import BaseSQLModel


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
    model_configs: list["ModelConfig"] = Relationship(back_populates="user")
    # system_configs: list["SystemConfig"] = Relationship(back_populates="user")
    # inference_runtime_configs: list["InferenceRuntimeConfig"] = Relationship(back_populates="user")
    # train_runtime_configs: List["TrainRuntimeConfig"] = Relationship(
    #     back_populates="user"
    # )

    # # User 和 Task 的对应关 (一对多)
    inference_sim_tasks: List["InferenceSimTask"] = Relationship(
        back_populates="user"
    )

#     icloud_account_id: Optional[UUID] = Field(default=None, foreign_key="icloudaccount.id")
#     icloud_account: Optional["ICloudAccount"] = Relationship(back_populates="user")


# class ICloudAccount(BaseSQLModel, table=True):
#     user_name: str
#     user: Optional["User"] = Relationship(
#         sa_relationship_kwargs={'uselist': False},
#         back_populates="icloud_account"
#     )
