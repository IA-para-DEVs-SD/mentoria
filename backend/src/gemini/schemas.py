import unicodedata

from pydantic import BaseModel, field_validator


def _normalize_priority(v: str) -> str:
    """Remove acentos e converte para maiúsculas."""
    nfkd = unicodedata.normalize("NFKD", v)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).upper()


class GeminiActionItem(BaseModel):
    priority: str  # "ALTA", "MEDIA", "BAIXA"
    category: str
    title: str
    objective: str
    context: str
    sequence: int

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v: str) -> str:
        return _normalize_priority(v)


class GeminiGapItem(BaseModel):
    description: str
    relevance: int


class GeminiPlanResponse(BaseModel):
    plan_name: str
    gaps: list[GeminiGapItem]
    actions: list[GeminiActionItem]
