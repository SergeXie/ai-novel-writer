"""
AI 聊天 API 路由
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.core.security import get_optional_user
from app.schemas.conversation import ChatRequest, ChatResponse, MessageResponse
from app.services.ai_service import get_ai_service
from datetime import datetime, timezone
import json

router = APIRouter(prefix="/chat", tags=["AI 对话"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_optional_user),
):
    """发送消息并获取 AI 回复"""
    ai_service = get_ai_service()

    # 构建消息
    messages = [
        {"role": "system", "content": "你是一位专业的小说作家助手，帮助用户创作优秀的小说作品。"},
        {"role": "user", "content": request.message},
    ]

    # 调用 AI
    response_content = await ai_service.chat(messages)

    return ChatResponse(
        conversation_id=request.conversation_id or "new",
        message=MessageResponse(
            role="assistant",
            content=response_content,
            timestamp=datetime.now(timezone.utc),
        ),
    )


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """流式聊天接口"""
    ai_service = get_ai_service()

    messages = [
        {"role": "system", "content": "你是一位专业的小说作家助手，帮助用户创作优秀的小说作品。"},
        {"role": "user", "content": request.message},
    ]

    async def event_generator():
        """SSE 事件生成器"""
        stream = await ai_service.stream_chat(messages)
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'content': content})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
