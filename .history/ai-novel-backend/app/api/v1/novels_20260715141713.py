"""
小说项目 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.novel import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from app.services.novel_service import NovelService

router = APIRouter(prefix="/projects", tags=["小说项目"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新项目"""
    service = NovelService(db)
    project = await service.create(
        owner_id=current_user["id"],
        project_data=project_data,
    )
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目详情"""
    service = NovelService(db)
    project = await service.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此项目")

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
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
    current_user: dict = Depends(get_current_user),
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
