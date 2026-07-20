"""
词条相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


class SnippetCreate(BaseModel):
    """创建词条"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str | None = None
    category: str = "自定义"


class SnippetUpdate(BaseModel):
    """更新词条"""
    title: str | None = None
    content: str | None = None
    category: str | None = None


class SnippetResponse(BaseModel):
    """词条响应"""
    id: str
    title: str
    content: str | None = None
    category: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SnippetListResponse(BaseModel):
    """词条列表响应"""
    items: list[SnippetResponse]
    total: int
