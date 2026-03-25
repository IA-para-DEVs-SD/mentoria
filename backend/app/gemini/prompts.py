"""Templates de prompt para o Gemini."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.plans.models import Action, Rejection
    from app.profile.models import Profile


def _format_profile_section(profile: "Profile") -> str:
    experiences = []
    for exp in profile.experiences:
        period = str(exp.start_date)
        if exp.end_date:
            period += f" a {exp.end_date}"
        else:
            period += " até o momento"
        company = f", {exp.company}" if exp.company else ""
        experiences.append(f"  - {exp.role} ({exp.seniority}{company}, {period})")

    educations = []
    for edu in profile.educations:
        educations.append(f"  - {edu.institution}: {edu.level} em {edu.title} ({edu.study_area})")

    skills = profile.skills or []

    lines = [
        "PERFIL DO USUÁRIO:",
        f"- Objetivo: {profile.career_goal}",
        "- Experiências:",
        *experiences,
        "- Formação:",
        *educations,
        f"- Habilidades: {', '.join(skills)}",
    ]
    return "\n".join(lines)


def _format_rejections_section(rejections: list["Rejection"]) -> str:
    if not rejections:
        return "REJEIÇÕES ANTERIORES (evitar conteúdo similar):\n- Nenhuma"

    items = [f"  - {r.category}: {r.action_title}" for r in rejections]
    lines = ["REJEIÇÕES ANTERIORES (evitar conteúdo similar):", *items]
    return "\n".join(lines)


def build_plan_prompt(profile: "Profile", rejections: list["Rejection"]) -> str:
    """Monta o prompt para geração de plano completo."""
    profile_section = _format_profile_section(profile)
    rejections_section = _format_rejections_section(rejections)

    return f"""{profile_section}

{rejections_section}

INSTRUÇÕES:
Retorne um JSON com o seguinte schema:
{{
  "plan_name": "string",
  "gaps": [{{"description": "string", "relevance": int}}],
  "actions": [{{
    "priority": "ALTA|MEDIA|BAIXA",
    "category": "string",
    "title": "string",
    "objective": "string",
    "context": "string",
    "sequence": int
  }}]
}}"""


def build_actions_prompt(
    profile: "Profile",
    existing_actions: list["Action"],
    rejections: list["Rejection"],
) -> str:
    """Monta o prompt para geração de mais ações."""
    profile_section = _format_profile_section(profile)
    rejections_section = _format_rejections_section(rejections)

    if existing_actions:
        action_items = [
            f"  - [{a.category}] {a.title}" for a in existing_actions
        ]
        existing_section = "AÇÕES EXISTENTES (não duplicar):\n" + "\n".join(action_items)
    else:
        existing_section = "AÇÕES EXISTENTES (não duplicar):\n- Nenhuma"

    return f"""{profile_section}

{rejections_section}

{existing_section}

INSTRUÇÕES:
Retorne um JSON com o seguinte schema:
{{"actions": [{{
  "priority": "ALTA|MEDIA|BAIXA",
  "category": "string",
  "title": "string",
  "objective": "string",
  "context": "string",
  "sequence": int
}}]}}"""
