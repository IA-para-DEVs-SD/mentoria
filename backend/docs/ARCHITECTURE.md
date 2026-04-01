# Arquitetura — MentorIA (Backend)

## Visão Geral

API REST responsável pela lógica de negócio da plataforma MentorIA. Gerencia autenticação via Google OAuth, perfis de usuário, e a geração de planos de desenvolvimento de carreira utilizando agentes de IA (Google Gemini). Persistência em SQLite.

> Arquitetura do frontend: [`frontend/docs/ARCHITECTURE.md`](../../frontend/docs/ARCHITECTURE.md)

---

## Stack

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.12 | Linguagem |
| FastAPI | 0.135+ | Framework web async |
| SQLAlchemy | 2.x | ORM |
| Alembic | 1.x | Migrations |
| SQLite | — | Banco de dados (embutido) |
| PydanticAI | 0.x | Agentes de IA com output estruturado |
| Google Gemini | 2.5 Flash | Modelo LLM |
| Pydantic | 2.x | Validação de dados |
| pydantic-settings | 2.x | Configuração via .env |
| python-jose | 3.x | JWT (criação/verificação) |
| authlib | 1.x | OAuth 2.0 client |
| httpx | 0.x | HTTP client async |
| uvicorn | 0.x | ASGI server |

---

## Estrutura de Pastas/Arquivos

```
backend/
├── src/
│   ├── main.py              # App FastAPI, middlewares (CORS, logging), registro de routers
│   ├── config.py            # Settings via pydantic-settings (.env)
│   ├── database.py          # Engine SQLAlchemy + SessionLocal
│   ├── dependencies.py      # get_db, get_current_user
│   ├── auth/
│   │   ├── models.py        # User (UUID, google_id, name, email, photo_url)
│   │   ├── schemas.py       # TokenResponse, UserOut
│   │   ├── service.py       # AuthService (OAuth flow, JWT create/verify)
│   │   └── router.py        # Rotas de autenticação
│   ├── profile/
│   │   ├── models.py        # Profile, Experience, Education
│   │   ├── schemas.py       # ProfileIn/Out, ExperienceIn/Out, EducationIn/Out, enums
│   │   ├── service.py       # ProfileService (get, upsert, is_complete)
│   │   └── router.py        # Rotas de perfil
│   ├── plans/
│   │   ├── models.py        # Plan, Action, Gap, Rejection
│   │   ├── schemas.py       # PlanOut, PlanSummary, ActionOut, GapOut, ProgressOut, enums
│   │   ├── service.py       # PlanService (generate, list, get, delete, actions CRUD)
│   │   └── router.py        # Rotas de planos e ações
│   └── gemini/
│       ├── agents.py        # roadmap_agent, actions_agent (PydanticAI + GoogleProvider)
│       ├── client.py        # GeminiClient (orquestra chamadas aos agentes com timeout)
│       ├── prompts.py       # Templates de prompt (perfil + rejeições)
│       └── schemas.py       # GeminiPlanResponse, GeminiActionItem, GeminiGapItem
├── tests/
│   ├── conftest.py          # Fixtures compartilhadas (db, user, profile, plan, JWT, mocks)
│   └── test_*.py            # Testes por módulo (auth, profile, plans, gemini, dependencies)
├── alembic/                 # Migrations do banco de dados
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## Endpoints

### Auth (`/auth`)

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/auth/google/login` | Não | Redireciona para OAuth do Google |
| GET | `/auth/google/callback` | Não | Callback OAuth → cria/busca user → redireciona frontend com JWT |

### Profile (`/profile`)

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/profile` | JWT | Retorna perfil do usuário logado |
| POST | `/profile` | JWT | Cria ou atualiza perfil (upsert) |

### Plans (`/plans`)

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/plans` | JWT | Lista planos do usuário |
| POST | `/plans` | JWT | Gera novo plano via Gemini (201) |
| GET | `/plans/{id}` | JWT | Detalhe de um plano |
| DELETE | `/plans/{id}` | JWT | Remove plano (204) |
| PATCH | `/plans/{id}/actions/{action_id}` | JWT | Atualiza status de uma ação |
| DELETE | `/plans/{id}/actions/{action_id}` | JWT | Remove ação (registra rejeição, retorna progresso) |
| POST | `/plans/{id}/actions/generate` | JWT | Gera mais ações via Gemini |

---

## Diagrama UML de Classes

