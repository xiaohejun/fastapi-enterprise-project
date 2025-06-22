from os import path
from fastapi import APIRouter, Depends, HTTPException, status

# from app.api.dependencies import DependencyProvider
from app.api.dependencies import get_user_service
from app.services.user_service import UserService
from app.schemas.user import UserCreateSchema, UserPublicSchema

router = APIRouter(prefix="/users", tags=["users"])


class UserEndpoints:
    """用户相关的 API 端点。"""

    @staticmethod
    @router.post("/", response_model=UserPublicSchema, status_code=status.HTTP_201_CREATED)
    async def create_user(
        user: UserCreateSchema,
        # user_service: UserService = Depends(DependencyProvider.get_user_service),
        user_service: UserService = Depends(get_user_service)
    ):
        """创建新用户。"""
        try:
            print("==== Creating user:", user)
            ret = await user_service.create(user)
            print("==== User created successfully:", ret)
            return ret
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # @staticmethod
    # @router.get("/{user_id}", response_model=UserRead)
    # async def get_user(
    #     user_id: int,
    #     # user_service: UserService = Depends(DependencyProvider.get_user_service)
    #     user_service: UserService = Depends(get_user_service),
    # ):
    #     """获取用户信息。"""
    #     user = await user_service.get_user(user_id)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
    #         )
    #     return user
