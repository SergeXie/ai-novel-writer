"""
小说项目模型
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class NovelProject(Base):
    """小说项目表"""
    __tablename__ = "novel_projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    genre: Mapped[str | None] = mapped_column(String(50), nullable=True)  # 类型：玄幻、都市、科幻等
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, writing, completed

    # 外键关联用户
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 关系
    chapters = relationship("NovelChapter", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NovelProject(id={self.id}, title={self.title})>"
