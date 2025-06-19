from typing import Generic, TypeVar, List, Optional
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    """基础仓储类，提供通用的数据访问方法"""
    
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get(self, id: int) -> Optional[ModelType]:
        """根据ID获取单个对象"""
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        return results.scalar_one_or_none()
    
    async def list(self) -> List[ModelType]:
        """获取所有对象列表"""
        statement = select(self.model)
        results = await self.session.execute(statement)
        return results.scalars().all()
    
    async def create(self, obj: ModelType) -> ModelType:
        """创建新对象"""
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def update(self, obj: ModelType) -> ModelType:
        """更新对象"""
        await self.session.flush()
        return obj
    
    async def delete(self, obj: ModelType) -> None:
        """删除对象"""
        await self.session.delete(obj)
        await self.session.flush()
