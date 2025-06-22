from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.dependencies import get_config_service
from app.schemas.config import ModelConfigCreate, ModelConfigResponse
from app.services.config_service import ConfigService

router = APIRouter(prefix="/configs", tags=["configurations"])


@router.post(
    "/model", response_model=ModelConfigResponse, status_code=status.HTTP_201_CREATED
)
async def create_model_config(
    config_data: ModelConfigCreate,
    config_service: ConfigService = Depends(get_config_service),
):
    try:
        config = await config_service.create_model_config(config_data.dict())
        return config
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/model/{config_id}", response_model=ModelConfigResponse)
async def get_model_config(
    config_id: UUID = Path(..., description="模型配置ID"),
    config_service: ConfigService = Depends(get_config_service),
):
    config = await config_service.get_model_config(config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model configuration not found",
        )
    return config


@router.get("/model/templates", response_model=list[ModelConfigResponse])
async def get_model_templates(
    config_service: ConfigService = Depends(get_config_service),
):
    templates = await config_service.get_model_templates()
    return templates


# 其他配置类型的路由类似...
