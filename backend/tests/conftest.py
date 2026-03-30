"""
Fixtures compartilhadas para todos os testes.
"""
import uuid
from datetime import UTC, date, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.models import User
from src.database import Base
from src.plans.models import Action, Gap, Plan, Rejection
from src.profile.models import Education, Experience, Profile

# ---------------------------------------------------------------------------
# Database Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db_engine():
    """Cria engine SQLite em memória simulando dialeto PostgreSQL para testes."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Simula o dialeto PostgreSQL para testes
    engine.dialect.name = "postgresql"

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Cria sessão de banco de dados isolada para cada teste."""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


# ---------------------------------------------------------------------------
# User Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_user_id():
    """UUID fixo para testes."""
    return uuid.UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def sample_user(db_session, sample_user_id):
    """Cria usuário de teste no banco."""
    user = User(
        id=sample_user_id,
        google_id="google_123456",
        name="Test User",
        email="test@example.com",
        photo_url="https://example.com/photo.jpg",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_user_data():
    """Dados de usuário retornados pelo Google OAuth."""
    return {
        "google_id": "google_123456",
        "name": "Test User",
        "email": "test@example.com",
        "photo_url": "https://example.com/photo.jpg",
    }


# ---------------------------------------------------------------------------
# Profile Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_profile(db_session, sample_user):
    """Cria perfil completo de teste."""
    profile = Profile(
        user_id=sample_user.id,
        career_goal="Crescer_na_carreira_atual",
        skills=["Python", "FastAPI", "SQL"],
    )
    db_session.add(profile)
    db_session.flush()

    experience = Experience(
        profile_id=profile.id,
        role="Desenvolvedor Backend",
        seniority="Pleno",
        company="Tech Corp",
        start_date=date(2020, 1, 1),
        end_date=date(2023, 12, 31),
    )
    db_session.add(experience)

    education = Education(
        profile_id=profile.id,
        institution="Universidade XYZ",
        level="Bacharelado",
        title="Ciência da Computação",
        study_area="Tecnologia",
        start_date=date(2016, 1, 1),
        end_date=date(2020, 12, 31),
    )
    db_session.add(education)

    db_session.commit()
    db_session.refresh(profile)
    return profile


@pytest.fixture
def incomplete_profile(db_session, sample_user):
    """Cria perfil incompleto (sem skills)."""
    profile = Profile(
        user_id=sample_user.id,
        career_goal="Crescer_na_carreira_atual",
        skills=None,
    )
    db_session.add(profile)
    db_session.commit()
    return profile


# ---------------------------------------------------------------------------
# Plan Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_plan(db_session, sample_user):
    """Cria plano de teste com ações e gaps."""
    plan = Plan(
        user_id=sample_user.id,
        name="Plano de Carreira 2024",
        progress=0,
    )
    db_session.add(plan)
    db_session.flush()

    gap = Gap(
        plan_id=plan.id,
        description="Falta conhecimento em cloud",
        relevance=8,
    )
    db_session.add(gap)

    action1 = Action(
        plan_id=plan.id,
        priority="ALTA",
        category="Estudo",
        title="Estudar AWS",
        objective="Obter certificação AWS",
        context="Cloud é essencial para o mercado",
        status="pendente",
        sequence=1,
    )
    action2 = Action(
        plan_id=plan.id,
        priority="MEDIA",
        category="Projeto",
        title="Criar projeto pessoal",
        objective="Aplicar conhecimentos",
        context="Prática é fundamental",
        status="pendente",
        sequence=2,
    )
    db_session.add(action1)
    db_session.add(action2)

    db_session.commit()
    db_session.refresh(plan)
    return plan


@pytest.fixture
def sample_rejection(db_session, sample_user):
    """Cria rejeição de teste."""
    rejection = Rejection(
        user_id=sample_user.id,
        category="Estudo",
        action_title="Ação rejeitada",
    )
    db_session.add(rejection)
    db_session.commit()
    return rejection


# ---------------------------------------------------------------------------
# Auth/JWT Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_jwt_token(sample_user_id):
    """Gera token JWT válido para testes."""
    from jose import jwt

    from src.config import settings

    payload = {
        "sub": str(sample_user_id),
        "exp": datetime.now(UTC) + timedelta(hours=24),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def expired_jwt_token(sample_user_id):
    """Gera token JWT expirado para testes."""
    from jose import jwt

    from src.config import settings

    payload = {
        "sub": str(sample_user_id),
        "exp": datetime.now(UTC) - timedelta(hours=1),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


# ---------------------------------------------------------------------------
# Mock Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_oauth_client():
    """Mock do cliente OAuth2."""
    with patch("src.auth.service.OAuth2Client") as mock:
        yield mock


@pytest.fixture
def mock_gemini_client():
    """Mock do cliente Gemini."""
    with patch("src.plans.service._gemini") as mock:
        yield mock
