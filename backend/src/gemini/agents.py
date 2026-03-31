"""Agentes PydanticAI para geração de planos e ações via Gemini."""

import os

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from src.config import settings
from src.gemini.schemas import GeminiActionItem, GeminiPlanResponse

os.environ.setdefault("GEMINI_API_KEY", settings.GEMINI_API_KEY)

_model = GoogleModel(
    settings.GEMINI_MODEL,
    provider=GoogleProvider(api_key=settings.GEMINI_API_KEY),
)


class ActionsResponse(BaseModel):
    actions: list[GeminiActionItem]


roadmap_agent: Agent[None, GeminiPlanResponse] = Agent(
    _model,
    output_type=GeminiPlanResponse,
)

actions_agent: Agent[None, ActionsResponse] = Agent(
    _model,
    output_type=ActionsResponse,
)
