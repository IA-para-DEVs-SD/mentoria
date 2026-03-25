# Design Técnico — Mentoria.IA API

## Visão Geral

A Mentoria.IA API é um backend REST construído em FastAPI (Python) que expõe endpoints para autenticação via Google OAuth 2.0, gerenciamento de perfil profissional, geração de planos de desenvolvimento via Google Gemini (através do PydanticAI) e controle de progresso do usuário.

A API é stateless: toda autorização é feita via JWT. O estado persistente fica no PostgreSQL; o Redis é usado para rate limiting e cache de sessão. O processamento de IA é síncrono do ponto de vista do cliente (request/response com timeout de 30s), sem filas de background para o MVP.

### Objetivos de Design

- Separação clara por domínio: `auth`, `profile`, `plans`, `gemini`
- Validação de entrada centralizada via Pydantic (schemas reutilizados como contratos da LLM)
- Agentes PydanticAI encapsulam toda comunicação com Gemini — nenhum módulo chama o SDK diretamente
- Erros de terceiros (Gemini, Google OAuth) nunca vazam detalhes internos para o cliente

---

## Arquitetura

### Visão de Alto Nível

```
Cliente (Vue.js)
      │  HTTP/REST
      ▼
   Nginx (TLS termination, reverse proxy)
      │
      ▼
   FastAPI (porta 8000)
   ┌─────────────────────────────────────────┐
   │  Routers: /auth  /profile  /plans       │
   │                                         │
   │  Middleware: JWT Auth, Rate Limit        │
   │                                         │
   │  Services: AuthService  ProfileService  │
   │            PlanService  GeminiClient    │
   │                                         │
   │  Agents (PydanticAI):                   │
   │    ProfileAnalyzerAgent                 │
   │    RoadmapGeneratorAgent                │
   └──────────┬──────────────────────────────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
 PostgreSQL           Redis
 (dados)         (rate limiting)
              │
              ▼
       Google Gemini API
```

### Fluxo de Autenticação

```
1. GET /auth/google/login  →  redireciona para Google OAuth consent
2. GET /auth/google/callback?code=...  →  troca code por tokens Google
3. Obtém dados do usuário (nome, email, foto) via Google API
4. Cria/atualiza registro de Usuario no PostgreSQL
5. Emite JWT (access token, 24h)
6. Retorna JWT + has_profile flag
```

### Fluxo de Geração de Plano

```
1. POST /plans  (autenticado)
2. PlanService verifica Perfil completo
3. PlanService carrega Rejeicoes do Usuario
4. GeminiClient monta prompt estruturado
5. RoadmapGeneratorAgent chama Gemini API (timeout 30s)
6. Resposta validada via Pydantic schema
7. Plano + Gaps + Acoes persistidos no PostgreSQL
8. HTTP 201 com Plano completo
```

---

## Componentes e Interfaces

### Estrutura de Módulos

```
app/
├── main.py                  # FastAPI app, middleware, routers
├── config.py                # Settings via pydantic-settings
├── database.py              # SQLAlchemy engine + session
├── dependencies.py          # get_current_user, get_db, rate_limiter
│
├── auth/
│   ├── router.py            # GET /auth/google/login, /callback
│   ├── service.py           # AuthService
│   └── schemas.py           # TokenResponse, UserOut
│
├── profile/
│   ├── router.py            # GET/POST/PUT /profile
│   ├── service.py           # ProfileService
│   ├── schemas.py           # ProfileIn, ProfileOut, ExperienceIn, EducationIn
│   └── models.py            # ORM: Profile, Experience, Education
│
├── plans/
│   ├── router.py            # CRUD /plans, /plans/{id}/actions
│   ├── service.py           # PlanService
│   ├── schemas.py           # PlanOut, ActionOut, ProgressOut
│   └── models.py            # ORM: Plan, Action, Gap, Rejection
│
└── gemini/
    ├── client.py            # GeminiClient (orquestra agentes)
    ├── agents.py            # ProfileAnalyzerAgent, RoadmapGeneratorAgent
    ├── prompts.py           # Templates de prompt
    └── schemas.py           # GeminiPlanResponse, GeminiActionItem
```

