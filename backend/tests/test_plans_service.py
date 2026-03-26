"""
Testes unitários para o módulo plans/service.py
"""
import sys
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

# Mock the gemini modules before importing PlanService
sys.modules["app.gemini.agents"] = MagicMock()
sys.modules["app.gemini.client"] = MagicMock()

from app.gemini.schemas import GeminiActionItem, GeminiGapItem, GeminiPlanResponse
from app.plans.models import Action, Gap, Plan, Rejection
from app.plans.service import PlanService, calculate_progress


class TestCalculateProgress:
    """Testes para a função calculate_progress."""

    def test_zero_total_returns_zero(self):
        # Arrange & Act
        result = calculate_progress(0, 0)

        # Assert
        assert result == 0

    def test_no_completed_returns_zero(self):
        # Arrange & Act
        result = calculate_progress(0, 10)

        # Assert
        assert result == 0

    def test_all_completed_returns_100(self):
        # Arrange & Act
        result = calculate_progress(10, 10)

        # Assert
        assert result == 100

    def test_partial_completion(self):
        # Arrange & Act
        result = calculate_progress(5, 10)

        # Assert
        assert result == 50

    def test_floors_result(self):
        # Arrange & Act
        result = calculate_progress(1, 3)

        # Assert
        assert result == 33  # floor(33.33)


