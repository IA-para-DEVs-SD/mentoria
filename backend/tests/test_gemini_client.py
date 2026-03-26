"""
Testes unitários para o módulo gemini/client.py

Nota: Os testes do GeminiClient focam na validação dos schemas
e comportamento esperado. A integração com a API Gemini requer
a variável GEMINI_API_KEY configurada e é testada em testes de integração.
"""
import pytest
from pydantic import ValidationError

from app.gemini.schemas import GeminiActionItem, GeminiGapItem, GeminiPlanResponse


class TestGeminiPlanResponseValidation:
    """Testes para validação de respostas do Gemini."""

    def test_valid_plan_response(self):
        # Arrange
        data = {
            "plan_name": "Plano de Carreira",
            "gaps": [{"description": "Gap 1", "relevance": 8}],
            "actions": [
                {
                    "priority": "ALTA",
                    "category": "Estudo",
                    "title": "Ação 1",
                    "objective": "Objetivo 1",
                    "context": "Contexto 1",
                    "sequence": 1,
                }
            ],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert response.plan_name == "Plano de Carreira"
        assert len(response.gaps) == 1
        assert len(response.actions) == 1

    def test_plan_response_with_multiple_gaps_and_actions(self):
        # Arrange
        data = {
            "plan_name": "Plano Completo",
            "gaps": [
                {"description": "Gap 1", "relevance": 8},
                {"description": "Gap 2", "relevance": 5},
                {"description": "Gap 3", "relevance": 3},
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
        assert len(response.gaps) == 3
        assert len(response.actions) == 2

    def test_plan_response_empty_gaps_and_actions(self):
        # Arrange
        data = {
            "plan_name": "Plano Vazio",
            "gaps": [],
            "actions": [],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert response.plan_name == "Plano Vazio"
        assert len(response.gaps) == 0
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


class TestGeminiActionItemValidation:
    """Testes para validação de GeminiActionItem."""

    def test_valid_action_item(self):
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

    def test_action_item_all_priorities(self):
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

    def test_action_item_missing_required_field(self):
        # Arrange
        data = {
            "priority": "ALTA",
            "category": "Estudo",
            # missing title
            "objective": "Objetivo",
            "context": "Contexto",
            "sequence": 1,
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiActionItem(**data)


class TestGeminiGapItemValidation:
    """Testes para validação de GeminiGapItem."""

    def test_valid_gap_item(self):
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

    def test_gap_item_zero_relevance(self):
        # Arrange
        data = {
            "description": "Gap com baixa relevância",
            "relevance": 0,
        }

        # Act
        gap = GeminiGapItem(**data)

        # Assert
        assert gap.relevance == 0

    def test_gap_item_high_relevance(self):
        # Arrange
        data = {
            "description": "Gap crítico",
            "relevance": 10,
        }

        # Act
        gap = GeminiGapItem(**data)

        # Assert
        assert gap.relevance == 10

    def test_gap_item_missing_description(self):
        # Arrange
        data = {"relevance": 5}

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiGapItem(**data)

    def test_gap_item_missing_relevance(self):
        # Arrange
        data = {"description": "Test gap"}

        # Act & Assert
        with pytest.raises(ValidationError):
            GeminiGapItem(**data)


class TestGeminiResponseIntegration:
    """Testes de integração entre schemas Gemini."""

    def test_plan_response_contains_valid_gaps(self):
        # Arrange
        data = {
            "plan_name": "Test Plan",
            "gaps": [
                {"description": "Gap 1", "relevance": 8},
                {"description": "Gap 2", "relevance": 5},
            ],
            "actions": [],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        for gap in response.gaps:
            assert isinstance(gap, GeminiGapItem)
            assert gap.description is not None
            assert gap.relevance is not None

    def test_plan_response_contains_valid_actions(self):
        # Arrange
        data = {
            "plan_name": "Test Plan",
            "gaps": [],
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
        for action in response.actions:
            assert isinstance(action, GeminiActionItem)
            assert action.priority in ["ALTA", "MEDIA", "BAIXA"]
            assert action.title is not None

    def test_realistic_gemini_response(self):
        """Testa uma resposta realista que o Gemini poderia retornar."""
        # Arrange
        data = {
            "plan_name": "Plano de Desenvolvimento para Engenheiro de Software Senior",
            "gaps": [
                {
                    "description": "Falta experiência com arquitetura de microsserviços",
                    "relevance": 9,
                },
                {
                    "description": "Conhecimento limitado em Kubernetes",
                    "relevance": 8,
                },
                {
                    "description": "Pouca experiência com liderança técnica",
                    "relevance": 7,
                },
            ],
            "actions": [
                {
                    "priority": "ALTA",
                    "category": "Estudo",
                    "title": "Curso de Arquitetura de Microsserviços",
                    "objective": "Dominar padrões de design de microsserviços",
                    "context": "Essencial para posições senior em empresas de tecnologia",
                    "sequence": 1,
                },
                {
                    "priority": "ALTA",
                    "category": "Certificação",
                    "title": "Certificação Kubernetes (CKA)",
                    "objective": "Obter certificação oficial Kubernetes",
                    "context": "Kubernetes é padrão de mercado para orquestração",
                    "sequence": 2,
                },
                {
                    "priority": "MEDIA",
                    "category": "Projeto",
                    "title": "Liderar projeto open source",
                    "objective": "Desenvolver habilidades de liderança técnica",
                    "context": "Experiência prática em coordenação de equipes",
                    "sequence": 3,
                },
            ],
        }

        # Act
        response = GeminiPlanResponse(**data)

        # Assert
        assert response.plan_name == "Plano de Desenvolvimento para Engenheiro de Software Senior"
        assert len(response.gaps) == 3
        assert len(response.actions) == 3
        assert response.gaps[0].relevance == 9
        assert response.actions[0].priority == "ALTA"
