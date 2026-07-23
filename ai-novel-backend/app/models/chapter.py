"""
小说章节模型
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class NovelChapter(Base):
    """小说章节表"""
    __tablename__ = "novel_chapters"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    chapter_number: Mapped[int] = mapped_column(Integer, default=0, comment="排序序号")
    node_type: Mapped[str] = mapped_column(String(20), default="chapter", comment="节点类型: folder/chapter")
    parent_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("novel_chapters.id"), nullable=True, comment="父节点ID，为空表示顶层")
    is_expanded: Mapped[bool] = mapped_column(Boolean, default=True, comment="文件夹是否展开")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="同级排序")
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, writing, completed

    # 外键关联项目
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("novel_projects.id"), nullable=False)

    # 关系
    children = relationship("NovelChapter", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("NovelChapter", back_populates="children", remote_side="NovelChapter.id")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 关系
    project = relationship("NovelProject", back_populates="chapters")

    @property
    def is_folder(self) -> bool:
        return self.node_type == "folder"

    def __repr__(self):
        return f"<NovelChapter(id={self.id}, title={self.title}, type={self.node_type})>"
