# Tarefa 6 — US7: Gerar Novo Plano (Pré-preenchimento)

## Objetivo

Implementar o fluxo de gerar novo plano a partir da Home, reaproveitando o onboarding com dados pré-preenchidos do perfil salvo, permitindo edição antes de gerar.

## Dependências

- Tarefa 5 concluída (Home com botão "Gerar Novo Plano")
- Tarefa 2 concluída (OnboardingPage funcional)

## Referência

- **Requisitos:** US 7 — Gerar Novo Plano (Acessos Posteriores)
- **MVP:** Botão "Editar Mapa" no nav do MVP (conceito similar)

## Entregáveis

### 1. Botão "Gerar Novo Plano" na Home

Já existe na Tarefa 5. Ao clicar → navega para `/onboarding?mode=new-plan`.

### 2. Atualizar OnboardingPage — Modo pré-preenchido

Detectar query param `mode=new-plan`:

```typescript
const route = useRoute()
const isNewPlan = computed(() => route.query.mode === 'new-plan')
```

Se `isNewPlan`:
- Carregar dados do perfil salvo via `profileStore.loadProfile()`
- Pré-preencher todos os campos dos 5 steps com os dados existentes
- Usuário pode editar qualquer campo
- Botão final muda de "✨ Gerar Mentoria IA" para "✨ Gerar Novo Plano"

Se não é `isNewPlan` (primeiro acesso):
- Comportamento normal (campos vazios)

### 3. Atualizar composable useOnboarding

Adicionar função `prefillFromProfile(profile: ProfileData)`:
- Popula os refs/reactive dos steps com dados do perfil
- Chamada no `onMounted` se `isNewPlan`

### 4. Atualizar profileStore

- `saveProfile()` deve atualizar o perfil existente (não criar novo)
- Após salvar, o fluxo segue igual: redirect para `/loading` → gera plano → redirect para `/plan/:id`

### 5. Fluxo completo

```
Home → "Gerar Novo Plano" → /onboarding?mode=new-plan
  → Campos pré-preenchidos com perfil salvo
  → Usuário edita o que quiser
  → Clica "Gerar Novo Plano"
  → profileStore.saveProfile() (atualiza perfil)
  → Redirect /loading
  → plansStore.generatePlan() (gera NOVO plano, não substitui)
  → Redirect /plan/:id (novo plano)
  → Novo plano aparece na Home
```

## Critérios de Aceite (do PRD)

- [ ] Botão "Gerar Novo Plano" na Home abre onboarding
- [ ] Campos pré-preenchidos com dados do perfil salvo
- [ ] Usuário pode modificar qualquer informação
- [ ] Ao confirmar, gera novo plano via API (mock)
- [ ] Novo plano salvo e adicionado à lista
- [ ] Redirect para página de detalhes do novo plano
- [ ] Plano anterior permanece na lista (não é substituído)

## Arquivos a criar/modificar

- Modificar: `src/pages/OnboardingPage.vue` (detectar mode, pré-preencher)
- Modificar: `src/composables/useOnboarding.ts` (prefillFromProfile)
- Modificar: `src/stores/profileStore.ts` (update profile)
- Modificar: `src/pages/HomePage.vue` (link com query param)
