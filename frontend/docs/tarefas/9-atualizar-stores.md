# Tarefa 9 — Atualizar stores para os novos tipos e contratos

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Tarefas 1 e 2 concluídas
**Referência:** Services da Tarefa 2, tipos da Tarefa 1

## Arquivos a modificar

- `src/stores/authStore.ts`
- `src/stores/profileStore.ts`
- `src/stores/plansStore.ts`

## authStore.ts

O fluxo de login mudou — `loginWithGoogle()` agora faz redirect (não retorna nada).

- **Remover** o método `login()` que faz `await authService.loginWithGoogle()` e retorna `{ hasProfile }`
- **Adicionar** método `loginRedirect()` que chama `authService.loginWithGoogle()` (redirect, sem await)
- **Adicionar** método `handleCallback(token: string, hasProfile: boolean)`:
  - Salva token no localStorage
  - Atualiza `token.value`
  - Retorna `hasProfile` para que o caller decida a rota
- `isAuthenticated` — verificar apenas se tem token no localStorage
- `logout()` — limpa token e user do localStorage e do state
- **Remover** referência a `refreshToken`
- O `user` não vem mais do login mock. O backend não tem `GET /auth/me`. Opções:
  - Manter `user` como `null` até carregar o perfil
  - Ou remover `user` do authStore e usar `profileStore` quando precisar de dados do usuário
  - **Implementar:** manter `user` no state mas como opcional. Não bloquear funcionalidade se `user` for null.

## profileStore.ts

- Atualizar tipo: `ProfileData` → novo tipo da Tarefa 1 (tipo de API, não de form)
- `loadProfile()` — chama `profileService.getProfile()`. Tratar 404 como `profile = null` (não é erro)
- `saveProfile(data)` — chama `profileService.saveProfile(data)`. Recebe dados já convertidos (datas como string)

## plansStore.ts

- Atualizar todos os nomes de campos nos tipos: `Plan` com `name`, `created_at`, `actions`, `progress`
- **`generatePlan()`** — remover parâmetro `ProfileData`. Chamar `planService.generatePlan()` sem argumentos
- **`toggleAction()`** → renomear para **`updateActionStatus(planId, actionId, status)`**:
  - Chamar `planService.updateActionStatus(planId, actionId, status)`
  - Após sucesso, recarregar o plano completo via `loadPlan(planId)` para manter consistência
- **`deleteAction(planId, actionId)`**:
  - Backend retorna `{ progress }`. Atualizar `currentPlan.progress` e remover a ação da lista local
  - Ou recarregar o plano completo via `loadPlan(planId)`
- **`generateMoreActions(planId)`**:
  - Backend retorna `ActionOut[]`. Recarregar o plano completo via `loadPlan(planId)` para manter consistência

## Critério de aceite

- Stores compilam sem erros de tipo
- Lógica de chamada API correta (sem mocks)
- Sem referências a nomes antigos em português (`acoes`, `progresso`, `titulo`, etc.)
- `authStore` tem `loginRedirect()` e `handleCallback()`
- `plansStore.generatePlan()` não recebe parâmetro
