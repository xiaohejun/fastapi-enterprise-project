from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserInDB, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.create_user(
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}/password", response_model=UserInDB)
async def update_password(
    user_id: UUID,
    new_password: str,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.update_password(user_id, new_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    success = await user_service.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return
