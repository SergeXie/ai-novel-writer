"""
小说项目相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


# ---- 请求模型 ----

class ProjectCreate(BaseModel):
    """创建小说项目"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    genre: str | None = None


class ProjectUpdate(BaseModel):
    """更新小说项目"""
    title: str | None = None
    description: str | None = None
    genre: str | None = None
    cover_image: str | None = None
    status: str | None = None


# ---- 响应模型 ----

class ProjectResponse(BaseModel):
    """小说项目响应"""
    id: str
    title: str
    description: str | None = None
    genre: str | None = None
    cover_image: str | None = None
    status: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int
