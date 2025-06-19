from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.config import settings
from app.db.session import db_session_manager


class FastAPIApp:
    """FastAPI 应用初始化和配置类。"""

    def __init__(self):
        self.app = FastAPI(
            title=settings.app_name,
            debug=settings.debug
        )
        self._setup_cors()
        self._register_routes()
        self._setup_startup_event()

    def _setup_cors(self):
        """设置 CORS 中间件。"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self):
        """注册 API 路由。"""
        self.app.include_router(api_router, prefix="/api/v1")

    def _setup_startup_event(self):
        """设置应用启动事件。"""
        @self.app.on_event("startup")
        async def on_startup():
            await db_session_manager.init_db()


# 初始化 FastAPI 应用
app = FastAPIApp().app