### Interfaces Principais

#### AuthService

```python
class AuthService:
    def get_authorization_url() -> str
    def exchange_code(code: str) -> UserTokenData
    def get_or_create_user(user_data: UserTokenData) -> User
    def create_jwt(user_id: UUID) -> str
    def verify_jwt(token: str) -> UUID
```

#### ProfileService

```python
class ProfileService:
    def get_profile(user_id: UUID) -> ProfileOut | None
    def upsert_profile(user_id: UUID, data: ProfileIn) -> ProfileOut
    def is_profile_complete(user_id: UUID) -> bool
```

#### PlanService

```python
class PlanService:
    def list_plans(user_id: UUID) -> list[PlanSummary]
    def get_plan(user_id: UUID, plan_id: UUID) -> PlanOut
    def generate_plan(user_id: UUID) -> PlanOut
    def delete_plan(user_id: UUID, plan_id: UUID) -> None
    def update_action_status(user_id: UUID, plan_id: UUID, action_id: UUID, status: ActionStatus) -> ActionOut
    def delete_action(user_id: UUID, plan_id: UUID, action_id: UUID) -> ProgressOut
    def generate_more_actions(user_id: UUID, plan_id: UUID) -> list[ActionOut]
```

#### GeminiClient

```python
class GeminiClient:
    def generate_plan(profile: ProfileData, rejections: list[Rejection]) -> GeminiPlanResponse
    def generate_actions(profile: ProfileData, existing_actions: list[Action], rejections: list[Rejection]) -> list[GeminiActionItem]
```

### Endpoints REST

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/auth/google/login` | Não | Inicia fluxo OAuth |
| GET | `/auth/google/callback` | Não | Callback OAuth, emite JWT |
| GET | `/profile` | Sim | Retorna perfil completo |
| POST | `/profile` | Sim | Cria/atualiza perfil |
| GET | `/plans` | Sim | Lista planos do usuário |
| POST | `/plans` | Sim | Gera novo plano via Gemini |
| GET | `/plans/{plan_id}` | Sim | Detalhes do plano |
| DELETE | `/plans/{plan_id}` | Sim | Exclui plano |
| PATCH | `/plans/{plan_id}/actions/{action_id}` | Sim | Atualiza status da ação |
| DELETE | `/plans/{plan_id}/actions/{action_id}` | Sim | Exclui ação + registra rejeição |
| POST | `/plans/{plan_id}/actions/generate` | Sim | Gera mais ações |

### Middleware

**JWT Auth Middleware**: Extrai e valida Bearer token em todas as rotas protegidas. Injeta `current_user` via `Depends`.

**Rate Limit Middleware**: Usa Redis com sliding window. Chave: `rate:{user_id}`. Limite: 60 req/min para rotas Gemini. Retorna HTTP 429 com header `Retry-After`.

---

## Modelos de Dados

### Diagrama Entidade-Relacionamento

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    users     │       │    profiles      │       │  experiences │
│──────────────│       │──────────────────│       │──────────────│
│ id (PK)      │──1:1──│ id (PK)          │──1:N──│ id (PK)      │
│ google_id    │       │ user_id (FK)     │       │ profile_id   │
│ name         │       │ career_goal      │       │ role         │
│ email        │       │ skills (JSON)    │       │ seniority    │
│ photo_url    │       │ created_at       │       │ company      │
│ created_at   │       │ updated_at       │       │ start_date   │
└──────────────┘       └──────────────────┘       │ end_date     │
        │                                          └──────────────┘
        │              ┌──────────────────┐
        │              │    educations    │
        │              │──────────────────│
        │              │ id (PK)          │
        │              │ profile_id (FK)  │
        │              │ institution      │
        │              │ level            │
        │              │ title            │
        │              │ study_area       │
        │              │ start_date       │
        │              │ end_date         │
        │              └──────────────────┘
        │
        │──1:N──┐
                ▼
        ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
        │    plans     │──1:N──│    actions   │       │     gaps     │
        │──────────────│       │──────────────│       │──────────────│
        │ id (PK)      │       │ id (PK)      │       │ id (PK)      │
        │ user_id (FK) │       │ plan_id (FK) │       │ plan_id (FK) │
        │ name         │       │ priority     │       │ description  │
        │ progress     │       │ category     │       │ relevance    │
        │ created_at   │       │ title        │       └──────────────┘
        └──────────────┘       │ objective    │
                               │ context      │
                               │ status       │
                               │ sequence     │
                               └──────────────┘

        ┌──────────────────┐
        │    rejections    │
        │──────────────────│
        │ id (PK)          │
        │ user_id (FK)     │
        │ category         │
        │ action_title     │
        │ rejected_at      │
        └──────────────────┘
```

