from enum import Enum
from typing import Any, Dict, TypeVar
from uuid import UUID

from sqlmodel import Field
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base.base import BaseSQLModel


class SimTaskStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SimTaskBaseSQLModel(BaseSQLModel):
    """任务基础模型"""
    # 外键
    user_id: UUID = Field(foreign_key="users.id")

    name: str = Field(index=True, unique=True, max_length=100)
    status: SimTaskStatusEnum = Field(default=SimTaskStatusEnum.PENDING)
    result: Dict[str, Any] = Field(
        default={},
        sa_type=JSONB,
        description="存储结果"
    )


TSimTaskBaseSQLModel = TypeVar("TSimTaskBaseSQLModel", bound=SimTaskBaseSQLModel)
