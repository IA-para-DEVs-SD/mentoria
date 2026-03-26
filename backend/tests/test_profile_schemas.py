"""
Testes unitários para o módulo profile/schemas.py
"""
import uuid
from datetime import date, datetime

import pytest
from pydantic import ValidationError

from app.profile.schemas import (
    CareerGoal,
    EducationIn,
    EducationLevel,
    EducationOut,
    ExperienceIn,
    ExperienceOut,
    ProfileIn,
    ProfileOut,
    Seniority,
    _strip_control_chars,
)


class TestStripControlChars:
    """Testes para a função _strip_control_chars."""

    def test_removes_control_characters(self):
        # Arrange
        text_with_control = "Hello\x00World\x1F"

        # Act
        result = _strip_control_chars(text_with_control)

        # Assert
        assert result == "HelloWorld"

    def test_preserves_allowed_whitespace(self):
        # Arrange
        text = "Hello\tWorld\nNew Line\rCarriage"

        # Act
        result = _strip_control_chars(text)

        # Assert
        assert "\t" in result
        assert "\n" in result
        assert "\r" in result

    def test_preserves_normal_text(self):
        # Arrange
        text = "Normal text with spaces and números 123"

        # Act
        result = _strip_control_chars(text)

        # Assert
        assert result == text


