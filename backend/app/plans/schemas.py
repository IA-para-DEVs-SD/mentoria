from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ActionStatus(str, Enum):
    pendente = "pendente"
    concluida = "concluida"


class Priority(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"


# ---------------------------------------------------------------------------
# Output schemas
# ---------------------------------------------------------------------------


class GapOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    description: str
    relevance: int


class ActionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    priority: Priority
    category: str
    title: str
    objective: str
    context: str
    status: ActionStatus
    sequence: int


class PlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: datetime
    progress: int
    gaps: list[GapOut]
    actions: list[ActionOut]


class PlanSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: datetime
    progress: int


class ProgressOut(BaseModel):
    progress: int


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class ActionStatusUpdate(BaseModel):
    status: ActionStatus
