"""
API 配置服务层
管理用户的 AI API 配置
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.api_config import ApiConfig
from app.schemas.api_config import ApiConfigCreate, ApiConfigUpdate


def mask_api_key(key: str) -> str:
    """对 API Key 进行脱敏处理"""
    if not key:
        return ""
    if len(key) <= 8:
        return key[:2] + "***"
    return key[:4] + "***" + key[-4:]


class ApiConfigService:
    """API 配置服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, config_id: str) -> ApiConfig | None:
        """根据 ID 获取配置"""
        result = await self.db.execute(
            select(ApiConfig).where(ApiConfig.id == config_id)
        )
        return result.scalar_one_or_none()

    async def list_by_owner(
        self, owner_id: str
    ) -> list[ApiConfig]:
        """获取用户的所有 API 配置"""
        query = (
            select(ApiConfig)
            .where(ApiConfig.owner_id == owner_id)
            .order_by(ApiConfig.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(
        self, owner_id: str, config_data: ApiConfigCreate
    ) -> ApiConfig:
        """创建新的 API 配置"""
        config = ApiConfig(
            owner_id=owner_id,
            name=config_data.name,
            api_url=config_data.api_url,
            api_key=config_data.api_key,
            model=config_data.model,
            temperature=config_data.temperature,
            max_tokens=config_data.max_tokens,
        )
        self.db.add(config)
        await self.db.flush()
        return config

    async def update(
        self, config_id: str, config_data: ApiConfigUpdate
    ) -> ApiConfig | None:
        """更新 API 配置"""
        config = await self.get_by_id(config_id)
        if not config:
            return None

        update_data = config_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(config, field, value)

        await self.db.flush()
        return config

    async def delete(self, config_id: str) -> bool:
        """删除 API 配置"""
        config = await self.get_by_id(config_id)
        if not config:
            return False

        await self.db.delete(config)
        return True

    async def get_active_config(self, owner_id: str) -> ApiConfig | None:
        """获取用户启用的 API 配置（取最新的一个）"""
        query = (
            select(ApiConfig)
            .where(ApiConfig.owner_id == owner_id, ApiConfig.is_active == True)
            .order_by(ApiConfig.created_at.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
