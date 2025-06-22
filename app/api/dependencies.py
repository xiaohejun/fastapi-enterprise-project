from typing import AsyncGenerator

from fastapi import Depends
# from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.session import db_session_manager
# from app.repositories.user import UserRepository
# from app.services.user import UserService
from app.core.database import db
from app.services.user_service import UserService


# async def get_user_BaseRepository(
#     session: AsyncSession = Depends(db_session_manager.get_session),
# ) -> AsyncGenerator[UserRepository, None]:
#     """获取用户仓储依赖"""
#     yield UserRepository(session)


async def get_user_service(session: AsyncSession = Depends(db.get_session)) -> AsyncGenerator[UserService, None]:
    """获取用户服务依赖"""
    yield UserService(session)


# class DependencyProvider:
#     @staticmethod
#     async def get_user_BaseRepository(
#         session: AsyncSession = Depends(db_session_manager.get_session),
#     ) -> AsyncGenerator[UserRepository, None]:
#         yield UserRepository(session)

#     @staticmethod
#     async def get_user_service(
#         user_BaseRepository: UserRepository = Depends(get_user_BaseRepository),
#     ) -> AsyncGenerator[UserService, None]:
#         """获取用户服务依赖。"""
#         yield UserService(user_BaseRepository)
