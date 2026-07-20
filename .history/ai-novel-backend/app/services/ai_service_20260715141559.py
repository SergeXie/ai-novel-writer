"""
AI 服务层
处理与 LLM 的交互
"""
from openai import AsyncOpenAI
from loguru import logger
from app.core.config import settings


class AIService:
    """AI 服务 - 封装 LLM 调用"""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
        )
        self.model = settings.DEFAULT_MODEL

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
    ) -> str:
        """发送聊天请求"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

            if stream:
                return response  # 返回异步生成器

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"AI 服务调用失败: {e}")
            raise

    async def generate_novel(
        self,
        prompt: str,
        context: str | None = None,
        style: str = "普通",
    ) -> str:
        """生成小说内容"""
        system_prompt = """你是一位专业的小说作家，擅长创作各类题材的小说。
请根据用户的要求创作内容，注意：
1. 保持文笔流畅，情节连贯
2. 人物塑造丰满，对话自然
3. 适当使用修辞手法，增强文学性
4. 每次输出的内容应该有完整的情节发展"""

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "system", "content": f"参考上下文：{context}"})

        messages.append({"role": "user", "content": prompt})

        return await self.chat(messages, temperature=0.8)

    async def stream_chat(self, messages: list[dict]):
        """流式聊天"""
        return await self.chat(messages, stream=True)


# 单例模式
_ai_service: AIService | None = None


def get_ai_service() -> AIService:
    """获取 AI 服务实例"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
