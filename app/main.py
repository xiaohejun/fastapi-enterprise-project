import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import db
# from app.routers import configs, tasks, users
from app.api.v1 import users


async def lifespan(app: FastAPI):
    await db.create_tables()
    yield
    await db.close()

app = FastAPI(
    title="AI仿真平台API",
    description="企业级AI模型训练和推理仿真平台",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(users.router)
# app.include_router(configs.router)
# app.include_router(tasks.router)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=int(os.getenv("API_PORT")), reload=True, log_level="info"
    )
