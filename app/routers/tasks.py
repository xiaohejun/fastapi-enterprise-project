from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.dependencies import get_task_service
from app.schemas.task import InferenceTaskCreate, InferenceTaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/inference",
    response_model=InferenceTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inference_task(
    task_data: InferenceTaskCreate,
    task_service: TaskService = Depends(get_task_service),
):
    try:
        task = await task_service.create_inference_task(
            user_id=task_data.user_id,
            name=task_data.name,
            model_config_id=task_data.model_config_id,
            system_config_id=task_data.system_config_id,
            runtime_config_id=task_data.runtime_config_id,
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/inference/{task_id}/status", response_model=InferenceTaskResponse)
async def update_inference_task_status(
    task_id: UUID = Path(..., description="推理任务ID"),
    status: str = "running",
    task_service: TaskService = Depends(get_task_service),
):
    task = await task_service.update_task_status(task_id, status, is_inference=True)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inference task not found"
        )
    return task


@router.get("/user/{user_id}", response_model=dict)
async def get_user_tasks(
    user_id: UUID, task_service: TaskService = Depends(get_task_service)
):
    tasks = await task_service.get_user_tasks(user_id)
    return tasks
