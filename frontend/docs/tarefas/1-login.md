# Tarefa 1 — US1: Login com Google

## Objetivo

Implementar a página de login com botão "Entrar com Google" (mock), integrar com `authStore` e `authService`, e configurar o navigation guard para proteger rotas autenticadas.

## Dependências

- Tarefa 0 concluída (scaffold, stores, services, router)

## Referência

- **Requisitos:** US 1 — Autenticação com Google
- **MVP:** Seção `view === 'login'` do App.vue

## Entregáveis

### 1. Página de Login (`src/pages/LoginPage.vue`)

Layout centralizado com:
- Logo do app (ícone `BrainCircuit` do Lucide + texto "Mentoria.IA")
- Subtítulo: "Sua carreira impulsionada por Inteligência Artificial"
- Card com botão "Entrar com Google" (ícone SVG do Google)
- Estado de loading no botão durante autenticação

Comportamento:
- Ao clicar, chama `authStore.login()`
- Se login OK e perfil existe → redireciona para `/home`
- Se login OK e perfil não existe → redireciona para `/onboarding`
- Se já autenticado ao acessar `/` → redireciona para `/home`

### 2. Componente GoogleLoginButton (`src/components/auth/GoogleLoginButton.vue`)

Props:
- `loading: boolean`

Emits:
- `click`

Componente isolado com o botão estilizado do Google (ícone SVG + texto).

### 3. Atualizar authStore (`src/stores/authStore.ts`)

```typescript
// Estado
user: User | null
token: string | null
isAuthenticated: computed(() => !!user.value)

// Actions
async login() {
  // Chama authService.loginWithGoogle()
  // Salva user e token
  // Verifica se perfil existe via profileStore.loadProfile()
  // Retorna { hasProfile: boolean }
}

logout() {
  // Limpa user, token, localStorage
  // Router push para /
}
```

### 4. Atualizar authService (`src/services/authService.ts`)

Mock do login:
```typescript
async loginWithGoogle(): Promise<{ user: User; token: string }> {
  await delay(800)
  return {
    user: {
      id: 'google-12345',
      name: 'Alex Silva',
      email: 'alex.silva@email.com',
      photo: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex'
    },
    token: 'mock-jwt-token-xyz'
  }
}
```

### 5. Atualizar Router Guard (`src/router/index.ts`)

```typescript
router.beforeEach((to) => {
  const auth = useAuthStore()
  
  if (to.path !== '/' && !auth.isAuthenticated) {
    return '/'
  }
  
  if (to.path === '/' && auth.isAuthenticated) {
    return '/home'
  }
})
```

### 6. Atualizar DefaultLayout (`src/layouts/DefaultLayout.vue`)

- Header: logo "Mentoria.IA" à esquerda, botão logout (ícone `LogOut`) à direita
- Ao clicar logout → `authStore.logout()`
- Slot default para conteúdo da página

### 7. Estilização

- Mobile-first (funcionar em 320px)
- Usar Tailwind para layout
- Botão do Google com borda, hover sutil
- Cores: indigo-600 como primária (consistente com MVP)

## Critérios de Aceite (do PRD)

- [ ] Botão de login com Google exibido na página inicial
- [ ] Após login, verifica se perfil existe
- [ ] Se perfil existe → redireciona para Home
- [ ] Se perfil não existe → redireciona para Onboarding
- [ ] Dados do usuário armazenados após autenticação
- [ ] Guard impede acesso a rotas protegidas sem login
- [ ] Guard redireciona para Home se já logado e acessar `/`
- [ ] Botão logout funciona e redireciona para login

## Arquivos a criar/modificar

- Criar: `src/pages/LoginPage.vue`
- Criar: `src/components/auth/GoogleLoginButton.vue`
- Modificar: `src/stores/authStore.ts`
- Modificar: `src/services/authService.ts`
- Modificar: `src/router/index.ts`
- Modificar: `src/layouts/DefaultLayout.vue`
