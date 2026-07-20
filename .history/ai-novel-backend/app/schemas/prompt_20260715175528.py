"""
提示词相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    """创建提示词"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    content: str = Field(..., min_length=1)
    category: str = "其他"
    is_public: bool = True


class PromptUpdate(BaseModel):
    """更新提示词"""
    title: str | None = None
    description: str | None = None
    content: str | None = None
    category: str | None = None
    is_public: bool | None = None


class PromptResponse(BaseModel):
    """提示词响应"""
    id: str
    title: str
    description: str | None = None
    content: str
    category: str
    usage_count: int
    like_count: int
    owner_id: str
    is_public: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PromptListResponse(BaseModel):
    """提示词列表响应"""
    items: list[PromptResponse]
    total: int
    page: int
    page_size: int
