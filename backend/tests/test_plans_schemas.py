"""
Testes unitários para o módulo plans/schemas.py
"""
import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.plans.schemas import (
    ActionOut,
    ActionStatus,
    ActionStatusUpdate,
    GapOut,
    PlanOut,
    PlanSummary,
    Priority,
    ProgressOut,
)


class TestActionStatus:
    """Testes para o enum ActionStatus."""

    def test_pendente_value(self):
        # Assert
        assert ActionStatus.pendente.value == "pendente"

    def test_concluida_value(self):
        # Assert
        assert ActionStatus.concluida.value == "concluida"


class TestPriority:
    """Testes para o enum Priority."""

    def test_alta_value(self):
        # Assert
        assert Priority.ALTA.value == "ALTA"

    def test_media_value(self):
        # Assert
        assert Priority.MEDIA.value == "MEDIA"

    def test_baixa_value(self):
        # Assert
        assert Priority.BAIXA.value == "BAIXA"


class TestGapOut:
    """Testes para o schema GapOut."""

    def test_gap_out_creation(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "description": "Falta conhecimento em cloud",
            "relevance": 8,
        }

        # Act
        gap = GapOut(**data)

        # Assert
        assert gap.description == data["description"]
        assert gap.relevance == data["relevance"]

    def test_gap_out_from_orm(self, sample_plan):
        # Arrange
        gap_model = sample_plan.gaps[0]

        # Act
        gap_out = GapOut.model_validate(gap_model)

        # Assert
        assert gap_out.id == gap_model.id
        assert gap_out.description == gap_model.description


class TestActionOut:
    """Testes para o schema ActionOut."""

    def test_action_out_creation(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "priority": Priority.ALTA,
            "category": "Estudo",
            "title": "Estudar AWS",
            "objective": "Obter certificação",
            "context": "Cloud é essencial",
            "status": ActionStatus.pendente,
            "sequence": 1,
        }

        # Act
        action = ActionOut(**data)

        # Assert
        assert action.priority == Priority.ALTA
        assert action.status == ActionStatus.pendente
        assert action.sequence == 1

    def test_action_out_from_orm(self, sample_plan):
        # Arrange
        action_model = sample_plan.actions[0]

        # Act
        action_out = ActionOut.model_validate(action_model)

        # Assert
        assert action_out.id == action_model.id
        assert action_out.title == action_model.title


class TestPlanOut:
    """Testes para o schema PlanOut."""

    def test_plan_out_creation(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "name": "Plano de Carreira",
            "created_at": datetime.now(timezone.utc),
            "progress": 50,
            "gaps": [],
            "actions": [],
        }

        # Act
        plan = PlanOut(**data)

        # Assert
        assert plan.name == data["name"]
        assert plan.progress == 50

    def test_plan_out_from_orm(self, sample_plan):
        # Arrange & Act
        plan_out = PlanOut.model_validate(sample_plan)

        # Assert
        assert plan_out.id == sample_plan.id
        assert plan_out.name == sample_plan.name
        assert len(plan_out.actions) == 2
        assert len(plan_out.gaps) == 1


class TestPlanSummary:
    """Testes para o schema PlanSummary."""

    def test_plan_summary_creation(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "name": "Plano de Carreira",
            "created_at": datetime.now(timezone.utc),
            "progress": 75,
        }

        # Act
        summary = PlanSummary(**data)

        # Assert
        assert summary.name == data["name"]
        assert summary.progress == 75

    def test_plan_summary_from_orm(self, sample_plan):
        # Arrange & Act
        summary = PlanSummary.model_validate(sample_plan)

        # Assert
        assert summary.id == sample_plan.id
        assert summary.name == sample_plan.name


class TestProgressOut:
    """Testes para o schema ProgressOut."""

    def test_progress_out_creation(self):
        # Arrange & Act
        progress = ProgressOut(progress=50)

        # Assert
        assert progress.progress == 50

    def test_progress_out_zero(self):
        # Arrange & Act
        progress = ProgressOut(progress=0)

        # Assert
        assert progress.progress == 0

    def test_progress_out_hundred(self):
        # Arrange & Act
        progress = ProgressOut(progress=100)

        # Assert
        assert progress.progress == 100


class TestActionStatusUpdate:
    """Testes para o schema ActionStatusUpdate."""

    def test_action_status_update_pendente(self):
        # Arrange & Act
        update = ActionStatusUpdate(status=ActionStatus.pendente)

        # Assert
        assert update.status == ActionStatus.pendente

    def test_action_status_update_concluida(self):
        # Arrange & Act
        update = ActionStatusUpdate(status=ActionStatus.concluida)

        # Assert
        assert update.status == ActionStatus.concluida

    def test_invalid_status_raises_error(self):
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            ActionStatusUpdate(status="invalid_status")
