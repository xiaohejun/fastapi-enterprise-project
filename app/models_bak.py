from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from uuid import uuid4, UUID
from enum import Enum
from sqlalchemy import Column, TIMESTAMP, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class BaseMixin(Base):
    """所有模型共享的基础字段"""
    __abstract__ = True
    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        nullable=True
    )

class ConfigBase(BaseMixin):
    """配置模型基类"""
    __abstract__ = True
    
    name = Column(
        String(100),
        index=True,
        unique=True,
        nullable=False
    )
    is_template = Column(
        Boolean,
        default=True,
        comment="标识是否为模板配置,没有任务关联的配置为模板配置"
    )
    params = Column(
        JSONB,
        default={},
        comment="配置参数"
    )

class ModelConfig(ConfigBase):
    """模型配置表"""
    __tablename__ = "model_configs"
    
    type = Column(String(50), nullable=False)
    
    # 与推理任务的一对一关系
    inference_task = relationship(
        "InferenceSimTask", 
        back_populates="model_config",
        uselist=False
    )

class SystemConfig(ConfigBase):
    __tablename__ = "system_configs"

    type = Column(
        String(10),
        index=True,
        nullable=False
    )

    # 关系
    # user: "User" = Relationship(back_populates="system_configs")
    inference_task = relationship(
        "InferenceSimTask", 
        back_populates="system_config",
        uselist=False
    )

class InferenceRuntimeConfig(ConfigBase):
    __tablename__ = "inference_runtime_configs"

    inference_task = relationship(
        "InferenceSimTask", 
        back_populates="runtime_config",
        uselist=False
    )

class SimTaskStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SimTaskBase(BaseMixin):
    """任务基础模型"""
    __abstract__ = True
    
    name = Column(
        String(100),
        index=True,
        unique=True,
        nullable=False
    )
    status = Column(
        String(20),
        default=SimTaskStatusEnum.PENDING.value,
        nullable=False
    )
    result = Column(
        JSONB,
        default={},
        comment="存储结果"
    )

class InferenceSimTask(SimTaskBase):
    """推理模拟任务表"""
    __tablename__ = "inference_sim_tasks"
    
    # 外键指向模型配置
    model_config_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("model_configs.id", ondelete="SET NULL"),
        index=True
    )
    system_config_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("system_configs.id", ondelete="SET NULL"),
        index=True
    )
    runtime_config_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("inference_runtime_configs.id", ondelete="SET NULL"),
        index=True
    )
    
    # 与模型配置的一对一关系
    model_config = relationship(
        "ModelConfig", 
        back_populates="inference_task",
        foreign_keys=[model_config_id]
    )
    system_config = relationship(
        "SystemConfig", 
        back_populates="inference_task",
        foreign_keys=[system_config_id]
    )
    runtime_config = relationship(
        "InferenceRuntimeConfig", 
        back_populates="inference_task",
        foreign_keys=[system_config_id]
    )