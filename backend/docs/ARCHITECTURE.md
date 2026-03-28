# Arquitetura — MentorIA

## Visão Geral

O MentorIA é uma plataforma de mentoria de carreira com IA. Segue uma arquitetura de 2 camadas (frontend + backend) com integração à API do Google Gemini para geração de planos de desenvolvimento. Comunicação via REST, containerizada com Docker Compose para desenvolvimento local.

## Stack Tecnológica

### Backend
- **Framework:** FastAPI (async, Python 3.12)
- **ORM:** SQLAlchemy + Alembic (migrations)
- **Banco:** SQLite (`mentoria.db`)
- **Autenticação:** Google OAuth 2.0 + JWT (python-jose)
- **IA:** PydanticAI com Google Gemini (`gemini-2.5-flash`)
- **Validação:** Pydantic v2 + pydantic-settings
- **HTTP Client:** authlib + httpx (OAuth flow)

### Frontend
- **Framework:** Vue 3 (Composition API + `<script setup>`)
- **UI:** PrimeVue 4 + Tailwind CSS 4
- **Ícones:** Lucide Vue Next + PrimeIcons
- **State:** Pinia
- **HTTP:** Axios
- **Router:** Vue Router 5
- **Build:** Vite 7

---

## Estrutura do Backend

```
backend/src/
├── main.py              # App FastAPI, middlewares, routers
├── config.py            # Settings via pydantic-settings (.env)
├── database.py          # Engine SQLAlchemy + SessionLocal
├── dependencies.py      # get_db, get_current_user, rate_limiter
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
│   ├── schemas.py       # PlanOut, PlanSummary, ActionOut, GapOut, enums
│   ├── service.py       # PlanService (generate, list, get, delete, actions CRUD)
│   └── router.py        # CRUD /plans, /plans/{id}/actions/*
└── gemini/
    ├── agents.py        # roadmap_agent, actions_agent (PydanticAI)
    ├── client.py        # GeminiClient (orquestra chamadas aos agentes)
    ├── prompts.py       # Templates de prompt (perfil + rejeições)
    └── schemas.py       # GeminiPlanResponse, GeminiActionItem, GeminiGapItem
```

## Estrutura do Frontend

```
frontend/src/
├── App.vue              # Root (Toast, ConfirmDialog, RouterView)
├── main.ts              # Bootstrap (Pinia, PrimeVue, Router)
├── router/index.ts      # Rotas + guard de autenticação
├── services/
│   ├── api.ts           # Axios instance (baseURL, interceptors JWT/401)
│   ├── authService.ts   # loginWithGoogle(), logout()
│   ├── planService.ts   # CRUD planos e ações via API
│   └── profileService.ts # get/save perfil via API
├── stores/
│   ├── authStore.ts     # Token, login redirect, callback, logout
│   ├── plansStore.ts    # Lista planos, plano atual, CRUD ações
│   └── profileStore.ts  # Perfil do usuário
├── types/
│   ├── index.ts         # Re-exports
│   ├── user.ts          # User, TokenResponse
│   ├── profile.ts       # Seniority, EducationLevel, CareerGoal, ProfileData/Out
│   └── plan.ts          # ActionStatus, Priority, Plan, Action, Gap
├── pages/
│   ├── LoginPage.vue
│   ├── AuthCallbackPage.vue
│   ├── OnboardingPage.vue
│   ├── LoadingAIPage.vue
│   ├── HomePage.vue
│   └── PlanDetailPage.vue
├── components/
│   ├── auth/            # GoogleLoginButton
│   ├── onboarding/      # StepFormacao, StepHabilidades, StepObjetivo, StepRevisao, StepTrajetoria
│   ├── home/            # EmptyState, PlanCard, PlanList
│   └── plan/            # ActionItem, ActionTimeline, GapsList, PlanHeader, ProgressCard
├── composables/
│   └── useOnboarding.ts # Lógica do wizard de onboarding
└── layouts/
```

---

## Modelo de Dados

```
users
├── id (UUID, PK)
├── google_id (unique)
├── name, email, photo_url
└── created_at

profiles (1:1 com users)
├── id (UUID, PK)
├── user_id (FK → users, unique)
├── career_goal (enum: Crescer_na_carreira_atual | Assumir_cargos_de_lideranca | Mudar_de_area)
├── skills (JSON array)
├── created_at, updated_at
├── experiences[] → Experience (role, seniority, company, start_date, end_date)
└── educations[] → Education (institution, level, title, study_area, start_date, end_date)

plans (1:N com users)
├── id (UUID, PK)
├── user_id (FK → users)
├── name, progress (0-100)
├── created_at
├── actions[] → Action (priority, category, title, objective, context, status, sequence)
└── gaps[] → Gap (description, relevance)

rejections (histórico de ações rejeitadas pelo usuário)
├── id (UUID, PK)
├── user_id (FK → users)
├── category, action_title
└── rejected_at
```

---

## Endpoints da API

