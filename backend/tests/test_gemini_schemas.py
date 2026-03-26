"""
Testes unitários para o módulo gemini/schemas.py
"""
import pytest
from pydantic import ValidationError

from app.gemini.schemas import GeminiActionItem, GeminiGapItem, GeminiPlanResponse


class TestGeminiActionItem:
    """Testes para o schema GeminiActionItem."""

    def test_action_item_creation(self):
        # Arrange
        data = {
            "priority": "ALTA",
            "category": "Estudo",
            "title": "Estudar AWS",
            "objective": "Obter certificação",
            "context": "Cloud é essencial",
            "sequence": 1,
        }

        # Act
        action = GeminiActionItem(**data)

        # Assert
        assert action.priority == "ALTA"
        assert action.category == "Estudo"
        assert action.title == "Estudar AWS"
        assert action.objective == "Obter certificação"
        assert action.context == "Cloud é essencial"
        assert action.sequence == 1

    def test_action_item_with_different_priorities(self):
        # Arrange
        base_data = {
            "category": "Test",
            "title": "Test",
            "objective": "Test",
            "context": "Test",
            "sequence": 1,
        }

        # Act & Assert
        for priority in ["ALTA", "MEDIA", "BAIXA"]:
            action = GeminiActionItem(priority=priority, **base_data)
            assert action.priority == priority

    def test_action_item_missing_required_field_raises_error(self):
        # Arrange
        data = {
            "priority": "ALTA",
            "category": "Estudo",
            # missing title
            "objective": "Obter certificação",
            "context": "Cloud é essencial",
            "sequence": 1,
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiActionItem(**data)


class TestGeminiGapItem:
    """Testes para o schema GeminiGapItem."""

    def test_gap_item_creation(self):
        # Arrange
        data = {
            "description": "Falta conhecimento em cloud",
            "relevance": 8,
        }

        # Act
        gap = GeminiGapItem(**data)

        # Assert
        assert gap.description == "Falta conhecimento em cloud"
        assert gap.relevance == 8

    def test_gap_item_with_zero_relevance(self):
        # Arrange
        data = {
            "description": "Low relevance gap",
            "relevance": 0,
        }

        # Act
        gap = GeminiGapItem(**data)

        # Assert
        assert gap.relevance == 0

    def test_gap_item_with_high_relevance(self):
        # Arrange
        data = {
            "description": "High relevance gap",
            "relevance": 10,
        }

        # Act
        gap = GeminiGapItem(**data)

        # Assert
        assert gap.relevance == 10

    def test_gap_item_missing_description_raises_error(self):
        # Arrange
        data = {"relevance": 5}

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiGapItem(**data)


class TestGeminiPlanResponse:
    """Testes para o schema GeminiPlanResponse."""

    def test_plan_response_creation(self):
        # Arrange
        data = {
            "plan_name": "Plano de Carreira 2024",
            "gaps": [
                {"description": "Gap 1", "relevance": 8},
                {"description": "Gap 2", "relevance": 5},
            ],
            "actions": [
                {
                    "priority": "ALTA",
                    "category": "Estudo",
                    "title": "Ação 1",
                    "objective": "Objetivo 1",
                    "context": "Contexto 1",
                    "sequence": 1,
                },
                {
                    "priority": "MEDIA",
                    "category": "Projeto",
                    "title": "Ação 2",
                    "objective": "Objetivo 2",
                    "context": "Contexto 2",
                    "sequence": 2,
                },
            ],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert response.plan_name == "Plano de Carreira 2024"
        assert len(response.gaps) == 2
        assert len(response.actions) == 2

    def test_plan_response_with_empty_gaps(self):
        # Arrange
        data = {
            "plan_name": "Plan without gaps",
            "gaps": [],
            "actions": [
                {
                    "priority": "ALTA",
                    "category": "Test",
                    "title": "Test",
                    "objective": "Test",
                    "context": "Test",
                    "sequence": 1,
                }
            ],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert len(response.gaps) == 0

    def test_plan_response_with_empty_actions(self):
        # Arrange
        data = {
            "plan_name": "Plan without actions",
            "gaps": [{"description": "Gap", "relevance": 5}],
            "actions": [],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert len(response.actions) == 0

    def test_plan_response_missing_plan_name_raises_error(self):
        # Arrange
        data = {
            "gaps": [],
            "actions": [],
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiPlanResponse(**data)

    def test_plan_response_gaps_are_gemini_gap_items(self):
        # Arrange
        data = {
            "plan_name": "Test Plan",
            "gaps": [{"description": "Gap", "relevance": 5}],
            "actions": [],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert isinstance(response.gaps[0], GeminiGapItem)

    def test_plan_response_actions_are_gemini_action_items(self):
        # Arrange
        data = {
            "plan_name": "Test Plan",
            "gaps": [],
            "actions": [
                {
                    "priority": "ALTA",
                    "category": "Test",
                    "title": "Test",
                    "objective": "Test",
                    "context": "Test",
                    "sequence": 1,
                }
            ],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert isinstance(response.actions[0], GeminiActionItem)
