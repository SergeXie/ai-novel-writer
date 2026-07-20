"""
小说章节模型
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, DateTime, Integer
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
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, writing, completed

    # 外键关联项目
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("novel_projects.id"), nullable=False)

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

    def __repr__(self):
        return f"<NovelChapter(id={self.id}, title={self.title})>"
