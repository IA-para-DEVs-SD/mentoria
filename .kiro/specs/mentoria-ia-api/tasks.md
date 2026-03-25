# Plano de Implementação: Mentoria.IA API

## Visão Geral

Implementação incremental da API REST em FastAPI, organizada por domínio (`auth`, `profile`, `plans`, `gemini`). Cada tarefa constrói sobre a anterior, garantindo que nenhum código fique órfão. A integração final conecta todos os módulos.

## Tarefas

- [x] 1. Configurar estrutura do projeto e infraestrutura base
  - Criar estrutura de diretórios `app/` com módulos `auth/`, `profile/`, `plans/`, `gemini/`
  - Implementar `app/config.py` com `Settings` via `pydantic-settings` (variáveis: `DATABASE_URL`, `REDIS_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `JWT_SECRET`, `GEMINI_API_KEY`)
  - Implementar `app/database.py` com engine SQLAlchemy, `SessionLocal` e `Base`
  - Implementar `app/main.py` com instância FastAPI, registro de routers e handler de erro 500 genérico
  - Criar `requirements.txt` com dependências: `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `pydantic-settings`, `python-jose`, `authlib`, `google-generativeai`, `pydantic-ai`, `redis`, `httpx`, `pytest`, `hypothesis`, `pytest-asyncio`, `fakeredis`
  - _Requisitos: RNF 1, RNF 2_

- [x] 2. Implementar modelos ORM e migrações
  - [x] 2.1 Criar modelos ORM em `auth` e `profile`
    - Criar `app/auth/models.py`: modelo `User` (id UUID PK, google_id, name, email, photo_url, created_at)
    - Criar `app/profile/models.py`: modelos `Profile`, `Experience`, `Education` conforme diagrama ER do design
    - _Requisitos: 1.3, 2.2, 2.4_

  - [x] 2.2 Criar modelos ORM em `plans`
    - Criar `app/plans/models.py`: modelos `Plan`, `Action`, `Gap`, `Rejection` conforme diagrama ER do design
    - _Requisitos: 3.5, 8.2_

  - [x] 2.3 Configurar Alembic e gerar migração inicial
    - Inicializar Alembic (`alembic init alembic`)
    - Configurar `alembic/env.py` para importar `Base` e usar `DATABASE_URL` do `config.py`
    - Gerar migração inicial com todos os modelos
    - _Requisitos: RNF 1_

- [x] 3. Implementar schemas Pydantic e enums compartilhados
  - [x] 3.1 Criar enums e schemas de autenticação
    - Criar `app/auth/schemas.py`: `TokenResponse` (access_token, token_type, has_profile), `UserOut`
    - _Requisitos: 1.3, 1.4, 1.5_

  - [x] 3.2 Criar schemas de perfil com validações
    - Criar `app/profile/schemas.py`: enums `Seniority`, `EducationLevel`, `CareerGoal`; schemas `ExperienceIn`, `EducationIn`, `ProfileIn`, `ProfileOut` com `@model_validator` para validação de datas
    - _Requisitos: 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 10.2_

  - [ ]* 3.3 Escrever testes de propriedade para validação de datas de experiência
    - **Propriedade 3: Validação de datas de experiência profissional**
    - **Valida: Requisitos 2.2, 2.3**

  - [ ]* 3.4 Escrever testes de propriedade para validação de datas de formação acadêmica
    - **Propriedade 4: Validação de datas de formação acadêmica**
    - **Valida: Requisitos 2.4, 2.5**

  - [ ]* 3.5 Escrever testes de propriedade para sanitização de campos de texto
    - **Propriedade 14: Campos de texto são sanitizados**
    - **Valida: Requisito 10.2**

  - [x] 3.6 Criar schemas de planos
    - Criar `app/plans/schemas.py`: enums `ActionStatus`, `Priority`; schemas `ActionOut`, `GapOut`, `PlanOut`, `PlanSummary`, `ProgressOut`, `ActionStatusUpdate`
    - _Requisitos: 4.2, 4.3, 4.5, 5.2, 7.1, 7.4_

  - [x] 3.7 Criar schemas do Gemini
    - Criar `app/gemini/schemas.py`: `GeminiActionItem`, `GeminiPlanResponse` (validados via Pydantic para garantir tipagem forte antes de persistir)
    - _Requisitos: 3.4, 3.5_

- [x] 4. Implementar módulo de autenticação
  - [x] 4.1 Implementar AuthService
    - Criar `app/auth/service.py` com `AuthService`: `get_authorization_url()`, `exchange_code()`, `get_or_create_user()`, `create_jwt()`, `verify_jwt()`
    - Usar `authlib` para fluxo OAuth 2.0 com Google
    - JWT com expiração de 24h via `python-jose`
    - Armazenar apenas URL da foto (não tokens Google) — Requisito 10.3
    - _Requisitos: 1.1, 1.2, 1.3, 1.6, 10.3_

  - [ ]* 4.2 Escrever testes de propriedade para emissão e verificação de JWT
    - **Propriedade 1: Autenticação emite JWT válido**
    - **Valida: Requisitos 1.2, 1.3**

  - [ ]* 4.3 Escrever testes de propriedade para rejeição de JWT inválido
    - **Propriedade 2: JWT inválido ou ausente é rejeitado**
    - **Valida: Requisitos 1.7, 1.8, 1.9**

  - [x] 4.4 Implementar router de autenticação e dependências
    - Criar `app/auth/router.py`: `GET /auth/google/login` e `GET /auth/google/callback`
    - Criar `app/dependencies.py`: `get_db()`, `get_current_user()` (extrai e valida JWT, retorna HTTP 401 se inválido/ausente/expirado)
    - _Requisitos: 1.1, 1.2, 1.7, 1.8, 1.9_

- [x] 5. Checkpoint — Garantir que todos os testes passam
  - Garantir que todos os testes passam. Perguntar ao usuário se houver dúvidas.

- [x] 6. Implementar módulo de perfil
  - [x] 6.1 Implementar ProfileService
    - Criar `app/profile/service.py` com `ProfileService`: `get_profile()`, `upsert_profile()`, `is_profile_complete()`
    - Validar campos obrigatórios e retornar HTTP 422 com detalhes para entradas inválidas
    - Suportar múltiplos registros de experiência e formação por usuário
    - _Requisitos: 2.1, 2.8, 2.9, 2.10, 2.11_

  - [x] 6.2 Implementar router de perfil
    - Criar `app/profile/router.py`: `GET /profile`, `POST /profile`
    - Proteger rotas com `get_current_user` via `Depends`
    - _Requisitos: 2.1, 2.9, 2.11_

  - [ ]* 6.3 Escrever testes unitários para ProfileService
    - Testar `upsert_profile` com dados válidos e inválidos
    - Testar `is_profile_complete` com perfis parciais e completos
    - _Requisitos: 2.8, 2.9_

- [x] 7. Implementar módulo Gemini (agentes PydanticAI)
  - [x] 7.1 Implementar templates de prompt
    - Criar `app/gemini/prompts.py` com templates para geração de plano e geração de mais ações
    - Incluir seções: perfil do usuário, rejeições anteriores, instruções de formato JSON
    - _Requisitos: 3.3, 3.4, 9.2, 9.3_

  - [x] 7.2 Implementar agentes PydanticAI
    - Criar `app/gemini/agents.py`: `ProfileAnalyzerAgent` e `RoadmapGeneratorAgent` usando PydanticAI com output validado via `GeminiPlanResponse`
    - _Requisitos: 3.4, 9.3_

  - [x] 7.3 Implementar GeminiClient
    - Criar `app/gemini/client.py` com `GeminiClient`: `generate_plan()` e `generate_actions()`
    - Implementar timeout de 30s e retornar erro sem persistir dados parciais em caso de falha
    - _Requisitos: 3.4, 3.8, 9.6, 11.2, 11.3_

  - [ ]* 7.4 Escrever testes de propriedade para rejeições no prompt
    - **Propriedade 6: Rejeições influenciam geração de plano**
    - **Valida: Requisitos 3.3, 3.9**

  - [ ]* 7.5 Escrever testes de exemplo para timeout do Gemini sem persistência
    - **Propriedade 13: Timeout do Gemini não persiste dados parciais**
    - **Valida: Requisitos 3.8, 9.6, 11.2, 11.3**

- [x] 8. Implementar módulo de planos — CRUD e progresso
  - [x] 8.1 Implementar lógica de cálculo de progresso
    - Criar função `calculate_progress(completed: int, total: int) -> int` em `app/plans/service.py`
    - Fórmula: `floor((completed / total) * 100)`, retorna 0 se total == 0
    - _Requisitos: 4.3, 7.2, 7.3_

  - [ ]* 8.2 Escrever testes de propriedade para cálculo de progresso
    - **Propriedade 7: Progresso é calculado corretamente**
    - **Valida: Requisitos 4.3, 7.2, 7.3**

  - [x] 8.3 Implementar PlanService — geração e CRUD de planos
    - Implementar em `app/plans/service.py`: `generate_plan()`, `list_plans()`, `get_plan()`, `delete_plan()`
    - `generate_plan()`: verificar perfil completo (HTTP 400 se incompleto), carregar rejeições, chamar `GeminiClient`, persistir Plano + Gaps + Ações em transação (rollback em erro)
    - `list_plans()`: ordenar por `created_at` decrescente
    - `get_plan()`: retornar HTTP 404 se não pertencer ao usuário autenticado
    - _Requisitos: 3.1, 3.2, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

  - [ ]* 8.4 Escrever testes de exemplo para perfil incompleto bloqueando geração
    - **Propriedade 5: Perfil incompleto bloqueia geração de plano**
    - **Valida: Requisitos 3.1, 3.2**

  - [ ]* 8.5 Escrever testes de propriedade para isolamento de planos por usuário
    - **Propriedade 11: Planos pertencem ao usuário autenticado**
    - **Valida: Requisitos 4.4, 6.4, 7.5, 8.6, 9.7**

  - [x] 8.6 Implementar PlanService — gerenciamento de ações
    - Implementar em `app/plans/service.py`: `update_action_status()`, `delete_action()`, `generate_more_actions()`
    - `update_action_status()`: atualizar status e recalcular progresso; retornar HTTP 404 se ação não pertencer ao plano/usuário
    - `delete_action()`: verificar se é a única ação (HTTP 409), criar registro `Rejection`, recalcular progresso
    - `generate_more_actions()`: enviar ao GeminiClient perfil atual + ações existentes + rejeições; adicionar novas ações ao plano; recalcular progresso
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [ ]* 8.7 Escrever testes de propriedade para recálculo de progresso ao atualizar status
    - **Propriedade 8: Atualização de status recalcula progresso**
    - **Valida: Requisitos 7.1, 7.2, 7.3, 7.4**

  - [ ]* 8.8 Escrever testes de propriedade para registro de rejeição ao excluir ação
    - **Propriedade 9: Exclusão de ação registra rejeição**
    - **Valida: Requisito 8.2**

  - [ ]* 8.9 Escrever testes de exemplo para proteção da última ação do plano
    - **Propriedade 10: Plano com única ação não pode ter ação excluída**
    - **Valida: Requisito 8.5**

  - [x] 8.10 Implementar router de planos
    - Criar `app/plans/router.py` com todos os endpoints de `/plans` conforme tabela do design
    - Proteger todas as rotas com `get_current_user` via `Depends`
    - _Requisitos: 4.1, 5.1, 6.1, 7.1, 8.1, 9.1_

- [ ] 9. Checkpoint — Garantir que todos os testes passam
  - Garantir que todos os testes passam. Perguntar ao usuário se houver dúvidas.

- [x] 10. Implementar middleware de rate limiting
  - Criar middleware de rate limiting em `app/dependencies.py` usando Redis com sliding window
  - Chave: `rate:{user_id}`, limite: 60 req/min nas rotas de geração Gemini
  - Retornar HTTP 429 com header `Retry-After` ao exceder o limite
  - Usar `fakeredis` nos testes para mockar Redis
  - _Requisitos: 10.4, 10.5_

  - [ ]* 10.1 Escrever testes de propriedade para rate limiting
    - **Propriedade 12: Rate limiting bloqueia excesso de requisições**
    - **Valida: Requisitos 10.4, 10.5**

- [x] 11. Implementar logging estruturado e tratamento global de erros
  - Adicionar middleware de logging em `app/main.py`: registrar timestamp, método HTTP, rota, status code e tempo de resposta para cada requisição
  - Implementar handler global para exceções não tratadas retornando HTTP 500 com mensagem genérica (sem expor detalhes internos)
  - _Requisitos: RNF 3_

- [x] 12. Integração final e wiring dos módulos
  - [x] 12.1 Registrar todos os routers no `app/main.py`
    - Incluir `auth_router`, `profile_router`, `plans_router` com prefixos corretos
    - Configurar CORS para domínio do frontend
    - _Requisitos: RNF 2_

  - [x] 12.2 Criar `app/dependencies.py` completo
    - Consolidar `get_db()`, `get_current_user()` e `rate_limiter()` como dependências FastAPI reutilizáveis
    - _Requisitos: 1.7, 1.8, 1.9, 10.4_

  - [ ]* 12.3 Escrever testes de integração dos endpoints principais
    - Usar `httpx.AsyncClient` com SQLite em memória e `fakeredis`
    - Cobrir fluxo: autenticação → criação de perfil → geração de plano → atualização de ação → exclusão de ação
    - _Requisitos: 1.3, 2.9, 3.7, 7.4, 8.4_

- [ ] 13. Checkpoint final — Garantir que todos os testes passam
  - Garantir que todos os testes passam. Perguntar ao usuário se houver dúvidas.

## Notas

- Tarefas marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada tarefa referencia requisitos específicos para rastreabilidade
- Testes de propriedade usam **Hypothesis** com mínimo de 100 exemplos por propriedade (`@settings(max_examples=100)`)
- Cada teste de propriedade deve incluir o comentário: `# Feature: mentoria-ia-api, Property {N}: {texto da propriedade}`
- SQLite em memória é usado nos testes; PostgreSQL em produção (SQLAlchemy suporta ambos)
- Chamadas ao Gemini são mockadas nos testes via `unittest.mock`
