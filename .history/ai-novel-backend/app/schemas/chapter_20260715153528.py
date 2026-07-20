"""
章节相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


# ---- 请求模型 ----

class ChapterCreate(BaseModel):
    """创建章节"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str | None = None
    chapter_number: int = Field(..., ge=1)


class ChapterUpdate(BaseModel):
    """更新章节"""
    title: str | None = None
    content: str | None = None
    chapter_number: int | None = None
    status: str | None = None


# ---- 响应模型 ----

class ChapterResponse(BaseModel):
    """章节响应"""
    id: str
    title: str
    content: str | None = None
    chapter_number: int
    word_count: int
    status: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChapterListResponse(BaseModel):
    """章节列表响应"""
    items: list[ChapterResponse]
    total: int
