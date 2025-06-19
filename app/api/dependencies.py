# from typing import AsyncGenerator

# from fastapi import Depends
# from sqlmodel.ext.asyncio.session import AsyncSession

# from app.db.session import db_session_manager
# from app.repositories.user import UserRepository
# from app.services.user import UserService


# class DependencyProvider:
#     """依赖提供器，负责提供各种依赖项。"""
#     @staticmethod
#     async def get_session() -> AsyncSession:
#         """获取请求级别的会话依赖。"""
#         async with db_session_manager.get_session() as session:
#             yield session

#     @staticmethod
#     async def get_user_repository(
#         session_generator: AsyncSession = Depends(get_session)
#     ) -> UserRepository:
#         """获取用户仓储依赖。"""
#         # 正确获取 AsyncSession 实例
#         session = await session_generator.__anext__()
#         return UserRepository(session)

#     @staticmethod
#     async def get_user_service(
#         user_repository: UserRepository = Depends(get_user_repository)
#     ) -> UserService:
#         """获取用户服务依赖。"""
#         return UserService(user_repository)

from typing import AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import db_session_manager
from app.repositories.user import UserRepository
from app.services.user import UserService


async def get_user_repository(
    session: AsyncSession = Depends(db_session_manager.get_session)
) -> AsyncGenerator[UserRepository, None]:
    """获取用户仓储依赖"""
    yield UserRepository(session)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AsyncGenerator[UserService, None]:
    """获取用户服务依赖"""
    yield UserService(user_repository)
