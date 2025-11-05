from dataclasses import dataclass
from typing import Optional

@dataclass
class FolkCultureBase:
    """民俗文化基础模型"""
    title: str
    description: str
    category: str
    region: str

@dataclass
class FolkCultureCreate(FolkCultureBase):
    """创建民俗文化的请求模型"""
    pass

@dataclass
class FolkCultureResponse(FolkCultureBase):
    """民俗文化响应模型"""
    id: int
    created_at: Optional[str] = None
