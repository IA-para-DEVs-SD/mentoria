"""
Testes unitários para o módulo gemini/prompts.py
"""
from datetime import date
from unittest.mock import MagicMock

import pytest

from app.gemini.prompts import (
    _format_profile_section,
    _format_rejections_section,
    build_actions_prompt,
    build_plan_prompt,
)


class TestFormatProfileSection:
    """Testes para _format_profile_section"""

    def test_formats_profile_with_all_fields(self, sample_profile):
        # Arrange & Act
        result = _format_profile_section(sample_profile)

        # Assert
        assert "PERFIL DO USUÁRIO:" in result
        assert "Objetivo:" in result
        assert "Experiências:" in result
        assert "Formação:" in result
        assert "Habilidades:" in result
        assert sample_profile.career_goal in result

    def test_includes_experience_details(self, sample_profile):
        # Arrange & Act
        result = _format_profile_section(sample_profile)

        # Assert
        experience = sample_profile.experiences[0]
        assert experience.role in result
        assert experience.seniority in result

    def test_includes_education_details(self, sample_profile):
        # Arrange & Act
        result = _format_profile_section(sample_profile)

        # Assert
        education = sample_profile.educations[0]
        assert education.institution in result
        assert education.title in result

    def test_includes_skills(self, sample_profile):
        # Arrange & Act
        result = _format_profile_section(sample_profile)

        # Assert
        for skill in sample_profile.skills:
            assert skill in result

    def test_handles_experience_without_end_date(self, db_session, sample_user):
        # Arrange
        from app.profile.models import Education, Experience, Profile

        profile = Profile(
            user_id=sample_user.id,
            career_goal="Test Goal",
            skills=["Python"],
        )
        db_session.add(profile)
        db_session.flush()

        experience = Experience(
            profile_id=profile.id,
            role="Developer",
            seniority="Pleno",
            start_date=date(2020, 1, 1),
            end_date=None,  # Current job
        )
        education = Education(
            profile_id=profile.id,
            institution="Uni",
            level="Bacharelado",
            title="CS",
            study_area="Tech",
            start_date=date(2016, 1, 1),
        )
        db_session.add(experience)
        db_session.add(education)
        db_session.commit()
        db_session.refresh(profile)

        # Act
        result = _format_profile_section(profile)

        # Assert
        assert "até o momento" in result

    def test_handles_experience_with_company(self, sample_profile):
        # Arrange & Act
        result = _format_profile_section(sample_profile)

        # Assert
        experience = sample_profile.experiences[0]
        if experience.company:
            assert experience.company in result


class TestFormatRejectionsSection:
    """Testes para _format_rejections_section"""

    def test_formats_empty_rejections(self):
        # Arrange & Act
        result = _format_rejections_section([])

        # Assert
        assert "REJEIÇÕES ANTERIORES" in result
        assert "Nenhuma" in result

    def test_formats_rejections_list(self, sample_rejection):
        # Arrange
        rejections = [sample_rejection]

        # Act
        result = _format_rejections_section(rejections)

        # Assert
        assert "REJEIÇÕES ANTERIORES" in result
        assert sample_rejection.category in result
        assert sample_rejection.action_title in result

    def test_formats_multiple_rejections(self, db_session, sample_user):
        # Arrange
        from app.plans.models import Rejection

        rejection1 = Rejection(
            user_id=sample_user.id,
            category="Estudo",
            action_title="Ação 1",
        )
        rejection2 = Rejection(
            user_id=sample_user.id,
            category="Projeto",
            action_title="Ação 2",
        )
        db_session.add(rejection1)
        db_session.add(rejection2)
        db_session.commit()

        rejections = [rejection1, rejection2]

        # Act
        result = _format_rejections_section(rejections)

        # Assert
        assert "Estudo" in result
        assert "Projeto" in result
        assert "Ação 1" in result
        assert "Ação 2" in result


class TestBuildPlanPrompt:
    """Testes para build_plan_prompt"""

    def test_builds_complete_prompt(self, sample_profile):
        # Arrange & Act
        result = build_plan_prompt(sample_profile, [])

        # Assert
        assert "PERFIL DO USUÁRIO:" in result
        assert "REJEIÇÕES ANTERIORES" in result
        assert "INSTRUÇÕES:" in result
        assert "plan_name" in result
        assert "gaps" in result
        assert "actions" in result

    def test_includes_json_schema(self, sample_profile):
        # Arrange & Act
        result = build_plan_prompt(sample_profile, [])

        # Assert
        assert '"priority": "ALTA|MEDIA|BAIXA"' in result
        assert '"category": "string"' in result
        assert '"title": "string"' in result

    def test_includes_rejections_in_prompt(self, sample_profile, sample_rejection):
        # Arrange
        rejections = [sample_rejection]

        # Act
        result = build_plan_prompt(sample_profile, rejections)

        # Assert
        assert sample_rejection.action_title in result


class TestBuildActionsPrompt:
    """Testes para build_actions_prompt"""

    def test_builds_complete_prompt(self, sample_profile):
        # Arrange & Act
        result = build_actions_prompt(sample_profile, [], [])

        # Assert
        assert "PERFIL DO USUÁRIO:" in result
        assert "REJEIÇÕES ANTERIORES" in result
        assert "AÇÕES EXISTENTES" in result
        assert "INSTRUÇÕES:" in result

    def test_includes_existing_actions(self, sample_profile, sample_plan):
        # Arrange
        existing_actions = sample_plan.actions

        # Act
        result = build_actions_prompt(sample_profile, existing_actions, [])

        # Assert
        assert "AÇÕES EXISTENTES (não duplicar):" in result
        for action in existing_actions:
            assert action.title in result
            assert action.category in result

    def test_handles_no_existing_actions(self, sample_profile):
        # Arrange & Act
        result = build_actions_prompt(sample_profile, [], [])

        # Assert
        assert "AÇÕES EXISTENTES (não duplicar):" in result
        assert "Nenhuma" in result

    def test_includes_rejections(self, sample_profile, sample_rejection):
        # Arrange
        rejections = [sample_rejection]

        # Act
        result = build_actions_prompt(sample_profile, [], rejections)

        # Assert
        assert sample_rejection.action_title in result

    def test_includes_json_schema_for_actions(self, sample_profile):
        # Arrange & Act
        result = build_actions_prompt(sample_profile, [], [])

        # Assert
        assert '"actions":' in result
        assert '"priority": "ALTA|MEDIA|BAIXA"' in result