```mermaid
classDiagram
    class User {
        +UUID id
        +String google_id
        +String name
        +String email
        +String photo_url
        +DateTime created_at
    }

    class Profile {
        +UUID id
        +UUID user_id
        +String career_goal
        +JSON skills
        +DateTime created_at
        +DateTime updated_at
    }

    class Experience {
        +UUID id
        +UUID profile_id
        +String role
        +String seniority
        +String company
        +Date start_date
        +Date end_date
    }

    class Education {
        +UUID id
        +UUID profile_id
        +String institution
        +String level
        +String title
        +String study_area
        +Date start_date
        +Date end_date
    }

    class Plan {
        +UUID id
        +UUID user_id
        +String name
        +Integer progress
        +DateTime created_at
    }

    class Action {
        +UUID id
        +UUID plan_id
        +String priority
        +String category
        +String title
        +String objective
        +String context
        +String status
        +Integer sequence
    }

    class Gap {
        +UUID id
        +UUID plan_id
        +String description
        +Integer relevance
    }

    class Rejection {
        +UUID id
        +UUID user_id
        +String category
        +String action_title
        +DateTime rejected_at
    }

    class AuthService {
        +get_authorization_url() String
        +handle_callback(code) TokenResponse
        +verify_token(token) UUID
    }

    class ProfileService {
        +get_profile(db, user_id) Profile
        +upsert_profile(db, user_id, data) Profile
        +is_complete(profile) bool
    }

    class PlanService {
        +generate_plan(db, user_id) Plan
        +list_plans(db, user_id) List~Plan~
        +get_plan(db, plan_id, user_id) Plan
        +delete_plan(db, plan_id, user_id) void
        +update_action_status(db, action_id, status) Action
        +delete_action(db, action_id) ProgressOut
        +generate_more_actions(db, plan_id) List~Action~
    }

    class GeminiClient {
        +generate_plan(profile_text, rejections) GeminiPlanResponse
        +generate_actions(profile_text, plan_context, rejections) List~GeminiActionItem~
    }

    User "1" -- "0..1" Profile : possui
    Profile "1" -- "1..*" Experience : contém
    Profile "1" -- "1..*" Education : contém
    User "1" -- "0..*" Plan : gera
    User "1" -- "0..*" Rejection : registra
    Plan "1" -- "1..*" Action : possui
    Plan "1" -- "1..*" Gap : identifica
    PlanService --> GeminiClient : usa
    PlanService --> Plan : gerencia
    ProfileService --> Profile : gerencia
    AuthService --> User : autentica
```

---

## Diagrama de Sequência — Geração de Plano

```mermaid
sequenceDiagram
    actor U as Usuário
    participant F as Frontend
    participant API as FastAPI
    participant PS as PlanService
    participant GC as GeminiClient
    participant AI as Google Gemini

    U->>F: Confirma onboarding
    F->>API: POST /plans (JWT)
    API->>API: Valida JWT + get_current_user
    API->>PS: generate_plan(db, user_id)
    PS->>PS: Carrega perfil + rejeições
    PS->>GC: generate_plan(profile_text, rejections)

    loop Retry (até 3 tentativas)
        GC->>AI: Envia prompt estruturado
        AI-->>GC: Resposta JSON (gaps + ações)
    end

    GC-->>PS: GeminiPlanResponse
    PS->>PS: Salva Plan, Actions, Gaps no DB
    PS-->>API: Plan (com ações e gaps)
    API-->>F: 201 Created + PlanOut
    F->>F: Redireciona para /plan/:id
    F-->>U: Exibe detalhes do plano
```

---

## Diagrama de Conexões

```mermaid
graph LR
    Frontend["Frontend (Vue.js)"] -->|HTTP REST + JWT| FastAPI

    subgraph Backend
        FastAPI["FastAPI"] --> AuthModule["Auth (OAuth + JWT)"]
        FastAPI --> ProfileModule["Profile Service"]
        FastAPI --> PlansModule["Plans Service"]
        PlansModule --> GeminiClient["Gemini Client"]
        GeminiClient --> Agents["PydanticAI Agents"]
    end

    AuthModule -->|OAuth 2.0| Google["Google OAuth"]
    Agents -->|API| Gemini["Google Gemini 2.5 Flash"]
    ProfileModule --> SQLite["SQLite"]
    PlansModule --> SQLite
    AuthModule --> SQLite
```