### Auth (`/auth`)
| Método | Rota                    | Descrição                                      |
|--------|-------------------------|-------------------------------------------------|
| GET    | `/auth/google/login`    | Redireciona para OAuth do Google                |
| GET    | `/auth/google/callback` | Callback OAuth → cria/busca user → redireciona frontend com JWT |

### Profile (`/profile`)
| Método | Rota       | Auth | Descrição                          |
|--------|------------|------|------------------------------------|
| GET    | `/profile` | JWT  | Retorna perfil do usuário logado   |
| POST   | `/profile` | JWT  | Cria ou atualiza perfil (upsert)   |

### Plans (`/plans`)
| Método | Rota                                  | Auth | Descrição                              |
|--------|---------------------------------------|------|----------------------------------------|
| GET    | `/plans`                              | JWT  | Lista planos do usuário                |
| POST   | `/plans`                              | JWT  | Gera novo plano via Gemini             |
| GET    | `/plans/{id}`                         | JWT  | Detalhe de um plano                    |
| DELETE | `/plans/{id}`                         | JWT  | Remove plano                           |
| PATCH  | `/plans/{id}/actions/{action_id}`     | JWT  | Atualiza status de uma ação            |
| DELETE | `/plans/{id}/actions/{action_id}`     | JWT  | Remove ação (registra rejeição)        |
| POST   | `/plans/{id}/actions/generate`        | JWT  | Gera mais ações via Gemini             |

---

## Agentes PydanticAI

O sistema usa 2 agentes PydanticAI com o modelo `gemini-2.5-flash`:

### 1. roadmap_agent
- **Input:** Prompt com perfil do usuário + rejeições anteriores
- **Output:** `GeminiPlanResponse` (plan_name, gaps[], actions[])
- **Uso:** Geração de plano completo de desenvolvimento

### 2. actions_agent
- **Input:** Prompt com perfil + ações existentes + rejeições
- **Output:** `ActionsResponse` (actions[])
- **Uso:** Geração de ações adicionais para um plano existente

Ambos usam `ThreadPoolExecutor` com timeout de 30s para evitar bloqueio.

---

## Fluxo Principal

```
1. Usuário acessa LoginPage → clica "Entrar com Google"
2. Redirect para Google OAuth → callback no backend
3. Backend cria/busca User, gera JWT, redireciona para /auth/callback?token=...&has_profile=...
4. Frontend salva token no localStorage
5. Se !has_profile → OnboardingPage (wizard 5 steps: Trajetória, Formação, Habilidades, Objetivo, Revisão)
6. POST /profile → salva perfil
7. LoadingAIPage → POST /plans → Gemini gera plano
8. Redirect para PlanDetailPage com o plano gerado
9. HomePage lista todos os planos do usuário
10. PlanDetailPage: visualizar gaps, ações, marcar concluídas, remover, gerar mais
```

---

## Infraestrutura Local (Docker Compose)

```
Navegador (localhost)
    │
    ├── :5173 ──► Frontend (Nginx servindo SPA Vue.js)
    │                 │
    │                 │ proxy /api/* ──► backend:8000
    │                 ▼
    └── :8000 ──► Backend (FastAPI + Uvicorn)
                      │
                      ├── SQLite (mentoria.db)
                      │
                      └── Google Gemini API (externo)
```

### Containers

| Container            | Porta         | Descrição                                      |
|----------------------|---------------|-------------------------------------------------|
| mentoria-frontend    | 5173 → 80     | Nginx servindo build Vue.js + proxy reverso /api |
| mentoria-backend     | 8000          | FastAPI (REST API + OAuth)                       |

### Rede
- `mentoria-net` (bridge) — comunicação entre containers
- Nginx do frontend faz proxy de `/api/*` para `http://backend:8000/`

### Variáveis de Ambiente (`backend/.env`)

| Variável               | Descrição                                    |
|------------------------|----------------------------------------------|
| DATABASE_URL           | Connection string SQLite                     |
| GOOGLE_CLIENT_ID       | OAuth 2.0 Client ID (Google Cloud Console)   |
| GOOGLE_CLIENT_SECRET   | OAuth 2.0 Client Secret                      |
| GOOGLE_REDIRECT_URI    | Callback URL do OAuth                        |
| JWT_SECRET             | Chave para assinatura dos tokens JWT         |
| GEMINI_API_KEY         | API Key do Google Gemini                     |

---

## Como Subir

### Docker Compose (recomendado)
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend Swagger: http://localhost:8000/docs

### Sem Docker
```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # preencher chaves
alembic upgrade head
uvicorn src.main:app --reload

# Frontend (outro terminal)
cd frontend
npm install
npm run dev
```

---

## Segurança
- Autenticação via Google OAuth 2.0 + JWT (24h expiry)
- CORS allow all origins (desenvolvimento)
- Secrets via `.env` (fora do git)
- Input sanitization (strip control chars) em todos os campos de texto
- Validação de datas (não aceita datas futuras em experiências)
- Normalização de prioridades (remove acentos) nos schemas Gemini
- Interceptor 401 no frontend (limpa token e redireciona para login)
