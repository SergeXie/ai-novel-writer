"""
对话记录模型
用于保存用户与 AI 的对话历史
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Conversation(Base):
    """对话记录表"""
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    messages: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # 存储对话消息列表

    # 外键关联
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    project_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("novel_projects.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title})>"
