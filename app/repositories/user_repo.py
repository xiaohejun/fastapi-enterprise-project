from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.repositories.base.crud import CRUDBaseRepository


class UserRepository(CRUDBaseRepository[User]):
    sql_model_cls = User

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    # async def get_by_username(self, username: str) -> User | None:
    #     result = await self.session.execute(
    #         select(User).where(User.username == username)
    #     )
    #     return result.scalars().first()

    # async def get_active_users(self) -> list[User]:
    #     result = await self.session.execute(select(User).where(User.is_active == True))
    #     return result.scalars().all()
