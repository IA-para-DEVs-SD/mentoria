# Tarefa 8 — Reescrever services para usar API real

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Tarefa 1 concluída
**Referência:** `backend/app/auth/router.py`, `backend/app/profile/router.py`, `backend/app/plans/router.py`

## Arquivos a modificar

- `src/services/authService.ts`
- `src/services/profileService.ts`
- `src/services/planService.ts`

## Contexto

Substituir toda a lógica mock por chamadas HTTP via `api.ts` (Axios). O `api.ts` já está configurado com baseURL e interceptors — não mexer nele.

## authService.ts

O fluxo de login muda completamente. O backend usa OAuth redirect flow:

1. Frontend redireciona o browser para `GET /auth/google/login` (backend retorna redirect para o Google)
2. Google autentica e redireciona para `GET /auth/google/callback?code=...` (no backend)
3. Backend retorna `{ access_token, token_type, has_profile }`

**NOTA IMPORTANTE:** O backend atual retorna o `TokenResponse` diretamente no `GET /auth/google/callback`, sem redirect para o frontend. O agente deve:
1. Implementar o `authService` assumindo que o backend será ajustado para redirecionar para o frontend com token na URL
2. Deixar um comentário `// TODO: requer ajuste no backend para redirecionar para o frontend com token na URL`
3. A página `AuthCallbackPage.vue` será criada na Tarefa 6

Métodos:
- `loginWithGoogle()` — `window.location.href = '${API_BASE_URL}/auth/google/login'` (onde `API_BASE_URL` vem de `import.meta.env.VITE_API_URL`)
- `logout()` — limpa localStorage (token)
- **Remover** `refreshToken()` (backend não tem esse endpoint)
- **Remover** `delay()` e todo mock

## profileService.ts

Remover toda lógica de localStorage. Usar API:

| Método | HTTP | Endpoint | Body | Retorno |
|---|---|---|---|---|
| `getProfile()` | GET | `/profile` | — | `ProfileOut` ou `null` (tratar 404) |
| `saveProfile(data)` | POST | `/profile` | `ProfileIn` | `ProfileOut` |

Converter datas `Date` → `string` (formato `YYYY-MM-DD`) antes de enviar ao backend.

## planService.ts

Remover todo o mock (arrays em memória, delays, funções `buildTitle`, `buildGaps`, `buildAcoes`, `createMockPlan`, `calcProgress`).

| Método | HTTP | Endpoint | Body | Retorno |
|---|---|---|---|---|
| `getPlans()` | GET | `/plans` | — | `PlanSummary[]` |
| `getPlanById(id)` | GET | `/plans/${id}` | — | `PlanOut` |
| `generatePlan()` | POST | `/plans` | — (sem body) | `PlanOut` |
| `deletePlan(id)` | DELETE | `/plans/${id}` | — | void (204) |
| `updateActionStatus(planId, actionId, status)` | PATCH | `/plans/${planId}/actions/${actionId}` | `{ status }` | `ActionOut` |
| `deleteAction(planId, actionId)` | DELETE | `/plans/${planId}/actions/${actionId}` | — | `{ progress }` |
| `generateMoreActions(planId)` | POST | `/plans/${planId}/actions/generate` | — | `ActionOut[]` |

**Atenção:** `generatePlan()` não recebe mais `ProfileData` como parâmetro — o backend usa o perfil já salvo no banco.

## Critério de aceite

- Nenhum mock restante nos services (sem `delay()`, sem arrays em memória, sem dados hardcoded)
- Todos os métodos fazem chamadas HTTP reais via `api.ts`
- Tipos de entrada/saída corretos conforme Tarefa 1
- `profileService` converte datas Date ↔ string
