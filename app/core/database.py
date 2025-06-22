from contextlib import asynccontextmanager
import logging
import os
from typing import AsyncGenerator

from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(
        self,
        db_url: str,
    ):
        self.db_url = db_url
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
            # 企业级项目建议添加连接池配置
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )
        logger.info(f"Initialized async database connection pool for {db_url}")

    async def is_connected(self):
        """检查数据库连接是否正常"""
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    async def create_tables(self):
        """创建所有定义的数据表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created")

    async def drop_tables(self):
        """删除所有定义的数据表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        logger.info("Database tables dropped")  # 修复：拼写错误 info -> info

    async def close(self):
        """关闭数据库连接池"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection pool closed")

    # @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取请求级别的会话。"""
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Error during session operation: {str(e)}")
            raise  # 修复：使用 raise 保留原始异常堆栈
        finally:
            await session.close()


db = AsyncDatabase(os.getenv("DATABASE_URL"))
