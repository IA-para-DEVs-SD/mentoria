"""
Testes unitários para o módulo profile/models.py
"""
from datetime import date, datetime

import pytest

from app.profile.models import Education, Experience, Profile


class TestProfileModel:
    """Testes para o modelo Profile."""

    def test_profile_creation(self, db_session, sample_user):
        # Arrange
        profile_data = {
            "user_id": sample_user.id,
            "career_goal": "Crescer_na_carreira_atual",
            "skills": ["Python", "FastAPI"],
        }

        # Act
        profile = Profile(**profile_data)
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)

        # Assert
        assert profile.id is not None
        assert profile.career_goal == "Crescer_na_carreira_atual"
        assert profile.skills == ["Python", "FastAPI"]
        assert profile.created_at is not None
        assert profile.updated_at is not None

    def test_profile_without_optional_fields(self, db_session, sample_user):
        # Arrange
        profile = Profile(user_id=sample_user.id)

        # Act
        db_session.add(profile)
        db_session.commit()

        # Assert
        assert profile.career_goal is None
        assert profile.skills is None

    def test_profile_user_relationship(self, db_session, sample_user, sample_profile):
        # Arrange & Act
        db_session.refresh(sample_profile)

        # Assert
        assert sample_profile.user is not None
        assert sample_profile.user.id == sample_user.id

    def test_profile_experiences_relationship(self, db_session, sample_profile):
        # Arrange & Act
        db_session.refresh(sample_profile)

        # Assert
        assert len(sample_profile.experiences) >= 1

    def test_profile_educations_relationship(self, db_session, sample_profile):
        # Arrange & Act
        db_session.refresh(sample_profile)

        # Assert
        assert len(sample_profile.educations) >= 1

    def test_profile_cascade_delete_experiences(self, db_session, sample_user, sample_profile):
        # Arrange
        profile_id = sample_profile.id
        experience_ids = [e.id for e in sample_profile.experiences]

        # Act
        db_session.delete(sample_profile)
        db_session.commit()

        # Assert
        for exp_id in experience_ids:
            exp = db_session.query(Experience).filter(Experience.id == exp_id).first()
            assert exp is None

    def test_profile_cascade_delete_educations(self, db_session, sample_user, sample_profile):
        # Arrange
        profile_id = sample_profile.id
        education_ids = [e.id for e in sample_profile.educations]

        # Act
        db_session.delete(sample_profile)
        db_session.commit()

        # Assert
        for edu_id in education_ids:
            edu = db_session.query(Education).filter(Education.id == edu_id).first()
            assert edu is None

    def test_profile_user_id_unique_constraint(self, db_session, sample_user, sample_profile):
        # Arrange
        duplicate_profile = Profile(
            user_id=sample_user.id,
            career_goal="Different goal",
        )

        # Act & Assert
        db_session.add(duplicate_profile)
        with pytest.raises(Exception):
            db_session.commit()


class TestExperienceModel:
    """Testes para o modelo Experience."""

    def test_experience_creation(self, db_session, sample_profile):
        # Arrange
        experience_data = {
            "profile_id": sample_profile.id,
            "role": "Software Engineer",
            "seniority": "Senior",
            "company": "Tech Company",
            "start_date": date(2020, 1, 1),
            "end_date": date(2023, 12, 31),
        }

        # Act
        experience = Experience(**experience_data)
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)

        # Assert
        assert experience.id is not None
        assert experience.role == "Software Engineer"
        assert experience.seniority == "Senior"
        assert experience.company == "Tech Company"

    def test_experience_without_end_date(self, db_session, sample_profile):
        # Arrange
        experience = Experience(
            profile_id=sample_profile.id,
            role="Current Role",
            seniority="Pleno",
            start_date=date(2022, 1, 1),
        )

        # Act
        db_session.add(experience)
        db_session.commit()

        # Assert
        assert experience.end_date is None

    def test_experience_without_company(self, db_session, sample_profile):
        # Arrange
        experience = Experience(
            profile_id=sample_profile.id,
            role="Freelancer",
            seniority="Senior",
            start_date=date(2020, 1, 1),
        )

        # Act
        db_session.add(experience)
        db_session.commit()

        # Assert
        assert experience.company is None

    def test_experience_profile_relationship(self, db_session, sample_profile):
        # Arrange
        experience = sample_profile.experiences[0]

        # Act
        db_session.refresh(experience)

        # Assert
        assert experience.profile is not None
        assert experience.profile.id == sample_profile.id


class TestEducationModel:
    """Testes para o modelo Education."""

    def test_education_creation(self, db_session, sample_profile):
        # Arrange
        education_data = {
            "profile_id": sample_profile.id,
            "institution": "MIT",
            "level": "Mestrado",
            "title": "Computer Science",
            "study_area": "Artificial Intelligence",
            "start_date": date(2018, 1, 1),
            "end_date": date(2020, 12, 31),
        }

        # Act
        education = Education(**education_data)
        db_session.add(education)
        db_session.commit()
        db_session.refresh(education)

        # Assert
        assert education.id is not None
        assert education.institution == "MIT"
        assert education.level == "Mestrado"
        assert education.title == "Computer Science"
        assert education.study_area == "Artificial Intelligence"

    def test_education_without_end_date(self, db_session, sample_profile):
        # Arrange
        education = Education(
            profile_id=sample_profile.id,
            institution="University",
            level="Doutorado",
            title="PhD",
            study_area="Research",
            start_date=date(2022, 1, 1),
        )

        # Act
        db_session.add(education)
        db_session.commit()

        # Assert
        assert education.end_date is None

    def test_education_profile_relationship(self, db_session, sample_profile):
        # Arrange
        education = sample_profile.educations[0]

        # Act
        db_session.refresh(education)

        # Assert
        assert education.profile is not None
        assert education.profile.id == sample_profile.id
