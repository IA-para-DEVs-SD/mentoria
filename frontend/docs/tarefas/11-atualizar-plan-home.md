# Tarefa 11 — Atualizar componentes de plano e home para novos tipos

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Tarefas 1, 2 e 3 concluídas (paralela com Tarefas 4 e 6)
**Referência:** Tipos da Tarefa 1, stores da Tarefa 3

## Arquivos a modificar

- `src/components/home/PlanCard.vue`
- `src/components/home/PlanList.vue`
- `src/components/plan/PlanHeader.vue`
- `src/components/plan/ProgressCard.vue`
- `src/components/plan/GapsList.vue`
- `src/components/plan/ActionTimeline.vue`
- `src/components/plan/ActionItem.vue`
- `src/pages/HomePage.vue`
- `src/pages/PlanDetailPage.vue`

## PlanCard.vue

| Antes | Depois |
|---|---|
| `plan.titulo` | `plan.name` |
| `plan.criadoEm` | `plan.created_at` |
| `plan.progresso` | `plan.progress` |

## PlanList.vue

- Tipo da prop `plans`: `Plan[]` → `PlanSummary[]` (a home só precisa do resumo, que não tem `gaps` nem `actions`)

## PlanHeader.vue

- `plan.titulo` → `plan.name`
- `user.photo` → `user.photo_url`
- Tratar `photo_url` null — usar avatar placeholder (ex: `https://api.dicebear.com/7.x/avataaars/svg?seed=default` ou um ícone genérico)

## ProgressCard.vue

- Prop `progresso` → `progress` (renomear a prop)

## GapsList.vue

Gaps mudaram completamente:

| Antes | Depois |
|---|---|
| `gap.skill` (string) | `gap.description` (string) |
| `gap.level` (texto: "Iniciante", "Intermediário") | `gap.relevance` (number 1-10) |
| `gap.ideal` (texto) | — (removido) |

- Remover a função `gapWidth()` baseada em texto
- Usar `gap.relevance` para a barra de progresso: `width: ${gap.relevance * 10}%`
- Exibir `gap.description` como label
- Exibir `gap.relevance` como número (ex: "Relevância: 8/10")

## ActionItem.vue

| Antes | Depois |
|---|---|
| `action.prioridade` | `action.priority` |
| `action.categoria` | `action.category` |
| `action.titulo` | `action.title` |
| `action.objetivo` | `action.objective` |
| `action.contexto` | `action.context` |
| `action.concluida` (boolean) | `action.status === 'concluida'` |

- `PRIORITY_SEVERITY`: key `'MÉDIA'` → `'MEDIA'`
- Atualizar aria-labels e condicionais que usavam `action.concluida`

## ActionTimeline.vue

- Prop `acoes` → `actions`
- Atualizar referências no template: `acoes` → `actions`, `acao` → `action` (no v-for)

## PlanDetailPage.vue

- `currentPlan.progresso` → `currentPlan.progress`
- `currentPlan.acoes` → `currentPlan.actions`
- `currentPlan.acoes.length <= 1` → `currentPlan.actions.length <= 1`
- `plansStore.toggleAction(id, actionId)` → `plansStore.updateActionStatus(id, actionId, newStatus)`
  - Determinar o novo status: `action.status === 'pendente' ? 'concluida' : 'pendente'`
  - O `handleToggle` precisa receber o action completo (ou o status atual) para calcular o toggle
- Passar `actions` em vez de `acoes` para `ActionTimeline`
- Passar `progress` em vez de `progresso` para `ProgressCard`

## HomePage.vue

- Verificar se `plans` agora é `PlanSummary[]` e ajustar tipagem se necessário
- Sem mudanças estruturais grandes

## Critério de aceite

- Todas as páginas e componentes compilam sem erros de tipo
- Nenhuma referência a nomes antigos em português (`titulo`, `criadoEm`, `acoes`, `progresso`, `prioridade`, `categoria`, `concluida`, etc.)
- Gaps exibem `description` e barra baseada em `relevance`
- Actions usam `status` em vez de `concluida`
