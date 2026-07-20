"""
提示词 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_optional_user
from app.schemas.prompt import (
    PromptCreate,
    PromptUpdate,
    PromptResponse,
    PromptListResponse,
)
from app.models.prompt import Prompt

router = APIRouter(prefix="/prompts", tags=["提示词"])


@router.get("", response_model=PromptListResponse)
async def list_prompts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str | None = None,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取提示词列表"""
    # 查询条件：公开的 + 自己的
    conditions = [
        (Prompt.is_public == True) | (Prompt.owner_id == current_user["id"])
    ]
    if category:
        conditions.append(Prompt.category == category)

    count_query = select(func.count()).select_from(Prompt).where(*conditions)
    total = (await db.execute(count_query)).scalar()

    query = (
        select(Prompt)
        .where(*conditions)
        .order_by(Prompt.like_count.desc(), Prompt.usage_count.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = list(result.scalars().all())

    return PromptListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    data: PromptCreate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """创建提示词"""
    prompt = Prompt(
        title=data.title,
        description=data.description,
        content=data.content,
        category=data.category,
        is_public=data.is_public,
        owner_id=current_user["id"],
    )
    db.add(prompt)
    await db.flush()
    return prompt


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取单个提示词"""
    result = await db.execute(
        select(Prompt).where(Prompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return prompt


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: str,
    data: PromptUpdate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """更新提示词"""
    result = await db.execute(
        select(Prompt).where(
            Prompt.id == prompt_id,
            Prompt.owner_id == current_user["id"],
        )
    )
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在或无权修改")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prompt, field, value)

    await db.flush()
    return prompt


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """删除提示词"""
    result = await db.execute(
        select(Prompt).where(
            Prompt.id == prompt_id,
            Prompt.owner_id == current_user["id"],
        )
    )
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在或无权删除")

    await db.delete(prompt)


@router.post("/{prompt_id}/use")
async def use_prompt(
    prompt_id: str,
    db: AsyncSession = Depends(get_db),
):
    """使用提示词（增加使用次数）"""
    result = await db.execute(
        select(Prompt).where(Prompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")

    prompt.usage_count += 1
    await db.flush()
    return {"success": True, "usage_count": prompt.usage_count}


@router.post("/{prompt_id}/like")
async def like_prompt(
    prompt_id: str,
    db: AsyncSession = Depends(get_db),
):
    """点赞提示词"""
    result = await db.execute(
        select(Prompt).where(Prompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")

    prompt.like_count += 1
    await db.flush()
    return {"success": True, "like_count": prompt.like_count}
