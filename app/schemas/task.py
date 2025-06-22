from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.base import SimTaskStatusEnum


class InferenceSimTaskCreate(BaseModel):
    """推理仿真任务创建 Schema"""
    user_id: str  # UUID 外键
    name: str = Field(max_length=100, description="任务名称（唯一）")
    model_config_id: str  # 模型配置外键
    system_config_id: str  # 系统配置外键
    runtime_config_id: str  # 运行时配置外键
    status: SimTaskStatusEnum = Field(default=SimTaskStatusEnum.PENDING, description="任务状态")
    result: Dict[str, Any] = Field(default={}, description="任务结果")


class InferenceSimTaskPublic(BaseModel):
    """推理仿真任务公共信息 Schema"""
    id: str
    user_id: str
    name: str
    model_config_id: str
    system_config_id: str
    runtime_config_id: str
    status: SimTaskStatusEnum
    result: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class InferenceSimTaskUpdate(BaseModel):
    """推理仿真任务更新 Schema"""
    status: Optional[SimTaskStatusEnum] = Field(description="可选更新：任务状态")
    result: Optional[Dict[str, Any]] = Field(description="可选更新：任务结果")
