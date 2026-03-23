# Tarefa 3 — US3: Geração do Plano (Loading + API Mock)

## Objetivo

Implementar a tela de loading durante geração do plano pela IA, a chamada ao service mock que simula a API Gemini, e o redirect para a página de detalhes do plano gerado.

## Dependências

- Tarefa 2 concluída (onboarding salva perfil e redireciona para /loading)

## Referência

- **Requisitos:** US 3 — Receber Primeiro Plano Personalizado
- **MVP:** Seção `view === 'loading-ai'` e função `handleFinishOnboarding()`

## Entregáveis

### 1. Página LoadingAIPage (`src/pages/LoadingAIPage.vue`)

Tela fullscreen com fundo indigo:
- Spinner animado (PrimeVue `ProgressSpinner` ou CSS custom)
- Ícone `Sparkles` do Lucide
- Título: "✨ O Gemini está criando seu futuro..."
- Subtítulo motivacional em itálico

Comportamento:
1. Ao montar, chama `plansStore.generatePlan(profileStore.profile)`
2. Se sucesso → redireciona para `/plan/:id` do plano gerado
3. Se erro → exibe mensagem de erro com botão "Tentar novamente"
4. Se não tem perfil (acesso direto à URL) → redireciona para `/onboarding`

### 2. Atualizar planService mock (`src/services/planService.ts`)

`generatePlan(profile: ProfileData)` deve:
- Simular delay de 2-3 segundos
- Retornar um `Plan` fake realista baseado no perfil:

```typescript
// Exemplo de plano fake gerado
{
  id: 'plan-' + Date.now(),
  titulo: `Plano de ${profile.objetivo} — ${profile.experiencias[0]?.senioridade || 'Profissional'}`,
  criadoEm: new Date().toISOString(),
  gaps: [
    { skill: 'Gestão de Pessoas', level: 'Iniciante', ideal: 'Avançado' },
    { skill: 'Comunicação Executiva', level: 'Intermediário', ideal: 'Avançado' },
    { skill: 'Pensamento Estratégico', level: 'Iniciante', ideal: 'Intermediário' }
  ],
  acoes: [
    {
      id: 'action-1',
      prioridade: 'ALTA',
      categoria: 'Liderança',
      titulo: 'Desenvolvimento de Inteligência Emocional',
      objetivo: 'Desenvolver habilidades de gestão emocional para liderar equipes',
      contexto: 'Baseado no seu perfil como [cargo], essa competência é essencial para o próximo nível',
      concluida: false
    },
    // ... mais 4-5 ações
  ],
  progresso: 0
}
```

### 3. Atualizar plansStore (`src/stores/plansStore.ts`)

```typescript
async generatePlan(profile: ProfileData) {
  loading.value = true
  error.value = null
  try {
    const plan = await planService.generatePlan(profile)
    plans.value.push(plan)
    currentPlan.value = plan
    return plan
  } catch (e) {
    error.value = 'Não foi possível gerar o plano. Tente novamente.'
    throw e
  } finally {
    loading.value = false
  }
}
```

Expor: `loading`, `error` como refs.

### 4. Estados da página

| Estado | UI |
|---|---|
| Carregando | Spinner + mensagem motivacional |
| Sucesso | Redirect automático para `/plan/:id` |
| Erro | Mensagem de erro + botão "Tentar novamente" |
| Sem perfil | Redirect para `/onboarding` |

## Critérios de Aceite (do PRD)

- [ ] Após onboarding, dados do perfil são enviados para o service
- [ ] Tela de loading exibida durante geração
- [ ] Plano gerado contém: título automático, gaps, ações com prioridade
- [ ] Plano salvo na store (e no service mock)
- [ ] Redirect para página de detalhes do plano após sucesso
- [ ] Mensagem de erro clara se falhar, com opção de retry
- [ ] Título do plano gerado automaticamente com base no objetivo e senioridade

## Arquivos a criar/modificar

- Modificar: `src/pages/LoadingAIPage.vue` (substituir placeholder)
- Modificar: `src/services/planService.ts` (implementar generatePlan mock)
- Modificar: `src/stores/plansStore.ts` (implementar generatePlan action)
