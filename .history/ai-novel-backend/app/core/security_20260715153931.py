"""
认证与安全模块
处理 JWT Token 生成和验证
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db


# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer Token 提取
security = HTTPBearer()


def hash_password(password: str) -> str:
    """对密码进行哈希"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """解码令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """获取当前认证用户"""
    token = credentials.credentials
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌类型无效",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户凭证",
        )

    # TODO: 从数据库查询用户
    # from app.models.user import User
    # result = await db.execute(select(User).where(User.id == user_id))
    # user = result.scalar_one_or_none()
    # if user is None:
    #     raise HTTPException(status_code=404, detail="用户不存在")
    # return user

    return {"id": user_id, "email": payload.get("email")}


# 默认用户ID（无需登录时使用）
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户（可选认证）
    
    如果提供了有效的 token，则返回认证用户信息
    如果没有提供 token，则返回默认用户信息
    """
    if credentials is None:
        # 没有提供 token，返回默认用户
        return {"id": DEFAULT_USER_ID, "email": "default@example.com"}

    try:
        token = credentials.credentials
        payload = decode_token(token)

        if payload.get("type") != "access":
            return {"id": DEFAULT_USER_ID, "email": "default@example.com"}

        user_id = payload.get("sub")
        if user_id is None:
            return {"id": DEFAULT_USER_ID, "email": "default@example.com"}

        return {"id": user_id, "email": payload.get("email")}
    except Exception:
        # token 无效时返回默认用户
        return {"id": DEFAULT_USER_ID, "email": "default@example.com"}
