# Arquitetura — MentorIA (Frontend)

> Documento completo de arquitetura do projeto: [`backend/docs/ARCHITECTURE.md`](../../backend/docs/ARCHITECTURE.md)

## Stack

- **Vue 3** (Composition API + `<script setup>`)
- **PrimeVue 4** (componentes UI) + **Tailwind CSS 4** (utilitários)
- **Pinia** (state management)
- **Vue Router 5** (SPA routing)
- **Axios** (HTTP client)
- **Lucide Vue Next** + **PrimeIcons** (ícones)
- **Vite 7** (build tool)
- **TypeScript 5.9**

## Estrutura

```
src/
├── App.vue                    # Root: Toast, ConfirmDialog, RouterView
├── main.ts                    # Bootstrap: Pinia, PrimeVue, Router
├── router/index.ts            # Rotas + navigation guard (JWT)
│
├── pages/                     # Páginas (1 por rota)
│   ├── LoginPage.vue          # /
│   ├── AuthCallbackPage.vue   # /auth/callback
│   ├── OnboardingPage.vue     # /onboarding (wizard 5 steps)
│   ├── LoadingAIPage.vue      # /loading (aguarda geração do plano)
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
│   └── useOnboarding.ts       # Lógica reativa do wizard de onboarding
│
├── services/                  # Camada HTTP (Axios)
│   ├── api.ts                 # Instância Axios (baseURL, interceptors JWT/401)
│   ├── authService.ts         # loginWithGoogle(), logout()
│   ├── planService.ts         # CRUD planos e ações
│   └── profileService.ts     # get/save perfil
│
├── stores/                    # Pinia stores
│   ├── authStore.ts           # Token, autenticação, login/logout
│   ├── plansStore.ts          # Lista planos, plano atual, ações
│   └── profileStore.ts       # Perfil do usuário
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

| Rota              | Página             | Auth | Descrição                        |
|-------------------|--------------------|------|----------------------------------|
| `/`               | LoginPage          | Não  | Login com Google                 |
| `/auth/callback`  | AuthCallbackPage   | Não  | Recebe token do OAuth callback   |
| `/onboarding`     | OnboardingPage     | Sim  | Wizard de perfil (5 etapas)      |
| `/loading`        | LoadingAIPage      | Sim  | Tela de loading durante geração  |
| `/home`           | HomePage           | Sim  | Lista de planos do usuário       |
| `/plan/:id`       | PlanDetailPage     | Sim  | Detalhe do plano com ações/gaps  |

## Navigation Guard

- Rotas públicas: `/` e `/auth/callback`
- Rotas protegidas: todas as demais (requer `token` no localStorage)
- Se autenticado e acessa `/` → redireciona para `/home`

## Comunicação com Backend

- Base URL: `VITE_API_URL` (default: `http://localhost:8000`)
- Interceptor de request: adiciona `Authorization: Bearer {token}`
- Interceptor de response: se 401 → limpa token e redireciona para `/`
- No Docker: Nginx faz proxy de `/api/*` para `backend:8000`

## Fluxo do Usuário

```
Login → OAuth Google → Callback (salva JWT)
  ├── Tem perfil? → HomePage (lista planos)
  └── Não tem? → Onboarding (5 steps) → POST /profile
                    → LoadingAIPage → POST /plans (Gemini gera plano)
                    → PlanDetailPage (visualizar/gerenciar plano)
```

## Onboarding (5 etapas)

1. **StepTrajetoria** — Experiências profissionais (cargo, senioridade, empresa, datas)
2. **StepFormacao** — Formação acadêmica (instituição, nível, título, área, datas)
3. **StepHabilidades** — Lista de habilidades técnicas
4. **StepObjetivo** — Objetivo de carreira (enum: crescer, liderar, mudar de área)
5. **StepRevisao** — Revisão dos dados antes de enviar

## PlanDetailPage (funcionalidades)

- Visualizar gaps identificados pela IA (GapsList)
- Timeline de ações ordenadas por sequência (ActionTimeline)
- Marcar ação como concluída/pendente (PATCH)
- Remover ação (DELETE — registra rejeição no backend)
- Gerar mais ações via IA (POST /actions/generate)
- Barra de progresso calculada pelo backend