class TestExperienceIn:
    """Testes para o schema ExperienceIn."""

    def test_valid_experience_creation(self):
        # Arrange
        data = {
            "role": "Developer",
            "seniority": Seniority.Pleno,
            "company": "Tech Corp",
            "start_date": date(2020, 1, 1),
            "end_date": date(2023, 12, 31),
        }

        # Act
        experience = ExperienceIn(**data)

        # Assert
        assert experience.role == "Developer"
        assert experience.seniority == Seniority.Pleno
        assert experience.company == "Tech Corp"

    def test_experience_without_end_date(self):
        # Arrange
        data = {
            "role": "Developer",
            "seniority": Seniority.Junior,
            "start_date": date(2020, 1, 1),
        }

        # Act
        experience = ExperienceIn(**data)

        # Assert
        assert experience.end_date is None

    def test_experience_without_company(self):
        # Arrange
        data = {
            "role": "Freelancer",
            "seniority": Seniority.Senior,
            "start_date": date(2020, 1, 1),
        }

        # Act
        experience = ExperienceIn(**data)

        # Assert
        assert experience.company is None

    def test_future_start_date_raises_error(self):
        # Arrange
        data = {
            "role": "Developer",
            "seniority": Seniority.Pleno,
            "start_date": date(2030, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ExperienceIn(**data)
        assert "start_date não pode ser futura" in str(exc_info.value)

    def test_end_date_before_start_date_raises_error(self):
        # Arrange
        data = {
            "role": "Developer",
            "seniority": Seniority.Pleno,
            "start_date": date(2022, 1, 1),
            "end_date": date(2021, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ExperienceIn(**data)
        assert "end_date deve ser maior ou igual a start_date" in str(exc_info.value)

    def test_future_end_date_raises_error(self):
        # Arrange
        data = {
            "role": "Developer",
            "seniority": Seniority.Pleno,
            "start_date": date(2020, 1, 1),
            "end_date": date(2030, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ExperienceIn(**data)
        assert "end_date não pode ser futura" in str(exc_info.value)

    def test_empty_role_raises_error(self):
        # Arrange
        data = {
            "role": "",
            "seniority": Seniority.Pleno,
            "start_date": date(2020, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ExperienceIn(**data)

    def test_sanitizes_control_characters_in_role(self):
        # Arrange
        data = {
            "role": "Developer\x00",
            "seniority": Seniority.Pleno,
            "start_date": date(2020, 1, 1),
        }

        # Act
        experience = ExperienceIn(**data)

        # Assert
        assert "\x00" not in experience.role


class TestEducationIn:
    """Testes para o schema EducationIn."""

    def test_valid_education_creation(self):
        # Arrange
        data = {
            "institution": "University",
            "level": EducationLevel.Bacharelado,
            "title": "Computer Science",
            "study_area": "Technology",
            "start_date": date(2016, 1, 1),
            "end_date": date(2020, 12, 31),
        }

        # Act
        education = EducationIn(**data)

        # Assert
        assert education.institution == "University"
        assert education.level == EducationLevel.Bacharelado

    def test_education_without_end_date(self):
        # Arrange
        data = {
            "institution": "University",
            "level": EducationLevel.Mestrado,
            "title": "Software Engineering",
            "study_area": "Technology",
            "start_date": date(2022, 1, 1),
        }

        # Act
        education = EducationIn(**data)

        # Assert
        assert education.end_date is None

    def test_future_start_date_raises_error(self):
        # Arrange
        data = {
            "institution": "University",
            "level": EducationLevel.Bacharelado,
            "title": "CS",
            "study_area": "Tech",
            "start_date": date(2030, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            EducationIn(**data)
        assert "start_date não pode ser futura" in str(exc_info.value)

    def test_end_date_before_start_date_raises_error(self):
        # Arrange
        data = {
            "institution": "University",
            "level": EducationLevel.Bacharelado,
            "title": "CS",
            "study_area": "Tech",
            "start_date": date(2020, 1, 1),
            "end_date": date(2019, 1, 1),
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            EducationIn(**data)
        assert "end_date deve ser maior ou igual a start_date" in str(exc_info.value)


class TestProfileIn:
    """Testes para o schema ProfileIn."""

    def test_valid_profile_creation(self):
        # Arrange
        data = {
            "experiences": [
                {
                    "role": "Developer",
                    "seniority": "Pleno",
                    "start_date": date(2020, 1, 1),
                }
            ],
            "educations": [
                {
                    "institution": "University",
                    "level": "Bacharelado",
                    "title": "CS",
                    "study_area": "Tech",
                    "start_date": date(2016, 1, 1),
                }
            ],
            "skills": ["Python", "FastAPI"],
            "career_goal": "Crescer_na_carreira_atual",
        }

        # Act
        profile = ProfileIn(**data)

        # Assert
        assert len(profile.experiences) == 1
        assert len(profile.educations) == 1
        assert profile.skills == ["Python", "FastAPI"]
        assert profile.career_goal == CareerGoal.Crescer_na_carreira_atual

    def test_empty_experiences_raises_error(self):
        # Arrange
        data = {
            "experiences": [],
            "educations": [
                {
                    "institution": "University",
                    "level": "Bacharelado",
                    "title": "CS",
                    "study_area": "Tech",
                    "start_date": date(2016, 1, 1),
                }
            ],
            "skills": ["Python"],
            "career_goal": "Crescer_na_carreira_atual",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ProfileIn(**data)

    def test_empty_educations_raises_error(self):
        # Arrange
        data = {
            "experiences": [
                {
                    "role": "Developer",
                    "seniority": "Pleno",
                    "start_date": date(2020, 1, 1),
                }
            ],
            "educations": [],
            "skills": ["Python"],
            "career_goal": "Crescer_na_carreira_atual",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ProfileIn(**data)

    def test_empty_skills_raises_error(self):
        # Arrange
        data = {
            "experiences": [
                {
                    "role": "Developer",
                    "seniority": "Pleno",
                    "start_date": date(2020, 1, 1),
                }
            ],
            "educations": [
                {
                    "institution": "University",
                    "level": "Bacharelado",
                    "title": "CS",
                    "study_area": "Tech",
                    "start_date": date(2016, 1, 1),
                }
            ],
            "skills": [],
            "career_goal": "Crescer_na_carreira_atual",
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            ProfileIn(**data)

    def test_sanitizes_skills(self):
        # Arrange
        data = {
            "experiences": [
                {
                    "role": "Developer",
                    "seniority": "Pleno",
                    "start_date": date(2020, 1, 1),
                }
            ],
            "educations": [
                {
                    "institution": "University",
                    "level": "Bacharelado",
                    "title": "CS",
                    "study_area": "Tech",
                    "start_date": date(2016, 1, 1),
                }
            ],
            "skills": ["Python\x00", "FastAPI\x1F"],
            "career_goal": "Crescer_na_carreira_atual",
        }

        # Act
        profile = ProfileIn(**data)

        # Assert
        assert profile.skills == ["Python", "FastAPI"]


class TestProfileOut:
    """Testes para o schema ProfileOut."""

    def test_profile_out_from_orm(self, sample_profile):
        # Arrange & Act
        profile_out = ProfileOut.model_validate(sample_profile)

        # Assert
        assert profile_out.id == sample_profile.id
        assert profile_out.career_goal.value == sample_profile.career_goal
        assert profile_out.skills == sample_profile.skills
