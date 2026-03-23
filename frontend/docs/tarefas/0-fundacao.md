# Tarefa 0 — Fundação do Projeto Frontend

## Objetivo

Criar o projeto Vue 3 do zero dentro de `grupo-6-mentoria/frontend/`, instalar todas as dependências, configurar ferramentas e criar a estrutura base (types, services mock, router, stores vazias) para que as próximas tarefas possam focar apenas em features.

## Pré-requisitos

- Node.js 20+
- npm

## Entregáveis

### 1. Scaffold do projeto

```bash
cd /home/paulo/dev/work/grupo-6-mentoria
npm create vue@latest frontend -- --typescript --router --pinia
```

### 2. Instalar dependências

```bash
cd frontend
npm install primevue @primevue/themes primeicons axios lucide-vue-next
npm install -D tailwindcss @tailwindcss/vite
```

### 3. Configurar Vite (`vite.config.ts`)

- Plugin Vue
- Plugin Tailwind CSS (`@tailwindcss/vite`)
- Alias `@` → `src/`

### 4. Configurar PrimeVue (`main.ts`)

- Registrar plugin PrimeVue com tema Aura
- Registrar serviços: ToastService, ConfirmationService
- Importar PrimeIcons CSS

```typescript
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import 'primeicons/primeicons.css'

app.use(PrimeVue, { theme: { preset: Aura } })
app.use(ToastService)
app.use(ConfirmationService)
```

### 5. Configurar Tailwind CSS (`src/assets/main.css`)

```css
@import "tailwindcss";
```

### 6. Criar estrutura de pastas

```
src/
├── assets/
├── components/
│   ├── common/
│   ├── auth/
│   ├── onboarding/
│   ├── home/
│   └── plan/
├── composables/
├── layouts/
├── pages/
├── router/
├── stores/
├── services/
├── types/
└── utils/
```

### 7. Criar Types (`src/types/`)

**`src/types/user.ts`**
```typescript
export interface User {
  id: string
  name: string
  email: string
  photo: string
}
```

**`src/types/profile.ts`**
```typescript
export interface Experiencia {
  cargo: string
  senioridade: 'Estágio' | 'Júnior' | 'Pleno' | 'Sênior' | 'Especialista' | 'Liderança'
  empresa?: string
  dataInicio: string
  dataFim?: string
}

export interface Formacao {
  instituicao: string
  nivel: string
  titulo: string
  areaEstudo: string
  dataInicio: string
  dataFim?: string
}

export interface ProfileData {
  experiencias: Experiencia[]
  formacoes: Formacao[]
  habilidades: string[]
  objetivo: 'Crescer na carreira atual' | 'Assumir cargos de liderança' | 'Mudar de área'
}
```

**`src/types/plan.ts`**
```typescript
export interface Gap {
  skill: string
  level: string
  ideal: string
}

export interface Action {
  id: string
  prioridade: 'ALTA' | 'MÉDIA' | 'BAIXA'
  categoria: string
  titulo: string
  objetivo: string
  contexto: string
  concluida: boolean
}

export interface Plan {
  id: string
  titulo: string
  criadoEm: string
  gaps: Gap[]
  acoes: Action[]
  progresso: number
}
```

**`src/types/index.ts`** — Re-exportar tudo.

### 8. Criar Services Mock (`src/services/`)

**`src/services/api.ts`** — Instância Axios com baseURL placeholder e interceptors (token no header, tratamento de 401).

**`src/services/authService.ts`** — Mock:
- `loginWithGoogle()` → retorna User fake após 500ms delay
- `logout()` → limpa dados
- `refreshToken()` → placeholder

**`src/services/profileService.ts`** — Mock:
- `getProfile()` → retorna null (primeiro acesso) ou ProfileData salvo
- `saveProfile(data)` → salva em memória/localStorage

**`src/services/planService.ts`** — Mock:
- `getPlans()` → retorna array de Plans fake
- `getPlanById(id)` → retorna Plan fake
- `generatePlan(profile)` → retorna Plan fake após 2s delay (simula IA)
- `deletePlan(id)` → remove do array
- `toggleAction(planId, actionId)` → alterna concluida
- `deleteAction(planId, actionId)` → remove ação
- `generateMoreActions(planId)` → adiciona ações fake

Os dados fake devem ser realistas (cargos, habilidades e gaps em português).

### 9. Criar Stores vazias (`src/stores/`)

**`src/stores/authStore.ts`** — `user`, `token`, `isAuthenticated`, actions: `login()`, `logout()`

**`src/stores/profileStore.ts`** — `profile`, actions: `loadProfile()`, `saveProfile()`

**`src/stores/plansStore.ts`** — `plans`, `currentPlan`, actions: `loadPlans()`, `loadPlan(id)`, `generatePlan()`, `deletePlan()`, `toggleAction()`, `deleteAction()`, `generateMoreActions()`

Todas usando `defineStore` com setup syntax, chamando os services.

### 10. Criar Router base (`src/router/index.ts`)

Rotas:
```
/              → LoginPage
/home          → HomePage
/onboarding    → OnboardingPage
/loading       → LoadingAIPage
/plan/:id      → PlanDetailPage
```

Navigation guard: redirecionar para `/` se não autenticado (exceto rota `/`).

### 11. Criar Layout (`src/layouts/DefaultLayout.vue`)

Header com logo "Mentoria.IA" + botão logout. Slot para conteúdo. Usar apenas quando autenticado.

### 12. Criar páginas placeholder (`src/pages/`)

Cada página com apenas um `<h1>` com o nome da página, para validar que o router funciona:
- `LoginPage.vue`
- `HomePage.vue`
- `OnboardingPage.vue`
- `LoadingAIPage.vue`
- `PlanDetailPage.vue`

### 13. Validação final

```bash
npm run build   # deve compilar sem erros
npm run dev     # deve abrir no browser e navegar entre páginas
```

## Critérios de Aceite

- [ ] `npm run build` compila sem erros
- [ ] `npm run dev` abre no browser
- [ ] PrimeVue configurado (testar um `<Button label="Test" />` em qualquer página)
- [ ] Tailwind funcionando (testar uma classe como `class="text-red-500"`)
- [ ] Router navega entre todas as páginas placeholder
- [ ] Guard redireciona para login se não autenticado
- [ ] Types exportados e importáveis
- [ ] Services mock retornam dados fake
- [ ] Stores funcionais (chamam services)

## Arquivos a criar

~25 arquivos. Nenhum arquivo existente é modificado.
