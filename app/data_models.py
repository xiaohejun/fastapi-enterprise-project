from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Column, SQLModel, Field, Relationship
from uuid import UUID, uuid4
from sqlalchemy import JSON
import enum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from sqlalchemy import DateTime

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


class BaseModel(SQLModel):
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


class ConfigBase(SQLModel):
    name: str = Field(
        index=True,
        max_length=100,
        sa_column_kwargs={"unique": True}  # 全局唯一名称
    )
    is_template: bool = Field(
        default=True,
        description="标识是否为模板配置"
    )

# ------------------------
# 模型配置
# ------------------------


class ModelConfig(ConfigBase, BaseModel, table=True):
    __tablename__ = "model_configs"

    type: str = Field(max_length=50)
    params: dict = Field(sa_column=Column(JSON))

    # 外键
    user_id: UUID = Field(
        foreign_key="users.id"
    )

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


class SystemConfig(ConfigBase, BaseModel, table=True):
    __tablename__ = "system_configs"

    type: SystemTypeEnum
    params: dict = Field(sa_column=Column(JSON))

    # 外键
    user_id: UUID = Field(
        foreign_key="users.id"
    )

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


class InferenceRuntimeConfig(ConfigBase, BaseModel, table=True):
    __tablename__ = "inference_runtime_configs"

    params: dict = Field(sa_column=Column(JSON))

    # 外键
    user_id: UUID = Field(
        foreign_key="users.id"
    )

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


class TrainRuntimeConfig(ConfigBase, BaseModel, table=True):
    __tablename__ = "train_runtime_configs"

    params: dict = Field(sa_column=Column(JSON))

    # 外键
    user_id: UUID = Field(
        foreign_key="users.id"
    )

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


class TaskBase:
    # 仅作为字段容器，不再继承SQLModel
    name: str = Field(index=True, max_length=100)
    status: SimTaskStatusEnum = Field(default=SimTaskStatusEnum.PENDING)
    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # 表参数作为类方法
    # @declared_attr
    # def __table_args__(cls):
    #     return (
    #         sa.UniqueConstraint('user_id', 'name', name=f'uq_{cls.__tablename__}_user_name'),
    #     )

# ------------------------
# 推理仿真任务
# ------------------------


# class InferenceSimTask(BaseModel, table=True):
#     __tablename__ = "inference_sim_tasks"

#     # 外键
#     user_id: UUID = Field(foreign_key="users.id")
#     model_config_id: UUID = Field(foreign_key="model_configs.id", unique=True)
#     system_config_id: UUID = Field(foreign_key="system_configs.id", unique=True)
#     runtime_config_id: UUID = Field(foreign_key="inference_runtime_configs.id", unique=True)

#     # 关系 - 使用字符串引用
#     user: "User" = Relationship(back_populates="inference_sim_tasks")
#     model_config: "ModelConfig" = Relationship(back_populates="inference_task")
#     system_config: "SystemConfig" = Relationship(back_populates="inference_task")
#     runtime_config: "InferenceRuntimeConfig" = Relationship(back_populates="inference_task")

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
