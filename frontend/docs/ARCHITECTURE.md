# Arquitetura — MentorIA (Frontend)

> Documento completo de arquitetura do projeto: [`backend/docs/ARCHITECTURE.md`](../../backend/docs/ARCHITECTURE.md)

## Stack

- **Vue 3** (Composition API + `<script setup>`)
- **PrimeVue 4** (componentes UI, tema Aura via `@primevue/themes/aura`)
- **Tailwind CSS 4** (utilitarios)
- **Pinia** (state management)
- **Vue Router 5** (SPA routing)
- **Axios** (HTTP client)
- **Lucide Vue Next** + **PrimeIcons** (icones)
- **Vite 7** (build tool)
- **TypeScript 5.9**
- **npm-run-all2** (orquestracao de scripts de build)

## Estrutura

```
src/
├── App.vue                    # Root: Toast, ConfirmDialog, RouterView
├── main.ts                    # Bootstrap: Pinia, PrimeVue (tema Aura), Router, ToastService, ConfirmationService
├── router/index.ts            # Rotas + navigation guard (JWT)
│
├── pages/                     # Paginas (1 por rota)
│   ├── LoginPage.vue          # /
│   ├── AuthCallbackPage.vue   # /auth/callback
│   ├── OnboardingPage.vue     # /onboarding (wizard 5 steps)
│   ├── LoadingAIPage.vue      # /loading (aguarda geracao do plano)
│   ├── HomePage.vue           # /home (lista de planos)
│   └── PlanDetailPage.vue     # /plan/:id (detalhe do plano)
│
├── components/
│   ├── auth/                  # GoogleLoginButton
│   ├── onboarding/            # StepTrajetoria, StepFormacao, StepHabilidades, StepObjetivo, StepRevisao
│   ├── home/                  # EmptyState, PlanCard, PlanList
│   └── plan/                  # ActionItem, ActionTimeline, GapsList, PlanHeader, ProgressCard
│
├── composables/
│   └── useOnboarding.ts       # Logica reativa do wizard de onboarding
│
├── layouts/
│   └── DefaultLayout.vue      # Header com logo MentorIA, botao de logout e slot para conteudo
│
├── services/                  # Camada HTTP (Axios)
│   ├── api.ts                 # Instancia Axios (baseURL, interceptors JWT/401)
│   ├── authService.ts         # loginWithGoogle(), logout()
│   ├── planService.ts         # CRUD planos e acoes
│   └── profileService.ts     # get/save perfil
│
├── stores/                    # Pinia stores
│   ├── authStore.ts           # Token, autenticacao, login/logout
│   ├── plansStore.ts          # Lista planos, plano atual, acoes
│   └── profileStore.ts       # Perfil do usuario
│
├── types/                     # TypeScript types (alinhados com backend schemas)
│   ├── index.ts               # Re-exports
│   ├── user.ts                # User, TokenResponse
│   ├── profile.ts             # Seniority, EducationLevel, CareerGoal, ProfileData/Out, label maps
│   └── plan.ts                # ActionStatus, Priority, Plan, Action, Gap
│
└── assets/
    └── main.css               # Estilos globais + Tailwind
```

## Rotas

| Rota              | Pagina             | Auth | Descricao                        |
|-------------------|--------------------|------|----------------------------------|
| `/`               | LoginPage          | Nao  | Login com Google                 |
| `/auth/callback`  | AuthCallbackPage   | Nao  | Recebe token do OAuth callback   |
| `/onboarding`     | OnboardingPage     | Sim  | Wizard de perfil (5 etapas)      |
| `/loading`        | LoadingAIPage      | Sim  | Tela de loading durante geracao  |
| `/home`           | HomePage           | Sim  | Lista de planos do usuario       |
| `/plan/:id`       | PlanDetailPage     | Sim  | Detalhe do plano com acoes/gaps  |

## Navigation Guard

- Rotas publicas: `/` e `/auth/callback`
- Rotas protegidas: todas as demais (requer `token` no localStorage via `authStore.isAuthenticated`)
- Se autenticado e acessa `/` -> redireciona para `/home`

## Layout

O `DefaultLayout.vue` fornece a estrutura visual padrao para paginas autenticadas:
- Header com logo MentorIA (link para `/home`) e botao de logout
- Slot para conteudo da pagina
- Usa componentes Lucide (`BrainCircuit`, `LogOut`) e PrimeVue (`Button`)

## Comunicacao com Backend

- Base URL: `VITE_API_URL` (default: `http://localhost:8000`)
- Interceptor de request: adiciona `Authorization: Bearer {token}`
- Interceptor de response: se 401 -> limpa token e redireciona para `/`
- No Docker: Nginx faz proxy de `/api/*` para `backend:8000`

## Fluxo do Usuario

```
Login -> OAuth Google -> Callback (salva JWT)
  +-- Tem perfil? -> HomePage (lista planos)
  +-- Nao tem? -> Onboarding (5 steps) -> POST /profile
                    -> LoadingAIPage -> POST /plans (Gemini gera plano)
                    -> PlanDetailPage (visualizar/gerenciar plano)
```

## Onboarding (5 etapas)

1. **StepTrajetoria** -- Experiencias profissionais (cargo, senioridade, empresa, datas)
2. **StepFormacao** -- Formacao academica (instituicao, nivel, titulo, area, datas)
3. **StepHabilidades** -- Lista de habilidades tecnicas
4. **StepObjetivo** -- Objetivo de carreira (enum: crescer, liderar, mudar de area)
5. **StepRevisao** -- Revisao dos dados antes de enviar

## PlanDetailPage (funcionalidades)

- Visualizar gaps identificados pela IA (GapsList)
- Timeline de acoes ordenadas por sequencia (ActionTimeline)
- Marcar acao como concluida/pendente (PATCH)
- Remover acao (DELETE -- registra rejeicao no backend, retorna progresso atualizado)
- Gerar mais acoes via IA (POST /actions/generate)
- Barra de progresso calculada pelo backend

## Testes

Atualmente o frontend nao possui testes automatizados configurados.
