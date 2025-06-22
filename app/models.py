from datetime import datetime, timezone
import json
from typing import Any, Dict, Optional, List
from sqlmodel import Column, SQLModel, Field, Relationship
from uuid import UUID, uuid4
from sqlalchemy import JSON, table
from pydantic import Json, model_validator
import enum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB

# ------------------------
# 枚举定义
# ------------------------


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class SimTaskStatusEnum(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SystemTypeEnum(str, enum.Enum):
    NPU = "npu"
    GPU = "gpu"

# ------------------------
# 基础模型
# ------------------------


class BaseModel(SQLModel, table=False):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    # 修改点：使用 Field 的标准参数定义时间字段
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )

# ------------------------
# 用户模型
# ------------------------


class User(BaseModel, table=True):
    __tablename__ = "users"

    username: str = Field(
        unique=True,
        index=True,
        max_length=50
    )
    password_hash: str
    is_active: bool = Field(default=True)
    role: RoleEnum = Field(default=RoleEnum.USER)

    # 关系 (一对多)
    model_configs: List["ModelConfig"] = Relationship(back_populates="user")
    system_configs: List["SystemConfig"] = Relationship(back_populates="user")
    inference_runtime_configs: List["InferenceRuntimeConfig"] = Relationship(
        back_populates="user"
    )
    train_runtime_configs: List["TrainRuntimeConfig"] = Relationship(
        back_populates="user"
    )
    # inference_sim_tasks: List["InferenceSimTask"] = Relationship(
    #     back_populates="user"
    # )
    # train_sim_tasks: List["TrainSimTask"] = Relationship(
    #     back_populates="user"
    # )

# ------------------------
# 配置模型基类
# ------------------------


class ConfigBaseSQLModel(BaseModel, table=False):
    name: str = Field(
        index=True,
        max_length=100,
        unique=True
    )

    params: Dict[str, Any] = Field(
        default={},
        sa_type=JSONB,  # 指定为 PostgreSQL 的 JSONB 类型
        sa_column_kwargs={"index": False},  # 可选：添加索引参数
        description="存储 JSONB 数据的公共字段"
    )
    # params: Json[Dict[str, Any]] = Field(default_factory=dict, nullable=False)

    is_template: bool = Field(
        default=True,
        description="标识是否为模板配置"
    )

    # 外键
    user_id: UUID = Field(
        foreign_key="users.id"
    )

    @model_validator(mode='before')
    def validate_params(cls, values):
        params = values.get('params', {})
        if params is None:
            params = {}
        return {**values, 'params': params}


# ------------------------
# 模型配置
# ------------------------


class ModelConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "model_configs"

    type: str = Field(max_length=50)
    # params: dict = Field(sa_column=Column(JSON))  # TODO: 这个字段放基类会有问题

    # 关系
    user: User = Relationship(back_populates="model_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="model_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )
    # train_task: Optional["TrainSimTask"] = Relationship(
    #     back_populates="model_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )

# ------------------------
# 系统配置
# ------------------------


class SystemConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "system_configs"

    type: SystemTypeEnum
    # params: dict = Field(sa_column=Column(JSON))
    # params: dict = Field(sa_column=Column(JSON))

    # 外键
    # user_id: UUID = Field(
    #     foreign_key="users.id"
    # )

    # 关系
    user: User = Relationship(back_populates="system_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="system_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )
    # train_task: Optional["TrainSimTask"] = Relationship(
    #     back_populates="system_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )

# ------------------------
# 推理运行时配置
# ------------------------


class InferenceRuntimeConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "inference_runtime_configs"

    # params: dict = Field(sa_column=Column(JSON))

    # 外键
    # user_id: UUID = Field(
    #     foreign_key="users.id"
    # )

    # 关系
    user: User = Relationship(back_populates="inference_runtime_configs")

    # 一对一关系 (可空)
    # inference_task: Optional["InferenceSimTask"] = Relationship(
    #     back_populates="runtime_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )

# ------------------------
# 训练运行时配置
# ------------------------


class TrainRuntimeConfig(ConfigBaseSQLModel, table=True):
    __tablename__ = "train_runtime_configs"

    # params: dict = Field(sa_column=Column(JSON))

    # 外键
    # user_id: UUID = Field(
    #     foreign_key="users.id"
    # )

    # 关系
    user: User = Relationship(back_populates="train_runtime_configs")

    # 一对一关系 (可空)
    # train_task: Optional["TrainSimTask"] = Relationship(
    #     back_populates="runtime_config",
    #     sa_relationship_kwargs={"uselist": False}
    # )

# ------------------------
# 任务基类
# ------------------------


class SimTaskBaseSQLModel(BaseModel):
    # 仅作为字段容器，不再继承SQLModel
    name: str = Field(index=True, unique=True, max_length=100)
    status: SimTaskStatusEnum = Field(default=SimTaskStatusEnum.PENDING)

    # 外键
    user_id: UUID = Field(foreign_key="users.id")
    # 表参数作为类方法
    # @declared_attr
    # def __table_args__(cls):
    #     return (
    #         sa.UniqueConstraint('user_id', 'name', name=f'uq_{cls.__tablename__}_user_name'),
    #     )

# ------------------------
# 推理仿真任务
# ------------------------


class InferenceSimTask(SimTaskBaseSQLModel, table=True):
    __tablename__ = "inference_sim_tasks"

    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # TODO: 这个字段放基类会有问题

    # # 外键
    # model_config_id: UUID = Field(foreign_key="model_configs.id", unique=True)
    # system_config_id: UUID = Field(foreign_key="system_configs.id", unique=True)
    # runtime_config_id: UUID = Field(foreign_key="inference_runtime_configs.id", unique=True)

    # # 关系 - 使用字符串引用
    # user: "User" = Relationship(back_populates="inference_sim_tasks")
    # model_config: "ModelConfig" = Relationship(back_populates="inference_task")
    # system_config: "SystemConfig" = Relationship(back_populates="inference_task")
    # runtime_config: "InferenceRuntimeConfig" = Relationship(back_populates="inference_task")

# ------------------------
# 训练仿真任务
# ------------------------


# class TrainSimTask(TaskBase, BaseModel, table=True):
#     __tablename__ = "train_sim_tasks"

#     # 外键 (带唯一约束实现一对一关系)
#     user_id: UUID = Field(
#         foreign_key="users.id"
#     )
#     model_config_id: UUID = Field(
#         foreign_key="model_configs.id",
#         unique=True
#     )
#     system_config_id: UUID = Field(
#         foreign_key="system_configs.id",
#         unique=True
#     )
#     runtime_config_id: UUID = Field(
#         foreign_key="train_runtime_configs.id",
#         unique=True
#     )

#     # 关系
#     user: User = Relationship(back_populates="train_sim_tasks")

#     # 一对一关系
#     model_config: ModelConfig = Relationship(
#         back_populates="train_task"
#     )
#     system_config: SystemConfig = Relationship(
#         back_populates="train_task"
#     )
#     runtime_config: TrainRuntimeConfig = Relationship(
#         back_populates="train_task"
#     )
