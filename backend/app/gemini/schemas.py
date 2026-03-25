from pydantic import BaseModel


class GeminiActionItem(BaseModel):
    priority: str  # "ALTA", "MEDIA", "BAIXA"
    category: str
    title: str
    objective: str
    context: str
    sequence: int


class GeminiGapItem(BaseModel):
    description: str
    relevance: int


class GeminiPlanResponse(BaseModel):
    plan_name: str
    gaps: list[GeminiGapItem]
    actions: list[GeminiActionItem]