### Schemas Pydantic Principais

```python
# Enums
class Seniority(str, Enum):
    ESTAGIO = "Estagio"
    JUNIOR = "Junior"
    PLENO = "Pleno"
    SENIOR = "Senior"
    ESPECIALISTA = "Especialista"
    LIDERANCA = "Lideranca"

class EducationLevel(str, Enum):
    ENSINO_MEDIO = "Ensino_Medio"
    TECNICO = "Tecnico"
    # ... demais valores

class CareerGoal(str, Enum):
    CRESCER_CARREIRA = "Crescer_na_carreira_atual"
    LIDERANCA = "Assumir_cargos_de_lideranca"
    MUDAR_AREA = "Mudar_de_area"

class ActionStatus(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"

class Priority(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"

# Profile
class ExperienceIn(BaseModel):
    role: str = Field(min_length=1, max_length=500)
    seniority: Seniority
    company: str | None = Field(None, max_length=500)
    start_date: date
    end_date: date | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> "ExperienceIn":
        if self.end_date:
            assert self.end_date >= self.start_date
            assert self.end_date <= date.today()
        assert self.start_date <= date.today()
        return self

class ProfileIn(BaseModel):
    experiences: list[ExperienceIn] = Field(min_length=1)
    educations: list[EducationIn] = Field(min_length=1)
    skills: list[str] = Field(min_length=1)
    career_goal: CareerGoal

# Plan
class ActionOut(BaseModel):
    id: UUID
    priority: Priority
    category: str
    title: str
    objective: str
    context: str
    status: ActionStatus

class PlanOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    progress: int  # 0-100
    gaps: list[GapOut]
    actions: list[ActionOut]

# Auth
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    has_profile: bool
```

### Estrutura do Prompt Gemini

O `GeminiClient` monta um prompt estruturado com seções bem delimitadas:

```
PERFIL DO USUÁRIO:
- Objetivo: {career_goal}
- Experiências: [{role, seniority, company, period}, ...]
- Formação: [{institution, level, title, area}, ...]
- Habilidades: [skill1, skill2, ...]

REJEIÇÕES ANTERIORES (evitar conteúdo similar):
- [{category, title}, ...]

INSTRUÇÕES:
Retorne um JSON com o seguinte schema:
{
  "plan_name": "string",
  "gaps": [{"description": "string", "relevance": int}],
  "actions": [{
    "priority": "ALTA|MEDIA|BAIXA",
    "category": "string",
    "title": "string",
    "objective": "string",
    "context": "string",
    "sequence": int
  }]
}
```

A resposta é validada via `GeminiPlanResponse` (Pydantic), garantindo tipagem forte antes de persistir.

---

## Propriedades de Correção

*Uma propriedade é uma característica ou comportamento que deve ser verdadeiro em todas as execuções válidas de um sistema — essencialmente, uma declaração formal sobre o que o sistema deve fazer. Propriedades servem como ponte entre especificações legíveis por humanos e garantias de correção verificáveis por máquina.*

### Propriedade 1: Autenticação emite JWT válido

*Para qualquer* authorization code válido retornado pelo Google, o sistema deve emitir um JWT que pode ser verificado com a chave secreta da aplicação e que contém o `user_id` correto.

**Valida: Requisitos 1.2, 1.3**

### Propriedade 2: JWT inválido ou ausente é rejeitado

