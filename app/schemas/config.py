from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import SystemTypeEnum
from app.models import InferenceSimTask  # 用于关系类型提示


# ---------------------- 通用配置基类（可复用） ----------------------
class ConfigCreateBase(BaseModel):
    """配置创建基类（所有配置类共享）"""
    user_id: str  # UUID 外键
    name: str = Field(max_length=100, description="配置名称（唯一）")
    is_template: bool = Field(default=True, description="是否为模板配置")
    params: Dict[str, Any] = Field(default={}, description="配置参数")


class ConfigPublicBase(BaseModel):
    """配置公共信息基类（所有配置类共享）"""
    id: str
    user_id: str
    name: str
    is_template: bool
    params: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ConfigUpdateBase(BaseModel):
    """配置更新基类（所有配置类共享）"""
    name: Optional[str] = Field(max_length=100, description="可选更新：配置名称")
    is_template: Optional[bool] = Field(description="可选更新：是否为模板配置")
    params: Optional[Dict[str, Any]] = Field(description="可选更新：配置参数")


# ---------------------- 具体配置类 Schema ----------------------
class ModelConfigCreate(ConfigCreateBase):
    """模型配置创建 Schema"""
    type: str = Field(max_length=50, description="模型类型（如 'resnet'）")


class ModelConfigPublic(ConfigPublicBase):
    """模型配置公共信息 Schema"""
    type: str


class ModelConfigUpdate(ConfigUpdateBase):
    """模型配置更新 Schema"""
    type: Optional[str] = Field(max_length=50, description="可选更新：模型类型")


class SystemConfigCreate(ConfigCreateBase):
    """系统配置创建 Schema"""
    type: SystemTypeEnum = Field(description="系统类型（NPU/GPU）")


class SystemConfigPublic(ConfigPublicBase):
    """系统配置公共信息 Schema"""
    type: SystemTypeEnum


class SystemConfigUpdate(ConfigUpdateBase):
    """系统配置更新 Schema"""
    type: Optional[SystemTypeEnum] = Field(description="可选更新：系统类型")


class InferenceRuntimeConfigCreate(ConfigCreateBase):
    """推理运行时配置创建 Schema（无额外字段）"""
    pass


class InferenceRuntimeConfigPublic(ConfigPublicBase):
    """推理运行时配置公共信息 Schema"""
    pass


class InferenceRuntimeConfigUpdate(ConfigUpdateBase):
    """推理运行时配置更新 Schema"""
    pass
