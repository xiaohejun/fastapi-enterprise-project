from contextvars import ContextVar
from typing import AsyncGenerator, Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.config import settings


class DatabaseSessionManager:
    """数据库会话管理器，负责创建引擎和管理请求级别的会话。"""

    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            future=True
        )
        self._request_session: ContextVar[Optional[AsyncSession]] = ContextVar(
            "_request_session", default=None
        )

    async def init_db(self):
        """初始化数据库，生产环境建议使用 Alembic 进行迁移。"""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取请求级别的会话。"""
        session = AsyncSession(self.engine)
        token = self._request_session.set(session)
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            self._request_session.reset(token)

    def get_current_session(self) -> AsyncSession:
        """获取当前上下文中的会话。"""
        session = self._request_session.get()
        if session is None:
            raise RuntimeError("没有可用的会话")
        return session


# 初始化数据库会话管理器
db_session_manager = DatabaseSessionManager()