class TestPlanServiceListPlans:
    """Testes para PlanService.list_plans"""

    def test_returns_empty_list_when_no_plans(self, db_session, sample_user):
        # Arrange
        service = PlanService()

        # Act
        result = service.list_plans(db_session, sample_user.id)

        # Assert
        assert result == []

    def test_returns_user_plans(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()

        # Act
        result = service.list_plans(db_session, sample_user.id)

        # Assert
        assert len(result) == 1
        assert result[0].id == sample_plan.id
        assert result[0].name == sample_plan.name

    def test_returns_plans_ordered_by_created_at_desc(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        plan1 = Plan(user_id=sample_user.id, name="Plan 1", progress=0)
        plan2 = Plan(user_id=sample_user.id, name="Plan 2", progress=0)
        db_session.add(plan1)
        db_session.add(plan2)
        db_session.commit()

        # Act
        result = service.list_plans(db_session, sample_user.id)

        # Assert
        assert len(result) == 2
        assert result[0].name == "Plan 2"  # Most recent first


class TestPlanServiceGetPlan:
    """Testes para PlanService.get_plan"""

    def test_returns_plan_when_exists(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()

        # Act
        result = service.get_plan(db_session, sample_user.id, sample_plan.id)

        # Assert
        assert result.id == sample_plan.id
        assert result.name == sample_plan.name
        assert len(result.actions) == 2
        assert len(result.gaps) == 1

    def test_raises_404_when_plan_not_found(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        non_existent_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_plan(db_session, sample_user.id, non_existent_id)

        assert exc_info.value.status_code == 404
        assert "Plano não encontrado" in exc_info.value.detail

    def test_raises_404_when_plan_belongs_to_other_user(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        other_user_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_plan(db_session, other_user_id, sample_plan.id)

        assert exc_info.value.status_code == 404


class TestPlanServiceDeletePlan:
    """Testes para PlanService.delete_plan"""

    def test_deletes_plan_successfully(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        plan_id = sample_plan.id

        # Act
        service.delete_plan(db_session, sample_user.id, plan_id)

        # Assert
        deleted_plan = db_session.query(Plan).filter(Plan.id == plan_id).first()
        assert deleted_plan is None

    def test_raises_404_when_plan_not_found(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        non_existent_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_plan(db_session, sample_user.id, non_existent_id)

        assert exc_info.value.status_code == 404


class TestPlanServiceGeneratePlan:
    """Testes para PlanService.generate_plan"""

    def test_raises_400_when_profile_incomplete(self, db_session, sample_user):
        # Arrange
        service = PlanService()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.generate_plan(db_session, sample_user.id)

        assert exc_info.value.status_code == 400
        assert "Perfil incompleto" in exc_info.value.detail

    def test_generates_plan_successfully(self, db_session, sample_user, sample_profile):
        # Arrange
        service = PlanService()
        mock_response = GeminiPlanResponse(
            plan_name="Plano de Carreira",
            gaps=[GeminiGapItem(description="Gap 1", relevance=8)],
            actions=[
                GeminiActionItem(
                    priority="ALTA",
                    category="Estudo",
                    title="Ação 1",
                    objective="Objetivo 1",
                    context="Contexto 1",
                    sequence=1,
                )
            ],
        )

        with patch("app.plans.service._gemini") as mock_gemini:
            mock_gemini.generate_plan.return_value = mock_response

            # Act
            result = service.generate_plan(db_session, sample_user.id)

            # Assert
            assert result.name == "Plano de Carreira"
            assert len(result.gaps) == 1
            assert len(result.actions) == 1
            assert result.progress == 0


class TestPlanServiceUpdateActionStatus:
    """Testes para PlanService.update_action_status"""

    def test_updates_action_status_to_concluida(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        action = sample_plan.actions[0]

        # Act
        result = service.update_action_status(
            db_session, sample_user.id, sample_plan.id, action.id, "concluida"
        )

        # Assert
        assert result.status.value == "concluida"

    def test_updates_plan_progress_when_action_completed(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        action = sample_plan.actions[0]

        # Act
        service.update_action_status(
            db_session, sample_user.id, sample_plan.id, action.id, "concluida"
        )

        # Assert
        db_session.refresh(sample_plan)
        assert sample_plan.progress == 50  # 1 of 2 actions completed

    def test_raises_404_when_plan_not_found(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        non_existent_plan_id = uuid.uuid4()
        action_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_action_status(
                db_session, sample_user.id, non_existent_plan_id, action_id, "concluida"
            )

        assert exc_info.value.status_code == 404
        assert "Plano não encontrado" in exc_info.value.detail

    def test_raises_404_when_action_not_found(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        non_existent_action_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_action_status(
                db_session, sample_user.id, sample_plan.id, non_existent_action_id, "concluida"
            )

        assert exc_info.value.status_code == 404
        assert "Ação não encontrada" in exc_info.value.detail


class TestPlanServiceDeleteAction:
    """Testes para PlanService.delete_action"""

    def test_deletes_action_and_creates_rejection(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        action = sample_plan.actions[0]
        action_id = action.id
        action_title = action.title
        action_category = action.category

        # Act
        result = service.delete_action(
            db_session, sample_user.id, sample_plan.id, action_id
        )

        # Assert
        deleted_action = db_session.query(Action).filter(Action.id == action_id).first()
        assert deleted_action is None

        rejection = db_session.query(Rejection).filter(
            Rejection.user_id == sample_user.id,
            Rejection.action_title == action_title,
        ).first()
        assert rejection is not None
        assert rejection.category == action_category

    def test_raises_409_when_only_one_action_remains(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        plan = Plan(user_id=sample_user.id, name="Single Action Plan", progress=0)
        db_session.add(plan)
        db_session.flush()

        action = Action(
            plan_id=plan.id,
            priority="ALTA",
            category="Test",
            title="Only Action",
            objective="Test",
            context="Test",
            status="pendente",
            sequence=1,
        )
        db_session.add(action)
        db_session.commit()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_action(db_session, sample_user.id, plan.id, action.id)

        assert exc_info.value.status_code == 409
        assert "pelo menos uma ação" in exc_info.value.detail

    def test_recalculates_progress_after_deletion(self, db_session, sample_user, sample_plan):
        # Arrange
        service = PlanService()
        # Complete one action first
        action_to_complete = sample_plan.actions[0]
        action_to_complete.status = "concluida"
        db_session.commit()

        action_to_delete = sample_plan.actions[1]

        # Act
        result = service.delete_action(
            db_session, sample_user.id, sample_plan.id, action_to_delete.id
        )

        # Assert
        assert result.progress == 100  # 1 of 1 remaining action is completed


class TestPlanServiceGenerateMoreActions:
    """Testes para PlanService.generate_more_actions"""

    def test_generates_new_actions(self, db_session, sample_user, sample_plan, sample_profile):
        # Arrange
        service = PlanService()
        new_actions = [
            GeminiActionItem(
                priority="MEDIA",
                category="Networking",
                title="Nova Ação",
                objective="Novo Objetivo",
                context="Novo Contexto",
                sequence=3,
            )
        ]

        with patch("app.plans.service._gemini") as mock_gemini:
            mock_gemini.generate_actions.return_value = new_actions

            # Act
            result = service.generate_more_actions(
                db_session, sample_user.id, sample_plan.id
            )

            # Assert
            assert len(result) == 1
            assert result[0].title == "Nova Ação"

    def test_raises_404_when_plan_not_found(self, db_session, sample_user):
        # Arrange
        service = PlanService()
        non_existent_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.generate_more_actions(db_session, sample_user.id, non_existent_id)

        assert exc_info.value.status_code == 404
