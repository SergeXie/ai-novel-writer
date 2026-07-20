"""
小说项目服务层
"""
from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.novel import NovelProject
from app.schemas.novel import ProjectCreate, ProjectUpdate


class NovelService:
    """小说项目服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: str) -> NovelProject | None:
        """根据 ID 获取项目"""
        result = await self.db.execute(
            select(NovelProject).where(NovelProject.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list_by_owner(
        self, owner_id: str, page: int = 1, page_size: int = 20
    ) -> tuple[list[NovelProject], int]:
        """获取用户的所有项目"""
        # 查询总数
        count_query = select(func.count()).select_from(NovelProject).where(
            NovelProject.owner_id == owner_id
        )
        total = (await self.db.execute(count_query)).scalar()

        # 分页查询
        query = (
            select(NovelProject)
            .where(NovelProject.owner_id == owner_id)
            .order_by(NovelProject.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(query)
        projects = list(result.scalars().all())

        return projects, total

    async def create(self, owner_id: str, project_data: ProjectCreate) -> NovelProject:
        """创建新项目"""
        project = NovelProject(
            title=project_data.title,
            description=project_data.description,
            genre=project_data.genre,
            owner_id=owner_id,
        )
        self.db.add(project)
        await self.db.flush()
        return project

    async def update(
        self, project_id: str, project_data: ProjectUpdate
    ) -> NovelProject | None:
        """更新项目"""
        project = await self.get_by_id(project_id)
        if not project:
            return None

        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        await self.db.flush()
        return project

    async def delete(self, project_id: str) -> bool:
        """删除项目"""
        project = await self.get_by_id(project_id)
        if not project:
            return False

        await self.db.delete(project)
        return True
