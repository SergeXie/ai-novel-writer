"""
小说项目 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_optional_user
from app.schemas.novel import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectListResponse,
)
from app.schemas.chapter import (
    ChapterCreate,
    ChapterUpdate,
    ChapterResponse,
    ChapterListResponse,
)
from app.models.chapter import NovelChapter
from app.services.novel_service import NovelService

router = APIRouter(prefix="/projects", tags=["小说项目"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目列表"""
    service = NovelService(db)
    projects, total = await service.list_by_owner(
        owner_id=current_user["id"],
        page=page,
        page_size=page_size,
    )

    return ProjectListResponse(
        items=projects,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新项目"""
    service = NovelService(db)
    project = await service.create(
        owner_id=current_user["id"],
        project_data=project_data,
    )
    return project


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目详情（包含章节列表）"""
    service = NovelService(db)
    project = await service.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此项目")

    # 查询章节列表
    chapters_query = (
        select(NovelChapter)
        .where(NovelChapter.project_id == project_id)
        .order_by(NovelChapter.chapter_number)
    )
    result = await db.execute(chapters_query)
    chapters = list(result.scalars().all())

    # 构建响应
    return ProjectDetailResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        genre=project.genre,
        cover_image=project.cover_image,
        status=project.status,
        owner_id=project.owner_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        chapters=chapters,
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """更新项目"""
    service = NovelService(db)
    project = await service.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权修改此项目")

    updated = await service.update(project_id, project_data)
    return updated


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """删除项目"""
    service = NovelService(db)
    project = await service.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权删除此项目")

    await service.delete(project_id)


# ==================== 章节管理 API ====================


@router.get("/{project_id}/chapters", response_model=ChapterListResponse)
async def list_chapters(
    project_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目的所有章节"""
    # 验证项目所有权
    service = NovelService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此项目")

    # 查询章节
    query = (
        select(NovelChapter)
        .where(NovelChapter.project_id == project_id)
        .order_by(NovelChapter.chapter_number)
    )
    result = await db.execute(query)
    chapters = list(result.scalars().all())

    return ChapterListResponse(items=chapters, total=len(chapters))


@router.post(
    "/{project_id}/chapters",
    response_model=ChapterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chapter(
    project_id: str,
    chapter_data: ChapterCreate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新章节"""
    # 验证项目所有权
    service = NovelService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权修改此项目")

    # 检查章节编号是否重复（仅对实际章节检查）
    if chapter_data.chapter_number > 0:
        existing = await db.execute(
            select(NovelChapter).where(
                NovelChapter.project_id == project_id,
                NovelChapter.chapter_number == chapter_data.chapter_number,
                NovelChapter.node_type == 'chapter',
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="该章节编号已存在")

    # 创建章节/文件夹
    chapter = NovelChapter(
        title=chapter_data.title,
        content=chapter_data.content,
        chapter_number=chapter_data.chapter_number,
        node_type=chapter_data.node_type,
        parent_id=chapter_data.parent_id,
        is_expanded=chapter_data.is_expanded,
        sort_order=chapter_data.sort_order,
        word_count=len(chapter_data.content) if chapter_data.content else 0,
        project_id=project_id,
    )
    db.add(chapter)
    await db.flush()

    return chapter


@router.get("/{project_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    project_id: str,
    chapter_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """获取单个章节详情"""
    # 验证项目所有权
    service = NovelService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此项目")

    # 查询章节
    result = await db.execute(
        select(NovelChapter).where(
            NovelChapter.id == chapter_id,
            NovelChapter.project_id == project_id,
        )
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    return chapter


@router.put("/{project_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    project_id: str,
    chapter_id: str,
    chapter_data: ChapterUpdate,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """更新章节"""
    # 验证项目所有权
    service = NovelService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权修改此项目")

    # 查询章节
    result = await db.execute(
        select(NovelChapter).where(
            NovelChapter.id == chapter_id,
            NovelChapter.project_id == project_id,
        )
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 更新字段
    update_data = chapter_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chapter, field, value)

    # 更新字数
    if chapter.content is not None:
        chapter.word_count = len(chapter.content)

    await db.flush()

    return chapter


@router.delete(
    "/{project_id}/chapters/{chapter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chapter(
    project_id: str,
    chapter_id: str,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """删除章节"""
    # 验证项目所有权
    service = NovelService(db)
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权修改此项目")

    # 查询章节
    result = await db.execute(
        select(NovelChapter).where(
            NovelChapter.id == chapter_id,
            NovelChapter.project_id == project_id,
        )
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 递归删除子节点（SQLite 不支持 ON DELETE CASCADE，需要手动处理）
    async def delete_children(parent_id: str):
        children_result = await db.execute(
            select(NovelChapter).where(NovelChapter.parent_id == parent_id)
        )
        children = list(children_result.scalars().all())
        for child in children:
            await delete_children(child.id)
            await db.delete(child)

    await delete_children(chapter_id)
    await db.delete(chapter)
