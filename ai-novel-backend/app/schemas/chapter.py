"""
章节相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


# ---- 请求模型 ----

class ChapterCreate(BaseModel):
    """创建章节/文件夹"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str | None = None
    chapter_number: int = Field(0, ge=0)
    node_type: str = Field("chapter", description="节点类型: folder/chapter")
    parent_id: str | None = Field(None, description="父节点ID")
    is_expanded: bool = Field(True, description="文件夹展开状态")
    sort_order: int = Field(0, description="同级排序")


class ChapterUpdate(BaseModel):
    """更新章节/文件夹"""
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    chapter_number: int | None = None
    node_type: str | None = None
    parent_id: str | None = None
    is_expanded: bool | None = None
    sort_order: int | None = None
    status: str | None = None


# ---- 响应模型 ----

class ChapterResponse(BaseModel):
    """章节/文件夹响应"""
    id: str
    title: str
    content: str | None = None
    chapter_number: int
    node_type: str
    parent_id: str | None = None
    is_expanded: bool
    sort_order: int
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
