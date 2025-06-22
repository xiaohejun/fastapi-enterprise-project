import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy import text
# from sqlalchemy.orm import declarative_base

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# from app.models.base.base import Base
from app.models_bak import Base
# from app.models import *

# 声明式基类 - 所有模型将继承自此类
# Base = declarative_base()

class AsyncDatabase:
    def __init__(
        self,
        db_url: str,
        pool_size: int = 20,
        max_overflow: int = 10,
        pool_recycle: int = 3600
    ):
        """
        异步数据库连接池
        
        :param db_url: 数据库连接字符串
        :param pool_size: 连接池大小
        :param max_overflow: 允许超出连接池大小的连接数
        :param pool_recycle: 连接回收时间(秒)
        """
        self.db_url = db_url
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            future=True,  # 启用 SQLAlchemy 2.0 特性
            echo=False    # 设置为 True 可查看生成的 SQL
        )
        
        # 创建异步会话工厂
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )
        logger.info(f"Initialized async database connection pool for {db_url}")

    async def is_connected(self) -> bool:
        """检查数据库连接是否正常"""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {str(e)}")
            return False

    async def create_tables(self):
        """创建所有定义的数据表"""
        logger.info("Creating database tables...")
        async with self.engine.begin() as conn:
            # 使用 SQLAlchemy 的 Base.metadata
            logger.info(f"Base.metadata = {Base.metadata}")
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

    async def drop_tables(self):
        """删除所有定义的数据表（谨慎使用）"""
        logger.warning("Dropping all database tables...")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("All database tables dropped")

    async def close(self):
        """关闭数据库连接池"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection pool closed")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        获取请求级别的异步会话
        
        用法:
        async with db.get_session() as session:
            result = await session.execute(query)
            ...
        """
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Session operation failed: {str(e)}")
            raise
        finally:
            await session.close()

# 配置数据库连接
def get_database_url() -> str:
    """获取数据库连接 URL"""
    # 优先使用环境变量配置
    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]
    
    # 默认开发配置
    return "postgresql+asyncpg://app_user:app_password@127.0.0.1:5432/app_db"

# 创建全局数据库实例
db = AsyncDatabase(db_url=get_database_url())