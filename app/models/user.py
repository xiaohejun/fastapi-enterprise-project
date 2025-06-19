from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    """用户基本信息"""
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    """用户数据库模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field()

class UserCreate(UserBase):
    """创建用户的请求模型"""
    password: str

class UserRead(UserBase):
    """返回给客户端的用户模型"""
    id: int
