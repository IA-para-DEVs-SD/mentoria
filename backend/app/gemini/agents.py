"""Agentes PydanticAI para geração de planos e ações via Gemini."""

import os

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from app.config import settings
from app.gemini.schemas import GeminiActionItem, GeminiPlanResponse

os.environ.setdefault("GEMINI_API_KEY", settings.GEMINI_API_KEY)

_model = GeminiModel("gemini-2.5-flash")


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
