"""
AI 聊天 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from loguru import logger
from app.core.database import get_db
from app.core.security import get_optional_user, DEFAULT_USER_ID
from app.core.config import settings
from app.schemas.conversation import ChatRequest, ChatResponse, MessageResponse
from app.schemas.api_config import ChatWithConfigRequest
from app.services.ai_service import get_ai_service
from app.services.api_config_service import ApiConfigService
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import json

router = APIRouter(prefix="/chat", tags=["AI 对话"])


async def _get_ai_client_for_user(
    user_id: str, db: AsyncSession
) -> tuple[AsyncOpenAI | None, str | None, float, int]:
    """
    尝试获取用户配置的 AI 客户端。
    优先使用用户在"API 设置"中保存的活跃配置，
    如果没有则回退到全局配置。
    返回 (client_or_none, model_or_none, temperature, max_tokens)
    """
    service = ApiConfigService(db)
    config = await service.get_active_config(user_id)
    if config:
        logger.info(f"使用用户 API 配置: {config.name} (model={config.model})")
        client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.api_url.replace("/chat/completions", "")
            if "/chat/completions" in config.api_url
            else config.api_url,
        )
        return client, config.model, config.temperature, config.max_tokens

    # 尝试使用全局配置（检查 API Key 是否已配置）
    if settings.OPENAI_API_KEY:
        ai_service = get_ai_service()
        return ai_service.client, ai_service.model, 0.7, 2000

    return None, None, 0.7, 2000


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """发送消息并获取 AI 回复（自动使用用户配置或全局配置）"""
    user_id = current_user.get("id", DEFAULT_USER_ID)

    # 构建系统提示
    system_prompt = "你是一位专业的小说作家助手，帮助用户创作优秀的小说作品。"
    
    # 如果有上下文信息，添加到系统提示中
    if request.context:
        context_text = "\n\n".join(request.context)
        system_prompt += f"\n\n以下是用户提供的参考内容，请基于这些内容来回答用户的问题：\n\n{context_text}"
    
    # 构建消息
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.message},
    ]

    # 获取用户的 AI 客户端配置
    client, model, temperature, max_tokens = await _get_ai_client_for_user(
        user_id, db
    )

    if client is None:
        raise HTTPException(
            status_code=400,
            detail="未配置 AI API，请先在「API 设置」中添加 API 配置，或在后端 .env 文件中设置 OPENAI_API_KEY",
        )

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        response_content = response.choices[0].message.content
    except Exception as e:
        logger.error(f"AI 服务调用失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 服务调用失败: {str(e)}",
        )

    return ChatResponse(
        conversation_id=request.conversation_id or "new",
        message=MessageResponse(
            role="assistant",
            content=response_content,
            timestamp=datetime.now(timezone.utc),
        ),
    )


@router.post("/with-config", response_model=ChatResponse)
async def chat_with_config(
    request: ChatWithConfigRequest,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """使用指定 API 配置发送消息"""
    service = ApiConfigService(db)
    config = await service.get_by_id(request.api_config_id)

    if not config:
        raise HTTPException(status_code=404, detail="API 配置不存在")

    # 使用用户配置创建 OpenAI 客户端
    client = AsyncOpenAI(
        api_key=config.api_key,
        base_url=config.api_url.replace("/chat/completions", "")
        if "/chat/completions" in config.api_url
        else config.api_url,
    )

    # 构建消息
    messages = [
        {"role": "system", "content": "你是一位专业的小说作家助手，帮助用户创作优秀的小说作品。"},
        {"role": "user", "content": request.message},
    ]

    try:
        response = await client.chat.completions.create(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        response_content = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 服务调用失败: {str(e)}"
        )

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
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """流式聊天接口"""
    user_id = current_user.get("id", DEFAULT_USER_ID)

    # 构建系统提示
    system_prompt = "你是一位专业的小说作家助手，帮助用户创作优秀的小说作品。"
    
    # 如果有上下文信息，添加到系统提示中
    if request.context:
        context_text = "\n\n".join(request.context)
        system_prompt += f"\n\n以下是用户提供的参考内容，请基于这些内容来回答用户的问题：\n\n{context_text}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.message},
    ]

    # 获取用户的 AI 客户端配置
    client, model, temperature, max_tokens = await _get_ai_client_for_user(
        user_id, db
    )

    if client is None:
        raise HTTPException(
            status_code=400,
            detail="未配置 AI API，请先在「API 设置」中添加 API 配置，或在后端 .env 文件中设置 OPENAI_API_KEY",
        )

    async def event_generator():
        """SSE 事件生成器"""
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
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
