# Tarefa 12 — Implementar fluxo de autenticação OAuth

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Tarefas 1, 2 e 3 concluídas (paralela com Tarefas 4 e 5)
**Referência:** `backend/app/auth/router.py`, `backend/app/auth/service.py`

## Arquivos a criar

- `src/pages/AuthCallbackPage.vue`

## Arquivos a modificar

- `src/router/index.ts`
- `src/pages/LoginPage.vue`
- `src/layouts/DefaultLayout.vue`

## AuthCallbackPage.vue (criar)

Página que processa o retorno do OAuth. Fluxo:

1. Lê query params `token` e `has_profile` da URL
2. Se params ausentes → redireciona para `/` com toast de erro
3. Chama `authStore.handleCallback(token, hasProfile)`
4. Redireciona para `/home` se `has_profile === 'true'`, senão `/onboarding`
5. Mostrar spinner/loading enquanto processa

```
// TODO: requer ajuste no backend para redirecionar para o frontend com token na URL
// Esperado: backend redireciona para http://localhost:5173/auth/callback?token=xxx&has_profile=true
```

Template mínimo: centralizado na tela, `ProgressSpinner` do PrimeVue + texto "Autenticando..."

## router/index.ts

- Adicionar rota `/auth/callback` → `AuthCallbackPage.vue`
- Essa rota deve ser **pública** (não exigir autenticação no guard)
- Atualizar o `beforeEach` para permitir acesso a `/auth/callback` sem token:
  ```ts
  const publicRoutes = ['/', '/auth/callback']
  if (!publicRoutes.includes(to.path) && !auth.isAuthenticated) {
    return '/'
  }
  ```

## LoginPage.vue

- `handleLogin()` não é mais async. Chamar `authStore.loginRedirect()` que faz `window.location.href` redirect
- Remover `try/catch`, remover `loading` ref (o redirect sai da página, não precisa de loading state)
- Simplificar: o botão chama `authStore.loginRedirect()` direto

## DefaultLayout.vue

- O `user` pode ser `null` agora (não vem mais do login mock)
- Se o header mostra dados do usuário, tratar o caso `null`
- Opção: usar dados do `profileStore` se disponível, ou mostrar apenas o botão de logout sem nome

## Critério de aceite

- Rota `/auth/callback` existe e é pública
- `AuthCallbackPage.vue` processa query params e redireciona corretamente
- `LoginPage.vue` faz redirect para o backend OAuth
- Guard do router permite acesso a `/auth/callback` sem autenticação
- TODO documentado sobre ajuste necessário no backend