*Para qualquer* requisição a uma rota protegida com token ausente, malformado ou expirado, o sistema deve retornar HTTP 401.

**Valida: Requisitos 1.7, 1.8, 1.9**

### Propriedade 3: Validação de datas de experiência profissional

*Para qualquer* registro de experiência profissional, se `end_date` for fornecida, ela deve ser maior ou igual a `start_date` e não pode ser futura; `start_date` também não pode ser futura. Qualquer violação deve retornar HTTP 422.

**Valida: Requisitos 2.2, 2.3**

### Propriedade 4: Validação de datas de formação acadêmica

*Para qualquer* registro de formação acadêmica, se `end_date` for fornecida, ela deve ser maior ou igual a `start_date`. Qualquer violação deve retornar HTTP 422.

**Valida: Requisitos 2.4, 2.5**

### Propriedade 5: Perfil incompleto bloqueia geração de plano

*Para qualquer* usuário sem perfil completo, uma requisição de geração de plano deve retornar HTTP 400 e nenhum dado deve ser persistido.

**Valida: Requisito 3.1, 3.2**

### Propriedade 6: Rejeições influenciam geração de plano

*Para qualquer* usuário com rejeições registradas, o prompt enviado ao Gemini deve conter todas as rejeições daquele usuário.

**Valida: Requisitos 3.3, 3.9**

### Propriedade 7: Progresso é calculado corretamente

*Para qualquer* plano com N ações, onde K estão com status `concluida`, o campo `progress` deve ser igual a `floor((K / N) * 100)`.

**Valida: Requisitos 4.3, 7.2, 7.3**

### Propriedade 8: Atualização de status recalcula progresso

*Para qualquer* ação de um plano, alternar seu status entre `pendente` e `concluida` deve resultar em um progresso recalculado consistente com a fórmula da Propriedade 7.

**Valida: Requisitos 7.1, 7.2, 7.3, 7.4**

### Propriedade 9: Exclusão de ação registra rejeição

*Para qualquer* ação excluída, deve existir um registro de `Rejection` com `user_id`, `category` e `action_title` correspondentes à ação excluída.

**Valida: Requisito 8.2**

### Propriedade 10: Plano com única ação não pode ter ação excluída

*Para qualquer* plano com exatamente 1 ação, uma requisição de exclusão dessa ação deve retornar HTTP 409 e o plano deve permanecer inalterado.

**Valida: Requisito 8.5**

### Propriedade 11: Planos pertencem ao usuário autenticado

*Para qualquer* operação em `/plans/{plan_id}`, se o `plan_id` não pertencer ao usuário autenticado, o sistema deve retornar HTTP 404 (sem revelar existência do recurso).

**Valida: Requisitos 4.4, 6.4, 7.5, 8.6, 9.7**

### Propriedade 12: Rate limiting bloqueia excesso de requisições

*Para qualquer* usuário autenticado que exceder 60 requisições por minuto nas rotas Gemini, a requisição que ultrapassar o limite deve retornar HTTP 429.

**Valida: Requisito 10.4, 10.5**

### Propriedade 13: Timeout do Gemini não persiste dados parciais

*Para qualquer* chamada ao Gemini que exceder 30 segundos, o sistema deve retornar HTTP 502 e nenhum dado parcial deve ser persistido no banco.

**Valida: Requisitos 3.8, 9.6, 11.2, 11.3**

### Propriedade 14: Campos de texto são sanitizados

*Para qualquer* campo de texto livre, caracteres de controle devem ser removidos e o tamanho deve ser limitado a 500 caracteres. Entradas que violem isso devem retornar HTTP 422.

**Valida: Requisito 10.2**

---

## Tratamento de Erros

### Mapeamento de Erros

