# Tarefa 5 — US5+6: Home (Lista de Planos + Exclusão)

## Objetivo

Implementar a página Home que lista todos os planos do usuário com título, data e progresso, permite ver detalhes, excluir planos e navegar para gerar novo plano.

## Dependências

- Tarefa 4 concluída (PlanDetailPage funcional)

## Referência

- **Requisitos:** US 5 — Visualizar Lista de Planos na Home + US 6 — Excluir um Plano
- **MVP:** Não existe no MVP (o MVP tem apenas 1 plano). Funcionalidade nova.

## Entregáveis

### 1. Página HomePage (`src/pages/HomePage.vue`)

Carrega planos via `plansStore.loadPlans()` ao montar.

Dois estados:
- **Com planos:** renderiza `PlanList`
- **Sem planos:** renderiza `EmptyState`

Botão "Gerar Novo Plano" sempre visível (topo ou flutuante).

### 2. PlanList (`src/components/home/PlanList.vue`)

Props: `plans: Plan[]`

Emits: `view(planId)`, `delete(planId)`

Grid/lista de `PlanCard`. Responsivo: 1 coluna mobile, 2 colunas desktop.

### 3. PlanCard (`src/components/home/PlanCard.vue`)

Props: `plan: Plan`

Emits: `view`, `delete`

Usar PrimeVue `Card` ou card custom com Tailwind. Exibe:
- Título do plano
- Data de geração (formatada: "22 Mar 2026")
- PrimeVue `ProgressBar` com percentual
- Botão "Ver Detalhes" → emite `view`
- Botão "Excluir" (ícone `Trash2`, cor vermelha sutil) → emite `delete`

### 4. EmptyState (`src/components/home/EmptyState.vue`)

Exibido quando não há planos:
- Ícone ilustrativo (ex: `Target` ou `Sparkles` do Lucide)
- Mensagem: "Você ainda não tem planos de desenvolvimento"
- Subtítulo: "Gere seu primeiro plano para começar sua jornada"
- Botão "Gerar Primeiro Plano" → navega para `/onboarding`

### 5. Exclusão de Plano

Ao clicar "Excluir" no PlanCard:
1. Exibir PrimeVue `ConfirmDialog`:
   - Mensagem: "Ao excluir este plano, você perderá seu progresso e histórico de desenvolvimento. Essa ação não pode ser desfeita."
2. Se confirmar → `plansStore.deletePlan(id)`
3. Toast sucesso: "Plano excluído. Você pode criar um novo plano a qualquer momento."
4. Se último plano excluído → lista atualiza para `EmptyState`
5. Se erro → Toast: "Não foi possível excluir o plano. Tente novamente."

### 6. Atualizar plansStore

```typescript
async loadPlans() {
  plans.value = await planService.getPlans()
}

async deletePlan(id: string) {
  await planService.deletePlan(id)
  plans.value = plans.value.filter(p => p.id !== id)
}
```

### 7. Atualizar planService mock

- `getPlans()` → retorna array de planos salvos em memória (inicialmente com 1-2 planos fake para testar)
- `deletePlan(id)` → remove do array interno

### 8. Atualizar Router

Após login com perfil existente → redirecionar para `/home` (já feito na Tarefa 1, validar).

## Critérios de Aceite (do PRD)

- [ ] Lista exibe todos os planos salvos
- [ ] Cada plano mostra: título, data de geração, progresso
- [ ] Botão "Ver Detalhes" navega para `/plan/:id`
- [ ] Botão "Excluir" com modal de confirmação
- [ ] Exclusão remove plano e atualiza lista
- [ ] Último plano excluído → exibe EmptyState
- [ ] EmptyState com mensagem orientando gerar primeiro plano
- [ ] Botão "Gerar Novo Plano" visível na Home
- [ ] Mobile-first

## Arquivos a criar/modificar

- Modificar: `src/pages/HomePage.vue`
- Criar: `src/components/home/PlanList.vue`
- Criar: `src/components/home/PlanCard.vue`
- Criar: `src/components/home/EmptyState.vue`
- Modificar: `src/stores/plansStore.ts`
- Modificar: `src/services/planService.ts`
