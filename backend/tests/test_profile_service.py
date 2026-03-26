"""
Testes unitários para o módulo profile/service.py
"""
from datetime import date

import pytest

from app.profile.models import Education, Experience, Profile
from app.profile.schemas import (
    CareerGoal,
    EducationIn,
    EducationLevel,
    ExperienceIn,
    ProfileIn,
    Seniority,
)
from app.profile.service import ProfileService


class TestProfileServiceGetProfile:
    """Testes para ProfileService.get_profile"""

    def test_get_profile_returns_existing_profile(self, db_session, sample_profile):
        # Arrange
        service = ProfileService()

        # Act
        result = service.get_profile(db_session, sample_profile.user_id)

        # Assert
        assert result is not None
        assert result.id == sample_profile.id
        assert result.career_goal == sample_profile.career_goal

    def test_get_profile_returns_none_when_not_exists(self, db_session, sample_user_id):
        # Arrange
        service = ProfileService()

        # Act
        result = service.get_profile(db_session, sample_user_id)

        # Assert
        assert result is None


class TestProfileServiceUpsertProfile:
    """Testes para ProfileService.upsert_profile"""

    def test_upsert_creates_new_profile(self, db_session, sample_user):
        # Arrange
        service = ProfileService()
        profile_in = ProfileIn(
            experiences=[
                ExperienceIn(
                    role="Developer",
                    seniority=Seniority.Pleno,
                    company="Tech Corp",
                    start_date=date(2020, 1, 1),
                    end_date=date(2023, 12, 31),
                )
            ],
            educations=[
                EducationIn(
                    institution="University",
                    level=EducationLevel.Bacharelado,
                    title="Computer Science",
                    study_area="Technology",
                    start_date=date(2016, 1, 1),
                    end_date=date(2020, 12, 31),
                )
            ],
            skills=["Python", "FastAPI"],
            career_goal=CareerGoal.Crescer_na_carreira_atual,
        )

        # Act
        result = service.upsert_profile(db_session, sample_user.id, profile_in)

        # Assert
        assert result is not None
        assert result.career_goal == CareerGoal.Crescer_na_carreira_atual
        assert result.skills == ["Python", "FastAPI"]
        assert len(result.experiences) == 1
        assert len(result.educations) == 1

    def test_upsert_updates_existing_profile(self, db_session, sample_user, sample_profile):
        # Arrange
        service = ProfileService()
        new_profile_in = ProfileIn(
            experiences=[
                ExperienceIn(
                    role="Senior Developer",
                    seniority=Seniority.Senior,
                    company="New Corp",
                    start_date=date(2021, 1, 1),
                )
            ],
            educations=[
                EducationIn(
                    institution="New University",
                    level=EducationLevel.Mestrado,
                    title="Software Engineering",
                    study_area="Technology",
                    start_date=date(2020, 1, 1),
                )
            ],
            skills=["Python", "FastAPI", "AWS"],
            career_goal=CareerGoal.Assumir_cargos_de_lideranca,
        )

        # Act
        result = service.upsert_profile(db_session, sample_user.id, new_profile_in)

        # Assert
        assert result.career_goal == CareerGoal.Assumir_cargos_de_lideranca
        assert "AWS" in result.skills
        assert len(result.experiences) == 1
        assert result.experiences[0].role == "Senior Developer"

    def test_upsert_replaces_experiences_and_educations(self, db_session, sample_user, sample_profile):
        # Arrange
        service = ProfileService()
        original_exp_count = len(sample_profile.experiences)
        original_edu_count = len(sample_profile.educations)

        new_profile_in = ProfileIn(
            experiences=[
                ExperienceIn(
                    role="Role 1",
                    seniority=Seniority.Junior,
                    start_date=date(2020, 1, 1),
                ),
                ExperienceIn(
                    role="Role 2",
                    seniority=Seniority.Pleno,
                    start_date=date(2022, 1, 1),
                ),
            ],
            educations=[
                EducationIn(
                    institution="Uni 1",
                    level=EducationLevel.Tecnico,
                    title="Title 1",
                    study_area="Area 1",
                    start_date=date(2015, 1, 1),
                ),
            ],
            skills=["Skill1"],
            career_goal=CareerGoal.Mudar_de_area,
        )

        # Act
        result = service.upsert_profile(db_session, sample_user.id, new_profile_in)

        # Assert
        assert len(result.experiences) == 2
        assert len(result.educations) == 1


class TestProfileServiceIsProfileComplete:
    """Testes para ProfileService.is_profile_complete"""

    def test_complete_profile_returns_true(self, db_session, sample_profile):
        # Arrange
        service = ProfileService()

        # Act
        result = service.is_profile_complete(db_session, sample_profile.user_id)

        # Assert
        assert result is True

    def test_no_profile_returns_false(self, db_session, sample_user_id):
        # Arrange
        service = ProfileService()

        # Act
        result = service.is_profile_complete(db_session, sample_user_id)

        # Assert
        assert result is False

    def test_profile_without_skills_returns_false(self, db_session, sample_user):
        # Arrange
        service = ProfileService()
        profile = Profile(
            user_id=sample_user.id,
            career_goal="Crescer_na_carreira_atual",
            skills=None,
        )
        db_session.add(profile)
        db_session.flush()

        experience = Experience(
            profile_id=profile.id,
            role="Dev",
            seniority="Pleno",
            start_date=date(2020, 1, 1),
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

        # Act
        result = service.is_profile_complete(db_session, sample_user.id)

        # Assert
        assert result is False

    def test_profile_without_career_goal_returns_false(self, db_session, sample_user):
        # Arrange
        service = ProfileService()
        profile = Profile(
            user_id=sample_user.id,
            career_goal=None,
            skills=["Python"],
        )
        db_session.add(profile)
        db_session.flush()

        experience = Experience(
            profile_id=profile.id,
            role="Dev",
            seniority="Pleno",
            start_date=date(2020, 1, 1),
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

        # Act
        result = service.is_profile_complete(db_session, sample_user.id)

        # Assert
        assert result is False

    def test_profile_without_experience_returns_false(self, db_session, sample_user):
        # Arrange
        service = ProfileService()
        profile = Profile(
            user_id=sample_user.id,
            career_goal="Crescer_na_carreira_atual",
            skills=["Python"],
        )
        db_session.add(profile)
        db_session.flush()

        education = Education(
            profile_id=profile.id,
            institution="Uni",
            level="Bacharelado",
            title="CS",
            study_area="Tech",
            start_date=date(2016, 1, 1),
        )
        db_session.add(education)
        db_session.commit()

        # Act
        result = service.is_profile_complete(db_session, sample_user.id)

        # Assert
        assert result is False

    def test_profile_without_education_returns_false(self, db_session, sample_user):
        # Arrange
        service = ProfileService()
        profile = Profile(
            user_id=sample_user.id,
            career_goal="Crescer_na_carreira_atual",
            skills=["Python"],
        )
        db_session.add(profile)
        db_session.flush()

        experience = Experience(
            profile_id=profile.id,
            role="Dev",
            seniority="Pleno",
            start_date=date(2020, 1, 1),
        )
        db_session.add(experience)
        db_session.commit()

        # Act
        result = service.is_profile_complete(db_session, sample_user.id)

        # Assert
        assert result is False
