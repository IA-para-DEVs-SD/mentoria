# Arquitetura — MentorIA

## Visão Geral

O MentorIA é uma plataforma de mentoria de carreira com IA. Segue uma arquitetura de 2 camadas (frontend + backend) com integração à API do Google Gemini para geração de planos de desenvolvimento. Comunicação via REST, containerizada com Docker Compose para desenvolvimento local.

## Stack Tecnológica

### Backend
- **Framework:** FastAPI (async, Python 3.12)
- **ORM:** SQLAlchemy + Alembic (migrations)
- **Banco:** SQLite (`mentoria.db`)
- **Cache / Rate Limiting:** Redis (via `redis-py`)
- **Autenticação:** Google OAuth 2.0 + JWT (python-jose)
- **IA:** PydanticAI com Google Gemini (`gemini-2.5-flash`)
- **Validação:** Pydantic v2 + pydantic-settings
- **HTTP Client:** authlib + httpx (OAuth flow)

### Frontend
- **Framework:** Vue 3 (Composition API + `<script setup>`)
- **UI:** PrimeVue 4 (tema Aura) + Tailwind CSS 4
- **Ícones:** Lucide Vue Next + PrimeIcons
- **State:** Pinia
- **HTTP:** Axios
- **Router:** Vue Router 5
- **Build:** Vite 7
- **Linguagem:** TypeScript 5.9

---

## Estrutura do Backend

```
backend/src/
├── main.py              # App FastAPI, middlewares (CORS, logging), routers
├── config.py            # Settings via pydantic-settings (.env)
├── database.py          # Engine SQLAlchemy + SessionLocal
├── dependencies.py      # get_db, get_current_user, rate_limiter (Redis)
├── auth/
│   ├── models.py        # User (UUID, google_id, name, email, photo_url)
│   ├── schemas.py       # TokenResponse, UserOut
│   ├── service.py       # AuthService (OAuth flow, JWT create/verify)
│   └── router.py        # GET /auth/google/login, GET /auth/google/callback
├── profile/
│   ├── models.py        # Profile, Experience, Education
│   ├── schemas.py       # ProfileIn/Out, ExperienceIn/Out, EducationIn/Out, enums
│   ├── service.py       # ProfileService (get, upsert, is_complete)
│   └── router.py        # GET /profile, POST /profile
├── plans/
│   ├── models.py        # Plan, Action, Gap, Rejection
│   ├── schemas.py       # PlanOut, PlanSummary, ActionOut, GapOut, ProgressOut, enums
│   ├── service.py       # PlanService (generate, list, get, delete, actions CRUD)
│   └── router.py        # CRUD /plans, /plans/{id}/actions/*
└── gemini/
    ├── agents.py        # roadmap_agent, actions_agent (PydanticAI + GoogleProvider)
    ├── client.py        # GeminiClient (orquestra chamadas aos agentes)
    ├── prompts.py       # Templates de prompt (perfil + rejeições)
    └── schemas.py       # GeminiPlanResponse, GeminiActionItem, GeminiGapItem
```
