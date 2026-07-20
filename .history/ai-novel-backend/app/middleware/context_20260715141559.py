"""
请求追踪中间件
为每个请求生成唯一 ID，便于日志追踪
"""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestContextMiddleware(BaseHTTPMiddleware):
    """请求上下文中间件 - 添加 request_id"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # 生成或复用请求 ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # 存储到请求状态中
        request.state.request_id = request_id

        response = await call_next(request)

        # 添加响应头
        response.headers["X-Request-ID"] = request_id

        return response
