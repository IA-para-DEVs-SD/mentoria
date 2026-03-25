import re
from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CONTROL_CHAR_RE = re.compile(r"[^\t\n\r\x20-\x7E\x80-\uFFFF]")


def _strip_control_chars(value: str) -> str:
    """Remove caracteres de controle (chr < 32, exceto \\t \\n \\r)."""
    return _CONTROL_CHAR_RE.sub("", value)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Seniority(str, Enum):
    Estagio = "Estagio"
    Junior = "Junior"
    Pleno = "Pleno"
    Senior = "Senior"
    Especialista = "Especialista"
    Lideranca = "Lideranca"


class EducationLevel(str, Enum):
    Ensino_Medio = "Ensino_Medio"
    Tecnico = "Tecnico"
    Tecnologo = "Tecnologo"
    Bacharelado = "Bacharelado"
    Licenciatura = "Licenciatura"
    Pos_graduacao = "Pos_graduacao"
    MBA = "MBA"
    Mestrado = "Mestrado"
    Doutorado = "Doutorado"
    Pos_doutorado = "Pos_doutorado"


class CareerGoal(str, Enum):
    Crescer_na_carreira_atual = "Crescer_na_carreira_atual"
    Assumir_cargos_de_lideranca = "Assumir_cargos_de_lideranca"
    Mudar_de_area = "Mudar_de_area"


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class ExperienceIn(BaseModel):
    role: str = Field(min_length=1, max_length=500)
    seniority: Seniority
    company: str | None = Field(None, max_length=500)
    start_date: date
    end_date: date | None = None

    @field_validator("role", "company", mode="before")
    @classmethod
    def sanitize_text(cls, v: str | None) -> str | None:
        return None if v is None else _strip_control_chars(str(v))

    @model_validator(mode="after")
    def validate_dates(self) -> "ExperienceIn":
        today = date.today()
        if self.start_date > today:
            raise ValueError("start_date não pode ser futura")
        if self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date deve ser maior ou igual a start_date")
            if self.end_date > today:
                raise ValueError("end_date não pode ser futura")
        return self


class EducationIn(BaseModel):
    institution: str = Field(min_length=1, max_length=500)
    level: EducationLevel
    title: str = Field(min_length=1, max_length=500)
    study_area: str = Field(min_length=1, max_length=500)
    start_date: date
    end_date: date | None = None

    @field_validator("institution", "title", "study_area", mode="before")
    @classmethod
    def sanitize_text(cls, v: str | None) -> str | None:
        return None if v is None else _strip_control_chars(str(v))

    @model_validator(mode="after")
    def validate_dates(self) -> "EducationIn":
        today = date.today()
        if self.start_date > today:
            raise ValueError("start_date não pode ser futura")
        if self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date deve ser maior ou igual a start_date")
        return self


class ProfileIn(BaseModel):
    experiences: list[ExperienceIn] = Field(min_length=1)
    educations: list[EducationIn] = Field(min_length=1)
    skills: list[str] = Field(min_length=1)
    career_goal: CareerGoal

    @field_validator("skills", mode="before")
    @classmethod
    def sanitize_skills(cls, v: list) -> list:
        return [_strip_control_chars(str(s)) for s in v]


# ---------------------------------------------------------------------------
# Output schemas
# ---------------------------------------------------------------------------


class ExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: str
    seniority: Seniority
    company: str | None
    start_date: date
    end_date: date | None


class EducationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    institution: str
    level: EducationLevel
    title: str
    study_area: str
    start_date: date
    end_date: date | None


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    career_goal: CareerGoal
    skills: list[str]
    experiences: list[ExperienceOut]
    educations: list[EducationOut]
    created_at: datetime
    updated_at: datetime
