from uuid import UUID

from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreateSchema, UserPublicSchema
from app.services.base.crud import CRUDBaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(CRUDBaseService[User, UserCreateSchema, UserPublicSchema]):
    sqlmodel_cls = User
    create_schema_cls = UserCreateSchema
    public_schema_cls = UserPublicSchema

    def __init__(self, session):
        super().__init__(session)

    async def create(self, create_data: UserCreateSchema) -> UserPublicSchema:
        # 将密码加密
        hashed_password = pwd_context.hash(create_data.password)
        create_data.password = hashed_password
        return await super().create(create_data)

    # async def authenticate_user(self, username: str, password: str) -> User | None:
    #     user = await self.BaseRepository.get_by_username(username)
    #     if not user or not pwd_context.verify(password, user.password_hash):
    #         return None
    #     return user

    # async def update_password(self, user_id: UUID, new_password: str) -> User | None:
    #     hashed_password = pwd_context.hash(new_password)
    #     return await self.BaseRepository.update(user_id, {"password_hash": hashed_password})
