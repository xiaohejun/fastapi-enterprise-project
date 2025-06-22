from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    database_url: str = Field(..., env="DATABASE_URL")
    debug: bool = Field(False, env="DEBUG")
    app_name: str = Field("FastAPI企业级应用", env="APP_NAME")

    class Config:
        env_file = ".env"


settings = Settings()
