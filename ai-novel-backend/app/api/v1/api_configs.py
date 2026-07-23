"""
API 配置管理路由
管理用户的 AI API 配置
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_optional_user, DEFAULT_USER_ID
from app.schemas.api_config import (
    ApiConfigCreate,
    ApiConfigUpdate,
    ApiConfigResponse,
    ApiConfigListResponse,
    ApiConfigDetailResponse,
)
from app.services.api_config_service import ApiConfigService, mask_api_key

router = APIRouter(prefix="/api-configs", tags=["API 配置"])


def config_to_response(config) -> ApiConfigResponse:
    """将模型转换为响应（脱敏 API Key）"""
    return ApiConfigResponse(
        id=config.id,
        owner_id=config.owner_id,
        name=config.name,
        api_url=config.api_url,
        api_key_masked=mask_api_key(config.api_key),
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        is_active=config.is_active,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


def config_to_detail(config) -> ApiConfigDetailResponse:
    """将模型转换为详情响应（包含完整 API Key）"""
    return ApiConfigDetailResponse(
        id=config.id,
        owner_id=config.owner_id,
        name=config.name,
        api_url=config.api_url,
        api_key=config.api_key,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        is_active=config.is_active,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.get("", response_model=ApiConfigListResponse)
async def list_configs(
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有 API 配置列表"""
    service = ApiConfigService(db)
    configs = await service.list_by_owner(DEFAULT_USER_ID)
    return ApiConfigListResponse(
        items=[config_to_response(c) for c in configs],
        total=len(configs),
    )


@router.get("/{config_id}", response_model=ApiConfigDetailResponse)
async def get_config(
    config_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取单个 API 配置详情（包含完整 API Key）"""
    service = ApiConfigService(db)
    config = await service.get_by_id(config_id)

    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    return config_to_detail(config)


@router.post("", response_model=ApiConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_config(
    config_data: ApiConfigCreate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新的 API 配置"""
    service = ApiConfigService(db)
    config = await service.create(DEFAULT_USER_ID, config_data)
    return config_to_response(config)


@router.put("/{config_id}", response_model=ApiConfigResponse)
async def update_config(
    config_id: str,
    config_data: ApiConfigUpdate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """更新 API 配置"""
    service = ApiConfigService(db)
    config = await service.get_by_id(config_id)

    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    updated = await service.update(config_id, config_data)
    return config_to_response(updated)


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_config(
    config_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """删除 API 配置"""
    service = ApiConfigService(db)
    config = await service.get_by_id(config_id)

    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    await service.delete(config_id)


@router.post("/{config_id}/test")
async def test_config(
    config_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """测试 API 配置是否可用"""
    service = ApiConfigService(db)
    config = await service.get_by_id(config_id)

    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    import httpx
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                config.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {config.api_key}",
                },
                json={
                    "model": config.model,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "max_tokens": 10,
                },
            )

            if response.status_code == 200:
                return {"success": True, "message": "连接成功！"}
            else:
                return {
                    "success": False,
                    "message": f"HTTP {response.status_code}: {response.text[:200]}",
                }
    except httpx.TimeoutException:
        return {"success": False, "message": "连接超时，请检查 API 地址是否正确"}
    except Exception as e:
        return {"success": False, "message": str(e)}
