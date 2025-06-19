from typing import Optional
from sqlmodel import select

from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """用户仓储实现"""
    
    def __init__(self, session):
        super().__init__(User, session)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        statement = select(User).where(User.username == username)
        results = await self.session.execute(statement)
        return results.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        statement = select(User).where(User.email == email)
        results = await self.session.execute(statement)
        return results.scalar_one_or_none()
