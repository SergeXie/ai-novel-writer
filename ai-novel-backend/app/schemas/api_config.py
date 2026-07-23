"""
API 配置 Pydantic 模型
用于请求/响应数据验证
"""
from datetime import datetime
from pydantic import BaseModel, Field


# ---- 请求模型 ----

class ApiConfigCreate(BaseModel):
    """创建 API 配置"""
    name: str = Field(..., min_length=1, max_length=100, description="配置名称")
    api_url: str = Field(..., description="API 接口地址")
    api_key: str = Field(..., description="API Key")
    model: str = Field(..., description="模型名称")
    temperature: float = Field(0.7, ge=0, le=2, description="创造性参数")
    max_tokens: int = Field(2048, ge=256, le=8192, description="最大回复长度")


class ApiConfigUpdate(BaseModel):
    """更新 API 配置"""
    name: str | None = Field(None, min_length=1, max_length=100)
    api_url: str | None = None
    api_key: str | None = None
    model: str | None = None
    temperature: float | None = Field(None, ge=0, le=2)
    max_tokens: int | None = Field(None, ge=256, le=8192)
    is_active: bool | None = None


# ---- 响应模型 ----

class ApiConfigResponse(BaseModel):
    """API 配置响应（隐藏完整 API Key）"""
    id: str
    owner_id: str
    name: str
    api_url: str
    api_key_masked: str = Field(..., description="脱敏的 API Key，如 sk-***abc")
    model: str
    temperature: float
    max_tokens: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApiConfigListResponse(BaseModel):
    """API 配置列表响应"""
    items: list[ApiConfigResponse]
    total: int


class ApiConfigDetailResponse(BaseModel):
    """API 配置详情响应（包含完整 API Key，仅编辑时使用）"""
    id: str
    owner_id: str
    name: str
    api_url: str
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---- 聊天请求（支持指定 API 配置） ----

class ChatWithConfigRequest(BaseModel):
    """使用指定 API 配置的聊天请求"""
    message: str
    api_config_id: str = Field(..., description="使用的 API 配置 ID")
    conversation_id: str | None = None
    project_id: str | None = None
