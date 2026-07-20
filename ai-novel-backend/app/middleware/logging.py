"""
请求日志中间件
记录每个请求的耗时和状态
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # 记录请求信息
        logger.info(f"请求开始: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(f"请求异常: {request.method} {request.url.path} - {exc}")
            raise

        # 计算耗时
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))

        logger.info(
            f"请求完成: {request.method} {request.url.path} "
            f"状态码: {response.status_code} "
            f"耗时: {process_time:.4f}s"
        )

        return response
