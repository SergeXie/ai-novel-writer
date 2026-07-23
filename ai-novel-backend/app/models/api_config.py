"""
API 配置模型
存储用户自定义的 AI API 配置
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class ApiConfig(Base):
    """用户 API 配置表"""
    __tablename__ = "api_configs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    owner_id: Mapped[str] = mapped_column(
        String(36), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="配置名称，如 '我的GPT4'"
    )
    api_url: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="API 接口地址"
    )
    api_key: Mapped[str] = mapped_column(
        Text, nullable=False, comment="API Key（加密存储）"
    )
    model: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="模型名称"
    )
    temperature: Mapped[float] = mapped_column(
        Float, default=0.7, comment="创造性参数 0-2"
    )
    max_tokens: Mapped[int] = mapped_column(
        Integer, default=2048, comment="最大回复长度"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="是否启用"
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
        return f"<ApiConfig(id={self.id}, name={self.name}, model={self.model})>"
