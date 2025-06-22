from typing import Any, Dict, TypeVar
from uuid import UUID

from sqlmodel import Field
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base.base import BaseSQLModel


class ConfigBaseSQLModel(BaseSQLModel, table=False):
    """配置基础模型"""
    # 外键
    user_id: UUID = Field(
        foreign_key="users.id",
        description="用户外键"
    )

    # 字段
    name: str = Field(
        index=True,
        max_length=100,
        unique=True
    )

    is_template: bool = Field(
        default=True,
        description="标识是否为模板配置,没有任务关联的配置为模板配置"
    )

    params: Dict[str, Any] = Field(
        default={},
        sa_type=JSONB,  # 指定为 PostgreSQL 的 JSONB 类型
        description="配置参数"
    )


TConfigBaseSQLModel = TypeVar("TConfigBaseSQLModel", bound=ConfigBaseSQLModel)
