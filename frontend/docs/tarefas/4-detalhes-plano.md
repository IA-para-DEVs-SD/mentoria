# Tarefa 4 — US4: Detalhes do Plano

## Objetivo

Implementar a página de detalhes de um plano com: cabeçalho, barra de progresso, lista de gaps, timeline de ações (concluir, excluir, gerar mais) e botão voltar para Home.

## Dependências

- Tarefa 3 concluída (plano gerado e salvo na store)

## Referência

- **Requisitos:** US 4 — Ver Detalhes de um Plano
- **MVP:** Seção `view === 'dashboard'` do App.vue (sem o chat)

## Entregáveis

### 1. Página PlanDetailPage (`src/pages/PlanDetailPage.vue`)

Recebe `id` via route params. Carrega plano da store. Container que organiza os sub-componentes:

```vue
<template>
  <DefaultLayout>
    <PlanHeader :plan="plan" :user="user" @back="router.push('/home')" />
    <ProgressCard :progresso="plan.progresso" />
    <GapsList :gaps="plan.gaps" />
    <ActionTimeline 
      :acoes="plan.acoes" 
      @toggle="handleToggle"
      @delete="handleDelete"
      @generate-more="handleGenerateMore"
    />
  </DefaultLayout>
</template>
```

Se plano não encontrado → redirect para `/home`.

### 2. PlanHeader (`src/components/plan/PlanHeader.vue`)

Props: `plan: Plan`, `user: User`

Exibe:
- Botão voltar (ícone `ChevronLeft`) → emite `back`
- Avatar do usuário
- Título do plano
- Subtítulo: nome do usuário

### 3. ProgressCard (`src/components/plan/ProgressCard.vue`)

Props: `progresso: number`

Card com fundo indigo:
- Label "Progresso do Roadmap"
- Percentual em destaque (ex: "35%")
- PrimeVue `ProgressBar` com valor dinâmico
- Ícone decorativo (Rocket do Lucide)

### 4. GapsList (`src/components/plan/GapsList.vue`)

Props: `gaps: Gap[]`

Card com lista de gaps:
- Cada gap mostra: nome da skill, nível atual, nível ideal
- Barra visual indicando o gap (ex: 30% para Iniciante, 60% para Intermediário)
- Ordenado por relevância (maior gap primeiro)

### 5. ActionTimeline (`src/components/plan/ActionTimeline.vue`)

Props: `acoes: Action[]`

Emits: `toggle(actionId)`, `delete(actionId)`, `generate-more`

Usar PrimeVue `Timeline` ou implementar timeline custom com Tailwind:
- Lista vertical de ações com linha conectora
- Cada ação renderiza `ActionItem`
- Ordenada por prioridade (ALTA → MÉDIA → BAIXA)
- Botão "Gerar mais ações" no final da timeline

### 6. ActionItem (`src/components/plan/ActionItem.vue`)

Props: `action: Action`

Emits: `toggle`, `delete`

Cada item exibe:
- Checkbox/botão para marcar como concluída (ícone `CheckCircle2` / `Circle`)
- Tag de prioridade: ALTA (vermelho), MÉDIA (amarelo), BAIXA (verde) — usar PrimeVue `Tag`
- Tag de categoria
- Título da ação (bold)
- Objetivo (descrição)
- Contexto (texto menor, personalizado)
- Botão excluir (ícone `Trash2`) — com confirmação

Quando concluída: visual atenuado (opacidade reduzida, riscado ou cinza).

### 7. ConfirmModal (`src/components/common/ConfirmModal.vue`)

Usar PrimeVue `ConfirmDialog` para confirmações de exclusão.

Mensagens conforme PRD:
- Exclusão de ação: "Essa ação removerá esta atividade do seu plano de desenvolvimento."
- Sucesso: Toast "Item removido do plano"
- Erro: Toast "Não foi possível remover o item. Tente novamente."
- Último item: Toast "Seu plano precisa ter pelo menos uma ação"

### 8. Atualizar plansStore — Actions

```typescript
async toggleAction(planId: string, actionId: string) {
  await planService.toggleAction(planId, actionId)
  // Atualiza ação local e recalcula progresso
}

async deleteAction(planId: string, actionId: string) {
  // Verificar se é o último item → bloquear
  await planService.deleteAction(planId, actionId)
  // Remove ação local e recalcula progresso
}

async generateMoreActions(planId: string) {
  const novasAcoes = await planService.generateMoreActions(planId)
  // Adiciona ao plano e recalcula progresso
}
```

Recalcular progresso: `(concluídas / total) * 100`

### 9. Atualizar planService mock

- `toggleAction()` → alterna `concluida` no plano mock
- `deleteAction()` → remove ação do array mock
- `generateMoreActions()` → retorna 2-3 ações fake novas após 1s delay

## Critérios de Aceite (do PRD)

- [ ] Cabeçalho com título, subtítulo e avatar
- [ ] Barra de progresso reflete ações concluídas / total
- [ ] Gaps listados e ordenados por relevância
- [ ] Timeline de ações ordenada por prioridade
- [ ] Cada ação mostra: prioridade, categoria, título, objetivo, contexto
- [ ] Marcar ação como concluída atualiza progresso em tempo real
- [ ] Excluir ação com confirmação prévia
- [ ] Não permite excluir última ação
- [ ] Gerar mais ações adiciona novas e recalcula progresso
- [ ] Feedback via Toast (sucesso, erro)
- [ ] Botão voltar para Home
- [ ] Mobile-first

## Arquivos a criar/modificar

- Modificar: `src/pages/PlanDetailPage.vue`
- Criar: `src/components/plan/PlanHeader.vue`
- Criar: `src/components/plan/ProgressCard.vue`
- Criar: `src/components/plan/GapsList.vue`
- Criar: `src/components/plan/ActionTimeline.vue`
- Criar: `src/components/plan/ActionItem.vue`
- Criar: `src/components/common/ConfirmModal.vue`
- Modificar: `src/stores/plansStore.ts`
- Modificar: `src/services/planService.ts`