| Situação | HTTP Status | Corpo |
|----------|-------------|-------|
| Token ausente/inválido | 401 | `{"detail": "Token inválido ou ausente"}` |
| Token expirado | 401 | `{"detail": "Token expirado"}` |
| OAuth code inválido | 401 | `{"detail": "Código de autorização inválido"}` |
| Recurso não encontrado / não pertence ao usuário | 404 | `{"detail": "Recurso não encontrado"}` |
| Validação de schema | 422 | Padrão FastAPI com lista de erros por campo |
| Plano com única ação | 409 | `{"detail": "O plano deve ter pelo menos uma ação"}` |
| Rate limit excedido | 429 | `{"detail": "Limite de requisições excedido"}` + `Retry-After` header |
| Timeout Gemini | 502 | `{"detail": "Serviço de IA indisponível. Tente novamente."}` |
| Erro interno | 500 | `{"detail": "Erro interno do servidor"}` |

### Princípios

- Erros de terceiros (Gemini, Google) são capturados e mapeados para respostas padronizadas — detalhes internos nunca chegam ao cliente
- Transações de banco de dados são revertidas em caso de erro durante persistência de plano/ações
- Logs estruturados registram o erro completo internamente (timestamp, rota, user_id, traceback)

---

## Estratégia de Testes

### Abordagem Dual

A estratégia combina testes unitários/de integração com testes baseados em propriedades (property-based testing).

**Testes unitários** cobrem:
- Casos específicos e exemplos concretos (ex: OAuth callback com code válido)
- Condições de erro e edge cases (ex: plano com 1 ação, token expirado)
- Integração entre camadas (router → service → ORM)

**Testes de propriedade** cobrem:
- Invariantes que devem valer para qualquer entrada válida
- Geração aleatória de perfis, planos e ações para verificar correção geral

### Biblioteca de Property-Based Testing

Usar **Hypothesis** (Python), com mínimo de 100 iterações por propriedade.

```python
from hypothesis import given, settings
from hypothesis import strategies as st

@given(st.integers(min_value=0), st.integers(min_value=1))
@settings(max_examples=100)
def test_progress_calculation(completed: int, total: int):
    # Feature: mentoria-ia-api, Property 7: Progresso é calculado corretamente
    assume(completed <= total)
    result = calculate_progress(completed, total)
    assert result == math.floor((completed / total) * 100)
    assert 0 <= result <= 100
```

### Mapeamento Propriedade → Teste

| Propriedade | Tipo | Descrição do Teste |
|-------------|------|--------------------|
| P1: JWT válido | property | Gerar UUIDs aleatórios, criar JWT, verificar decode |
| P2: JWT inválido rejeitado | property | Gerar tokens malformados/expirados, verificar 401 |
| P3: Datas de experiência | property | Gerar pares de datas aleatórios, verificar validação |
| P4: Datas de formação | property | Gerar pares de datas aleatórios, verificar validação |
| P5: Perfil incompleto bloqueia | example | Criar usuário sem perfil, tentar gerar plano |
| P6: Rejeições no prompt | property | Gerar lista de rejeições, verificar presença no prompt |
| P7: Cálculo de progresso | property | Gerar K/N aleatórios, verificar fórmula |
| P8: Recálculo ao atualizar status | property | Alternar status de ações, verificar consistência |
| P9: Exclusão registra rejeição | property | Excluir ações aleatórias, verificar tabela rejections |
| P10: Última ação protegida | example | Plano com 1 ação, tentar excluir, verificar 409 |
| P11: Isolamento por usuário | property | Gerar múltiplos usuários/planos, verificar 404 cruzado |
| P12: Rate limiting | property | Simular N+1 requisições, verificar 429 na última |
| P13: Timeout não persiste | example | Mock Gemini com timeout, verificar rollback |
| P14: Sanitização de texto | property | Gerar strings com caracteres de controle, verificar rejeição |

### Tag Format

Cada teste de propriedade deve incluir comentário:
```
# Feature: mentoria-ia-api, Property {N}: {texto da propriedade}
```

### Configuração de Testes

- **pytest** como runner principal
- **pytest-asyncio** para testes de endpoints async
- **httpx.AsyncClient** para testes de integração dos routers
- **SQLite em memória** para testes (SQLAlchemy suporta ambos)
- **fakeredis** para mockar Redis nos testes de rate limiting
- **unittest.mock** para mockar chamadas ao Gemini
