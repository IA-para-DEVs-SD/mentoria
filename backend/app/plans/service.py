from math import floor
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.gemini.client import GeminiClient
from app.plans.models import Action, Gap, Plan, Rejection
from app.plans.schemas import ActionOut, PlanOut, PlanSummary, ProgressOut
from app.profile.models import Profile
from app.profile.service import ProfileService

_gemini = GeminiClient()
_profile_service = ProfileService()

_PLAN_NOT_FOUND = "Plano não encontrado."
_ACTION_NOT_FOUND = "Ação não encontrada."

_PRIORITY_NORMALIZE = {
    "ALTA": "ALTA",
    "MEDIA": "MEDIA",
    "MÉDIA": "MEDIA",
    "BAIXA": "BAIXA",
}


def _normalize_priority(value: str) -> str:
    return _PRIORITY_NORMALIZE.get(value.strip().upper(), "MEDIA")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def calculate_progress(completed: int, total: int) -> int:
    """Retorna percentual de conclusão (0-100). Retorna 0 se total == 0."""
    if total == 0:
        return 0
    return floor((completed / total) * 100)


def _recalculate_plan_progress(db: Session, plan: Plan) -> int:
    total = len(plan.actions)
    completed = sum(1 for a in plan.actions if a.status == "concluida")
    progress = calculate_progress(completed, total)
    plan.progress = progress
    db.flush()
    return progress


# ---------------------------------------------------------------------------
# PlanService
# ---------------------------------------------------------------------------


class PlanService:
    # ------------------------------------------------------------------
    # Geração e CRUD de planos
    # ------------------------------------------------------------------

    def generate_plan(self, db: Session, user_id: UUID) -> PlanOut:
        if not _profile_service.is_profile_complete(db, user_id):
            raise HTTPException(
                status_code=400,
                detail="Perfil incompleto. Preencha experiências, formações, habilidades e objetivo de carreira.",
            )

        rejections = db.query(Rejection).filter(Rejection.user_id == user_id).all()

        profile = (
            db.query(Profile)
            .filter(Profile.user_id == user_id)
            .first()
        )

        gemini_response = _gemini.generate_plan(profile, rejections)

        try:
            plan = Plan(
                user_id=user_id,
                name=gemini_response.plan_name,
                progress=0,
            )
            db.add(plan)
            db.flush()

            for gap_item in gemini_response.gaps:
                gap = Gap(
                    plan_id=plan.id,
                    description=gap_item.description,
                    relevance=gap_item.relevance,
                )
                db.add(gap)

            for action_item in gemini_response.actions:
                action = Action(
                    plan_id=plan.id,
                    priority=_normalize_priority(action_item.priority),
                    category=action_item.category,
                    title=action_item.title,
                    objective=action_item.objective,
                    context=action_item.context,
                    sequence=action_item.sequence,
                    status="pendente",
                )
                db.add(action)

            db.commit()
            db.refresh(plan)
        except Exception:
            db.rollback()
            raise

        return PlanOut.model_validate(plan)

    def list_plans(self, db: Session, user_id: UUID) -> list[PlanSummary]:
        plans = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.created_at.desc())
            .all()
        )
        return [PlanSummary.model_validate(p) for p in plans]

    def get_plan(self, db: Session, user_id: UUID, plan_id: UUID) -> PlanOut:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan is None:
            raise HTTPException(status_code=404, detail=_PLAN_NOT_FOUND)
        return PlanOut.model_validate(plan)

    def delete_plan(self, db: Session, user_id: UUID, plan_id: UUID) -> None:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan is None:
            raise HTTPException(status_code=404, detail=_PLAN_NOT_FOUND)
        db.delete(plan)
        db.commit()

    # ------------------------------------------------------------------
    # Gerenciamento de ações
    # ------------------------------------------------------------------

    def update_action_status(
        self,
        db: Session,
        user_id: UUID,
        plan_id: UUID,
        action_id: UUID,
        status: str,
    ) -> ActionOut:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan is None:
            raise HTTPException(status_code=404, detail=_PLAN_NOT_FOUND)

        action = db.query(Action).filter(Action.id == action_id, Action.plan_id == plan_id).first()
        if action is None:
            raise HTTPException(status_code=404, detail=_ACTION_NOT_FOUND)

        action.status = status
        db.flush()

        _recalculate_plan_progress(db, plan)
        db.commit()
        db.refresh(action)

        return ActionOut.model_validate(action)

    def delete_action(
        self,
        db: Session,
        user_id: UUID,
        plan_id: UUID,
        action_id: UUID,
    ) -> ProgressOut:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan is None:
            raise HTTPException(status_code=404, detail=_PLAN_NOT_FOUND)

        action = db.query(Action).filter(Action.id == action_id, Action.plan_id == plan_id).first()
        if action is None:
            raise HTTPException(status_code=404, detail=_ACTION_NOT_FOUND)

        if len(plan.actions) <= 1:
            raise HTTPException(
                status_code=409,
                detail="O plano deve ter pelo menos uma ação.",
            )

        rejection = Rejection(
            user_id=user_id,
            category=action.category,
            action_title=action.title,
        )
        db.add(rejection)

        db.delete(action)
        db.flush()

        # Refresh actions list after deletion
        db.refresh(plan)
        progress = _recalculate_plan_progress(db, plan)
        db.commit()

        return ProgressOut(progress=progress)

    def generate_more_actions(
        self,
        db: Session,
        user_id: UUID,
        plan_id: UUID,
    ) -> list[ActionOut]:
        plan = db.query(Plan).filter(Plan.id == plan_id, Plan.user_id == user_id).first()
        if plan is None:
            raise HTTPException(status_code=404, detail=_PLAN_NOT_FOUND)

        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        existing_actions = plan.actions
        rejections = db.query(Rejection).filter(Rejection.user_id == user_id).all()

        new_action_items = _gemini.generate_actions(profile, existing_actions, rejections)

        new_actions: list[ActionOut] = []
        for item in new_action_items:
            action = Action(
                plan_id=plan.id,
                priority=_normalize_priority(item.priority),
                category=item.category,
                title=item.title,
                objective=item.objective,
                context=item.context,
                sequence=item.sequence,
                status="pendente",
            )
            db.add(action)
            db.flush()
            new_actions.append(ActionOut.model_validate(action))

        db.refresh(plan)
        _recalculate_plan_progress(db, plan)
        db.commit()

        return new_actions
