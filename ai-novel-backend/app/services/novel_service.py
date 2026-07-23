"""
小说项目服务层
"""
from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.novel import NovelProject
from app.models.chapter import NovelChapter
from app.schemas.novel import ProjectCreate, ProjectUpdate


# ---- 默认模板定义 ----
# 每个元素: (文件夹名, [(章节名, 默认内容), ...])
DEFAULT_TEMPLATE: list[tuple[str, list[tuple[str, str]]]] = [
    ("备忘录", [
        ("备忘录", "# 备忘录\n\n在这里记录你的创作灵感、待办事项和重要提醒。\n"),
    ]),
    ("大纲", [
        ("大纲", "# 大纲\n\n在这里填写你的故事主线大纲。\n"),
        ("其他大纲", "# 其他大纲\n\n支线剧情、角色线索等补充大纲。\n"),
        ("细纲", "# 细纲\n\n将大纲细化为具体的章节安排。\n"),
    ]),
    ("设定", [
        ("场景设定", "# 场景设定\n\n故事发生的场景、地点、环境描写。\n"),
        ("技能设定", "# 技能设定\n\n角色的能力、技能体系设定。\n"),
        ("人物设定", "# 人物设定\n\n主要角色的外貌、性格、背景等设定。\n"),
        ("世界设定", "# 世界设定\n\n故事世界观、历史、规则等设定。\n"),
        ("势力设定", "# 势力设定\n\n故事中的阵营、组织、势力关系。\n"),
        ("物品设定", "# 物品设定\n\n重要道具、武器、特殊物品设定。\n"),
    ]),
    ("章节", []),
]


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
        """创建新项目，并自动生成默认模板目录结构"""
        project = NovelProject(
            title=project_data.title,
            description=project_data.description,
            genre=project_data.genre,
            owner_id=owner_id,
        )
        self.db.add(project)
        await self.db.flush()

        # ---- 自动生成默认模板 ----
        for sort_idx, (folder_name, chapters) in enumerate(DEFAULT_TEMPLATE):
            # 创建文件夹节点
            folder = NovelChapter(
                title=folder_name,
                node_type="folder",
                project_id=project.id,
                sort_order=sort_idx,
                is_expanded=True,
            )
            self.db.add(folder)
            await self.db.flush()

            # 创建文件夹下的章节节点
            for ch_idx, (ch_title, ch_content) in enumerate(chapters):
                chapter = NovelChapter(
                    title=ch_title,
                    content=ch_content,
                    node_type="chapter",
                    project_id=project.id,
                    parent_id=folder.id,
                    sort_order=ch_idx,
                    word_count=len(ch_content),
                )
                self.db.add(chapter)

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
