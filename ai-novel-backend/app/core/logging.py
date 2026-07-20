"""
日志配置模块
使用 loguru 提供结构化日志
"""
import sys
from loguru import logger
from app.core.config import settings


def setup_logging():
    """配置应用日志"""
    # 移除默认处理器
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
    )

    # 文件输出 - 应用日志
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="00:00",      # 每天轮转
        retention="30 days",   # 保留30天
        compression="zip",     # 压缩旧日志
        encoding="utf-8",
    )

    # 文件输出 - 错误日志
    logger.add(
        "logs/error_{time:YYYY-MM-DD}.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="00:00",
        retention="90 days",
        compression="zip",
        encoding="utf-8",
    )

    logger.info("日志系统初始化完成")
    return logger
