"""Cliente Gemini — orquestra chamadas aos agentes PydanticAI."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import TYPE_CHECKING

from fastapi import HTTPException

from app.gemini.agents import actions_agent, roadmap_agent
from app.gemini.prompts import build_actions_prompt, build_plan_prompt
from app.gemini.schemas import GeminiActionItem, GeminiPlanResponse

if TYPE_CHECKING:
    from app.plans.models import Action, Rejection
    from app.profile.models import Profile

logger = logging.getLogger(__name__)
_TIMEOUT = 30
_AI_UNAVAILABLE = "Serviço de IA indisponível. Tente novamente."


class GeminiClient:
    def generate_plan(
        self,
        profile: "Profile",
        rejections: list["Rejection"],
    ) -> GeminiPlanResponse:
        prompt = build_plan_prompt(profile, rejections)
        logger.info("=== PROMPT GEMINI (generate_plan) ===\n%s\n=== FIM PROMPT ===", prompt)
        print(f"=== PROMPT GEMINI (generate_plan) ===\n{prompt}\n=== FIM PROMPT ===")
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(roadmap_agent.run_sync, prompt)
                result = future.result(timeout=_TIMEOUT)
        except FuturesTimeoutError:
            raise HTTPException(
                status_code=502,
                detail=_AI_UNAVAILABLE,
            )
        except Exception as e:
            logger.exception("Erro ao gerar plano via Gemini: %s", e)
            raise HTTPException(
                status_code=502,
                detail=_AI_UNAVAILABLE,
            )
        return result.output

    def generate_actions(
        self,
        profile: "Profile",
        existing_actions: list["Action"],
        rejections: list["Rejection"],
    ) -> list[GeminiActionItem]:
        prompt = build_actions_prompt(profile, existing_actions, rejections)
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(actions_agent.run_sync, prompt)
                result = future.result(timeout=_TIMEOUT)
        except FuturesTimeoutError:
            raise HTTPException(
                status_code=502,
                detail=_AI_UNAVAILABLE,
            )
        except Exception as e:
            logger.exception("Erro ao gerar ações via Gemini: %s", e)
            raise HTTPException(
                status_code=502,
                detail=_AI_UNAVAILABLE,
            )
        return result.output.actions
