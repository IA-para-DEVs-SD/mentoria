from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.dependencies import get_current_user, get_db
from app.plans.schemas import (
    ActionOut,
    ActionStatusUpdate,
    PlanOut,
    PlanSummary,
    ProgressOut,
)
from app.plans.service import PlanService

router = APIRouter(prefix="/plans", tags=["plans"])
_service = PlanService()


@router.get("", response_model=list[PlanSummary])
def list_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.list_plans(db, current_user.id)


@router.post("", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def generate_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.generate_plan(db, current_user.id)


@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.get_plan(db, current_user.id, plan_id)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _service.delete_plan(db, current_user.id, plan_id)


@router.patch("/{plan_id}/actions/{action_id}", response_model=ActionOut)
def update_action_status(
    plan_id: UUID,
    action_id: UUID,
    body: ActionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.update_action_status(db, current_user.id, plan_id, action_id, body.status)


@router.delete("/{plan_id}/actions/{action_id}", response_model=ProgressOut)
def delete_action(
    plan_id: UUID,
    action_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.delete_action(db, current_user.id, plan_id, action_id)


@router.post("/{plan_id}/actions/generate", response_model=list[ActionOut])
def generate_more_actions(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.generate_more_actions(db, current_user.id, plan_id)
