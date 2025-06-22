from datetime import datetime
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.user import RoleEnum
from app.schemas.base import BaseCreateSchema, BasePublicSchema


class UserCreateSchema(BaseCreateSchema):
    """用户创建 Schema"""
    username: str = Field(max_length=50, description="用户名（唯一）")
    password: str = Field(description="用户密码（明文，后端会哈希存储）")
    is_active: bool = Field(default=True, description="账户是否激活")
    role: RoleEnum = Field(default=RoleEnum.USER, description="用户角色")

    @staticmethod
    def _process_special_fields(data: dict[str, Any]):
        data["password_hash"] = data.pop("password")
        return data


class UserPublicSchema(BasePublicSchema):
    """用户公共信息 Schema（返回给前端）"""
    id: UUID  # UUID 会自动转为字符串
    username: str
    is_active: bool
    role: RoleEnum
    created_at: datetime
    updated_at: Optional[datetime]

    # class Config:
    #     orm_mode = True  # 支持从 ORM 对象转换


class UserUpdate(BaseModel):
    """用户信息更新 Schema"""
    is_active: Optional[bool] = Field(description="可选更新：账户激活状态")
    role: Optional[RoleEnum] = Field(description="可选更新：用户角色")
