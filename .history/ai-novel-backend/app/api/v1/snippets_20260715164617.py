"""
词条 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_optional_user
from app.schemas.snippet import (
    SnippetCreate,
    SnippetUpdate,
    SnippetResponse,
    SnippetListResponse,
)
from app.models.snippet import Snippet

router = APIRouter(prefix="/snippets", tags=["词条"])


@router.get("", response_model=SnippetListResponse)
async def list_snippets(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取词条列表"""
    count_query = select(func.count()).select_from(Snippet).where(
        Snippet.owner_id == current_user["id"]
    )
    total = (await db.execute(count_query)).scalar()

    query = (
        select(Snippet)
        .where(Snippet.owner_id == current_user["id"])
        .order_by(Snippet.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = list(result.scalars().all())

    return SnippetListResponse(items=items, total=total)


@router.post("", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    data: SnippetCreate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """创建词条"""
    snippet = Snippet(
        title=data.title,
        content=data.content,
        category=data.category,
        owner_id=current_user["id"],
    )
    db.add(snippet)
    await db.flush()
    return snippet


@router.put("/{snippet_id}", response_model=SnippetResponse)
async def update_snippet(
    snippet_id: str,
    data: SnippetUpdate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """更新词条"""
    result = await db.execute(
        select(Snippet).where(
            Snippet.id == snippet_id,
            Snippet.owner_id == current_user["id"],
        )
    )
    snippet = result.scalar_one_or_none()
    if not snippet:
        raise HTTPException(status_code=404, detail="词条不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(snippet, field, value)

    await db.flush()
    return snippet


@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_snippet(
    snippet_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """删除词条"""
    result = await db.execute(
        select(Snippet).where(
            Snippet.id == snippet_id,
            Snippet.owner_id == current_user["id"],
        )
    )
    snippet = result.scalar_one_or_none()
    if not snippet:
        raise HTTPException(status_code=404, detail="词条不存在")

    await db.delete(snippet)
