"""
Testes de integração para endpoints da API.
Cobre: POST/GET/DELETE /plans, POST /profile,
PATCH/DELETE /plans/{id}/actions/{id}, e exception handler.

Issue #84
"""
import sys
import uuid
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.auth.models import User
from src.database import Base
from src.dependencies import get_current_user, get_db
from src.gemini.schemas import GeminiActionItem, GeminiGapItem, GeminiPlanResponse
from src.main import app
from src.plans.models import Action, Gap, Plan
from src.profile.models import Education, Experience, Profile

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def test_user(test_session):
    user = User(
        id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        google_id="google_test",
        name="Test User",
        email="test@test.com",
        photo_url="https://example.com/photo.jpg",
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def test_profile(test_session, test_user):
    profile = Profile(
        user_id=test_user.id,
        career_goal="Crescer_na_carreira_atual",
        skills=["Python", "FastAPI"],
    )
    test_session.add(profile)
    test_session.flush()
    test_session.add(Experience(
        profile_id=profile.id, role="Dev", seniority="Pleno",
        company="Corp", start_date=date(2020, 1, 1),
    ))
    test_session.add(Education(
        profile_id=profile.id, institution="Uni", level="Bacharelado",
        title="CS", study_area="Tech", start_date=date(2016, 1, 1),
    ))
    test_session.commit()
    test_session.refresh(profile)
    return profile


@pytest.fixture
def test_plan(test_session, test_user):
    plan = Plan(user_id=test_user.id, name="Plano Teste", progress=0)
    test_session.add(plan)
    test_session.flush()
    test_session.add(Gap(plan_id=plan.id, description="Gap 1", relevance=8))
    test_session.add(Action(
        plan_id=plan.id, priority="ALTA", category="Estudo",
        title="Ação 1", objective="Obj 1", context="Ctx 1",
        status="pendente", sequence=1,
    ))
    test_session.add(Action(
        plan_id=plan.id, priority="MEDIA", category="Projeto",
        title="Ação 2", objective="Obj 2", context="Ctx 2",
        status="pendente", sequence=2,
    ))
    test_session.commit()
    test_session.refresh(plan)
    return plan


@pytest.fixture
def client(test_engine, test_session, test_user):
    """TestClient com dependências sobrescritas."""
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def _override_db():
        session = TestSession()
        try:
            yield session
        finally:
            session.close()

    def _override_user():
        return test_user

    app.dependency_overrides[get_db] = _override_db
    app.dependency_overrides[get_current_user] = _override_user
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 1. POST /plans — Geração de plano via API
# ---------------------------------------------------------------------------

class TestPostPlans:
    def test_generate_plan_returns_201(self, client, test_profile):
        mock_response = GeminiPlanResponse(
            plan_name="Plano Gerado",
            gaps=[GeminiGapItem(description="Gap IA", relevance=9)],
            actions=[GeminiActionItem(
                priority="ALTA", category="Estudo", title="Ação IA",
                objective="Obj", context="Ctx", sequence=1,
            )],
        )
        with patch("src.plans.service._gemini") as mock_gemini:
            mock_gemini.generate_plan.return_value = mock_response
            resp = client.post("/plans")

        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Plano Gerado"
        assert len(data["gaps"]) == 1
        assert len(data["actions"]) == 1
        assert data["progress"] == 0


# ---------------------------------------------------------------------------
# 2. GET /plans — Listagem de planos via API
# ---------------------------------------------------------------------------

class TestGetPlans:
    def test_list_plans_returns_200(self, client, test_plan):
        resp = client.get("/plans")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Plano Teste"
        assert "progress" in data[0]
        assert "created_at" in data[0]


# ---------------------------------------------------------------------------
# 3. DELETE /plans/{id} — Exclusão de plano via API
# ---------------------------------------------------------------------------

class TestDeletePlan:
    def test_delete_plan_returns_204(self, client, test_plan):
        resp = client.delete(f"/plans/{test_plan.id}")
        assert resp.status_code == 204

    def test_delete_nonexistent_plan_returns_404(self, client):
        fake_id = uuid.uuid4()
        resp = client.delete(f"/plans/{fake_id}")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# 4. POST /profile — Upsert de perfil via API
# ---------------------------------------------------------------------------

class TestPostProfile:
    def test_upsert_profile_returns_200(self, client, test_user):
        payload = {
            "experiences": [{
                "role": "Developer",
                "seniority": "Pleno",
                "company": "Corp",
                "start_date": "2020-01-01",
                "end_date": None,
            }],
            "educations": [{
                "institution": "Uni",
                "level": "Bacharelado",
                "title": "CS",
                "study_area": "Tech",
                "start_date": "2016-01-01",
                "end_date": "2020-12-31",
            }],
            "skills": ["Python", "SQL"],
            "career_goal": "Crescer_na_carreira_atual",
        }
        resp = client.post("/profile", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["career_goal"] == "Crescer_na_carreira_atual"
        assert data["skills"] == ["Python", "SQL"]
        assert len(data["experiences"]) == 1
        assert len(data["educations"]) == 1


# ---------------------------------------------------------------------------
# 5 & 6. Testes do GeminiClient (timeout e exceção)
# ---------------------------------------------------------------------------

class TestGeminiClientErrors:
    @staticmethod
    def _get_real_module():
        """Reimporta o módulo real removendo mocks de sys.modules temporariamente."""
        import importlib

        saved = {}
        for key in list(sys.modules.keys()):
            if key.startswith("src.gemini"):
                saved[key] = sys.modules.pop(key)
        try:
            mod = importlib.import_module("src.gemini.client")
            return mod, saved
        except Exception:
            sys.modules.update(saved)
            raise

    @staticmethod
    def _restore_modules(saved):
        for key in list(sys.modules.keys()):
            if key.startswith("src.gemini") and key not in saved:
                del sys.modules[key]
        sys.modules.update(saved)

    def test_timeout_raises_502(self):
        from concurrent.futures import TimeoutError as FuturesTimeoutError

        from fastapi import HTTPException

        mod, saved = self._get_real_module()
        try:
            gemini_client = mod.GeminiClient()
            mock_profile = MagicMock()
            mock_profile.experiences = []
            mock_profile.educations = []
            mock_profile.skills = []
            mock_profile.career_goal = "Test"

            original_agent = mod.roadmap_agent
            mock_agent = MagicMock()
            mock_agent.run_sync.side_effect = FuturesTimeoutError()
            mod.roadmap_agent = mock_agent
            try:
                with pytest.raises(HTTPException) as exc_info:
                    gemini_client.generate_plan(mock_profile, [])

                assert exc_info.value.status_code == 502
                assert "indisponível" in exc_info.value.detail
            finally:
                mod.roadmap_agent = original_agent
        finally:
            self._restore_modules(saved)

    def test_generic_exception_raises_502(self):
        from fastapi import HTTPException

        mod, saved = self._get_real_module()
        try:
            gemini_client = mod.GeminiClient()
            mock_profile = MagicMock()
            mock_profile.experiences = []
            mock_profile.educations = []
            mock_profile.skills = []
            mock_profile.career_goal = "Test"

            original_agent = mod.roadmap_agent
            mock_agent = MagicMock()
            mock_agent.run_sync.side_effect = RuntimeError("API error")
            mod.roadmap_agent = mock_agent
            try:
                with pytest.raises(HTTPException) as exc_info:
                    gemini_client.generate_plan(mock_profile, [])

                assert exc_info.value.status_code == 502
            finally:
                mod.roadmap_agent = original_agent
        finally:
            self._restore_modules(saved)


# ---------------------------------------------------------------------------
# 7. Normalização de prioridade
# ---------------------------------------------------------------------------

class TestNormalizePriority:
    def test_media_with_accent(self):
        from src.plans.service import _normalize_priority
        assert _normalize_priority("MÉDIA") == "MEDIA"

    def test_unknown_value_defaults_to_media(self):
        from src.plans.service import _normalize_priority
        assert _normalize_priority("INVALIDO") == "MEDIA"

    def test_strips_whitespace(self):
        from src.plans.service import _normalize_priority
        assert _normalize_priority("  ALTA  ") == "ALTA"

    def test_case_insensitive(self):
        from src.plans.service import _normalize_priority
        assert _normalize_priority("baixa") == "BAIXA"


# ---------------------------------------------------------------------------
# 8. PATCH /plans/{id}/actions/{id} — Atualizar status da ação via API
# ---------------------------------------------------------------------------

class TestPatchActionStatus:
    def test_mark_action_as_concluida(self, client, test_plan):
        action_id = test_plan.actions[0].id
        resp = client.patch(
            f"/plans/{test_plan.id}/actions/{action_id}",
            json={"status": "concluida"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "concluida"

    def test_revert_action_to_pendente(self, client, test_plan, test_session):
        action = test_plan.actions[0]
        action.status = "concluida"
        test_session.commit()

        resp = client.patch(
            f"/plans/{test_plan.id}/actions/{action.id}",
            json={"status": "pendente"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "pendente"


# ---------------------------------------------------------------------------
# 9. DELETE /plans/{id}/actions/{id} — Exclusão de ação via API
# ---------------------------------------------------------------------------

class TestDeleteAction:
    def test_delete_action_returns_progress(self, client, test_plan):
        action_id = test_plan.actions[0].id
        resp = client.delete(f"/plans/{test_plan.id}/actions/{action_id}")
        assert resp.status_code == 200
        assert "progress" in resp.json()

    def test_delete_last_action_returns_409(self, client, test_session, test_user):
        plan = Plan(user_id=test_user.id, name="Single", progress=0)
        test_session.add(plan)
        test_session.flush()
        action = Action(
            plan_id=plan.id, priority="ALTA", category="T",
            title="Only", objective="O", context="C",
            status="pendente", sequence=1,
        )
        test_session.add(action)
        test_session.commit()

        resp = client.delete(f"/plans/{plan.id}/actions/{action.id}")
        assert resp.status_code == 409
        assert "pelo menos uma ação" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 10. Exception handler — Erro 500 genérico
# ---------------------------------------------------------------------------

class TestExceptionHandler:
    def test_unhandled_exception_returns_500(self):
        """Força uma exceção não tratada para validar o handler."""
        test_app_client = TestClient(app, raise_server_exceptions=False)

        def _override_db():
            raise RuntimeError("boom")

        def _override_user():
            return MagicMock(id=uuid.uuid4())

        app.dependency_overrides[get_db] = _override_db
        app.dependency_overrides[get_current_user] = _override_user
        resp = test_app_client.get("/plans")
        app.dependency_overrides.clear()

        assert resp.status_code == 500
        assert resp.json()["detail"] == "Erro interno do servidor"
