"""
对话相关的 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


# ---- 请求模型 ----

class ConversationCreate(BaseModel):
    """创建对话"""
    title: str = Field(..., min_length=1, max_length=200)
    project_id: str | None = None


class MessageCreate(BaseModel):
    """发送消息"""
    content: str = Field(..., min_length=1)
    role: str = "user"  # user 或 assistant


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None
    project_id: str | None = None
    context: list[str] | None = None  # 上下文文件/目录


# ---- 响应模型 ----

class MessageResponse(BaseModel):
    """消息响应"""
    role: str
    content: str
    timestamp: datetime


class ConversationResponse(BaseModel):
    """对话响应"""
    id: str
    title: str
    messages: list[MessageResponse] | None = None
    project_id: str | None = None
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """聊天响应"""
    conversation_id: str
    message: MessageResponse
