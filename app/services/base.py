from abc import ABC
from typing import Any

class BaseService(ABC):
    """基础服务类"""
    
    def __init__(self, **dependencies: Any):
        """初始化服务，注入依赖"""
        for key, value in dependencies.items():
            setattr(self, key, value)
