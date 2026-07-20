"""
通用响应模型
"""
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    code: int = 200
    message: str = "success"
    data: dict | list | None = None


class PaginatedResponse(BaseModel):
    """分页响应"""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
