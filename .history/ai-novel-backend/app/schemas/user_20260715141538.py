"""
用户相关的 Pydantic 模型
用于请求/响应数据验证
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ---- 请求模型 ----

class UserCreate(BaseModel):
    """用户注册"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """更新用户信息"""
    username: str | None = None
    avatar: str | None = None


# ---- 响应模型 ----

class UserResponse(BaseModel):
    """用户信息响应"""
    id: str
    email: str
    username: str
    avatar: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """认证令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
