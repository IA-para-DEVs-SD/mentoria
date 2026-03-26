"""
Testes unitários para o módulo plans/models.py
"""
import uuid
from datetime import datetime

import pytest

from app.plans.models import Action, Gap, Plan, Rejection


class TestPlanModel:
    """Testes para o modelo Plan."""

    def test_plan_creation(self, db_session, sample_user):
        # Arrange
        plan_data = {
            "user_id": sample_user.id,
            "name": "Test Plan",
            "progress": 0,
        }

        # Act
        plan = Plan(**plan_data)
        db_session.add(plan)
        db_session.commit()
        db_session.refresh(plan)

        # Assert
        assert plan.id is not None
        assert plan.name == "Test Plan"
        assert plan.progress == 0
        assert plan.created_at is not None

    def test_plan_default_progress(self, db_session, sample_user):
        # Arrange
        plan = Plan(user_id=sample_user.id, name="Default Progress Plan")

        # Act
        db_session.add(plan)
        db_session.commit()

        # Assert
        assert plan.progress == 0

    def test_plan_user_relationship(self, db_session, sample_user, sample_plan):
        # Arrange & Act
        db_session.refresh(sample_plan)

        # Assert
        assert sample_plan.user is not None
        assert sample_plan.user.id == sample_user.id

    def test_plan_actions_relationship(self, db_session, sample_plan):
        # Arrange & Act
        db_session.refresh(sample_plan)

        # Assert
        assert len(sample_plan.actions) == 2

    def test_plan_gaps_relationship(self, db_session, sample_plan):
        # Arrange & Act
        db_session.refresh(sample_plan)

        # Assert
        assert len(sample_plan.gaps) == 1

    def test_plan_cascade_delete_actions(self, db_session, sample_user, sample_plan):
        # Arrange
        plan_id = sample_plan.id
        action_ids = [a.id for a in sample_plan.actions]

        # Act
        db_session.delete(sample_plan)
        db_session.commit()

        # Assert
        for action_id in action_ids:
            action = db_session.query(Action).filter(Action.id == action_id).first()
            assert action is None

    def test_plan_cascade_delete_gaps(self, db_session, sample_user, sample_plan):
        # Arrange
        plan_id = sample_plan.id
        gap_ids = [g.id for g in sample_plan.gaps]

        # Act
        db_session.delete(sample_plan)
        db_session.commit()

        # Assert
        for gap_id in gap_ids:
            gap = db_session.query(Gap).filter(Gap.id == gap_id).first()
            assert gap is None


class TestActionModel:
    """Testes para o modelo Action."""

    def test_action_creation(self, db_session, sample_plan):
        # Arrange
        action_data = {
            "plan_id": sample_plan.id,
            "priority": "ALTA",
            "category": "Test Category",
            "title": "Test Action",
            "objective": "Test Objective",
            "context": "Test Context",
            "status": "pendente",
            "sequence": 10,
        }

        # Act
        action = Action(**action_data)
        db_session.add(action)
        db_session.commit()
        db_session.refresh(action)

        # Assert
        assert action.id is not None
        assert action.priority == "ALTA"
        assert action.status == "pendente"
        assert action.sequence == 10

    def test_action_default_status(self, db_session, sample_plan):
        # Arrange
        action = Action(
            plan_id=sample_plan.id,
            priority="MEDIA",
            category="Test",
            title="Default Status Action",
            objective="Test",
            context="Test",
            sequence=1,
        )

        # Act
        db_session.add(action)
        db_session.commit()

        # Assert
        assert action.status == "pendente"

    def test_action_default_sequence(self, db_session, sample_plan):
        # Arrange
        action = Action(
            plan_id=sample_plan.id,
            priority="BAIXA",
            category="Test",
            title="Default Sequence Action",
            objective="Test",
            context="Test",
            status="pendente",
        )

        # Act
        db_session.add(action)
        db_session.commit()

        # Assert
        assert action.sequence == 0

    def test_action_plan_relationship(self, db_session, sample_plan):
        # Arrange
        action = sample_plan.actions[0]

        # Act
        db_session.refresh(action)

        # Assert
        assert action.plan is not None
        assert action.plan.id == sample_plan.id


class TestGapModel:
    """Testes para o modelo Gap."""

    def test_gap_creation(self, db_session, sample_plan):
        # Arrange
        gap_data = {
            "plan_id": sample_plan.id,
            "description": "Test Gap Description",
            "relevance": 7,
        }

        # Act
        gap = Gap(**gap_data)
        db_session.add(gap)
        db_session.commit()
        db_session.refresh(gap)

        # Assert
        assert gap.id is not None
        assert gap.description == "Test Gap Description"
        assert gap.relevance == 7

    def test_gap_default_relevance(self, db_session, sample_plan):
        # Arrange
        gap = Gap(
            plan_id=sample_plan.id,
            description="Default Relevance Gap",
        )

        # Act
        db_session.add(gap)
        db_session.commit()

        # Assert
        assert gap.relevance == 0

    def test_gap_plan_relationship(self, db_session, sample_plan):
        # Arrange
        gap = sample_plan.gaps[0]

        # Act
        db_session.refresh(gap)

        # Assert
        assert gap.plan is not None
        assert gap.plan.id == sample_plan.id


class TestRejectionModel:
    """Testes para o modelo Rejection."""

    def test_rejection_creation(self, db_session, sample_user):
        # Arrange
        rejection_data = {
            "user_id": sample_user.id,
            "category": "Estudo",
            "action_title": "Rejected Action Title",
        }

        # Act
        rejection = Rejection(**rejection_data)
        db_session.add(rejection)
        db_session.commit()
        db_session.refresh(rejection)

        # Assert
        assert rejection.id is not None
        assert rejection.category == "Estudo"
        assert rejection.action_title == "Rejected Action Title"
        assert rejection.rejected_at is not None

    def test_rejection_default_rejected_at(self, db_session, sample_user):
        # Arrange
        rejection = Rejection(
            user_id=sample_user.id,
            category="Test",
            action_title="Test Action",
        )

        # Act
        db_session.add(rejection)
        db_session.commit()

        # Assert
        assert rejection.rejected_at is not None
        assert isinstance(rejection.rejected_at, datetime)
