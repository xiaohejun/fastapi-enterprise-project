import bcrypt
from typing import Optional

from app.models.user import User, UserCreate
from app.repositories.user import UserRepository
from app.services.base import BaseService

class UserService(BaseService):
    """用户服务实现"""
    
    def __init__(self, user_repository: UserRepository):
        """初始化用户服务，注入用户仓储"""
        super().__init__(user_repository=user_repository)
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """获取用户信息"""
        return await self.user_repository.get(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await self.user_repository.get_by_username(username)
    
    async def create_user(self, user_create: UserCreate) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        if await self.user_repository.get_by_username(user_create.username):
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if await self.user_repository.get_by_email(user_create.email):
            raise ValueError("邮箱已存在")
        
        # 加密密码
        password_hash = bcrypt.hashpw(
            user_create.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # 创建用户对象
        user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=password_hash
        )
        
        # 保存到数据库
        return await self.user_repository.create(user)
