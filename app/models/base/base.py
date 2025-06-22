from datetime import datetime, timezone
from typing import Optional, TypeVar
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from sqlalchemy import TIMESTAMP


class BaseSQLModel(SQLModel):
    """基础模型,所有表都应该有这些字段"""
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    # 修改点：使用 Field 的标准参数定义时间字段
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True),
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )


# 泛型类型变量，限定必须是BaseSQLModel或其子类
TBaseSQLModel = TypeVar("TSQLModel", bound=BaseSQLModel)
