# from typing import Type
# from pydantic import BaseModel, Field
# from sqlmodel import SQLModel


from typing import Any, Callable, ClassVar, Generic, Self, Type, TypeVar
from pydantic import BaseModel
from app.models.base.base import TBaseSQLModel

TSchemaDataProcessFunc = Callable[[dict[str, Any]], dict[str, Any]]


class BaseCreateSchema(BaseModel, Generic[TBaseSQLModel]):
    sqlmodel_cls: ClassVar[Type[TBaseSQLModel]]

    def to_sqlmodel(self, sqlmodel_cls: Type[TBaseSQLModel]) -> TBaseSQLModel:
        """将当前Pydantic模型实例转换为SQLModel实例"""
        # 获取当前Pydantic模型实例的字段数据
        data = self.model_dump()

        data = self._process_special_fields(data)

        return sqlmodel_cls(**data)
    
    @staticmethod
    def _process_special_fields(data: dict[str, Any]) -> dict[str, Any]:
        """处理需要特殊转换的字段（如关系字段）"""
        # 子类实现自定义逻辑，例如：
        # - 排除不需要的字段
        return data


class BasePublicSchema(BaseModel):
    sqlmodel_cls: ClassVar[Type[TBaseSQLModel]]

    @classmethod
    def from_sqlmodel(cls, instance: TBaseSQLModel) -> Self:
        """将SQLModel实例转换为当前Pydantic模型实例"""
        # 获取SQLModel实例的字段数据
        data = instance.model_dump()
        return cls(**data)

    # @classmethod
    # def _process_special_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
    #     """处理需要特殊转换的字段（如关系字段）"""
    #     # 子类实现自定义逻辑，例如：
    #     # - 排除不需要的字段
    #     # - 转换关系对象为ID列表
    #     # - 处理日期时间格式等
    #     return data


TBaseCreateSchema = TypeVar("TBaseCreateSchema", bound=BaseCreateSchema)
TBasePublicSchema = TypeVar("TBasePublicSchema", bound=BasePublicSchema)
