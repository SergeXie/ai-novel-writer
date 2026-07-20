"""
认证 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, get_optional_user, DEFAULT_USER_ID
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    service = UserService(db)
    try:
        user = await service.create(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    service = UserService(db)
    user = await service.authenticate(login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
        )

    access_token = create_access_token(data={"sub": user.id, "email": user.email})
    refresh_token = create_refresh_token(data={"sub": user.id, "email": user.email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
async def get_me(current_user: dict = Depends(get_optional_user)):
    """获取当前用户信息"""
    return current_user
