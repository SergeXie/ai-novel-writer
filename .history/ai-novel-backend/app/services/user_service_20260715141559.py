"""
用户服务层
处理用户相关的业务逻辑
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password


class UserService:
    """用户服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: str) -> User | None:
        """根据 ID 获取用户"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """创建新用户"""
        # 检查邮箱是否已存在
        existing = await self.get_by_email(user_data.email)
        if existing:
            raise ValueError("邮箱已被注册")

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def authenticate(self, email: str, password: str) -> User | None:
        """用户认证"""
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def update(self, user_id: str, user_data: UserUpdate) -> User | None:
        """更新用户信息"""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.flush()
        return user
