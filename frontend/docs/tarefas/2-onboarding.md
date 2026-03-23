# Tarefa 2 — US2: Onboarding (5 Etapas)

## Objetivo

Implementar o fluxo de onboarding com 5 etapas usando PrimeVue Stepper, com validação completa de formulários, múltiplos registros por etapa e persistência no profileStore.

## Dependências

- Tarefa 1 concluída (login funcional, redirect para /onboarding)

## Referência

- **Requisitos:** US 2 — Preenchimento de Perfil (Primeiro Acesso)
- **MVP:** Seção `view === 'onboarding'` do App.vue (4 steps — o real tem 5)

## Entregáveis

### 1. Página OnboardingPage (`src/pages/OnboardingPage.vue`)

Container que usa PrimeVue `Stepper` com 5 steps. Cada step renderiza seu componente.

```vue
<Stepper :value="currentStep">
  <StepList>
    <Step value="1">Trajetória</Step>
    <Step value="2">Formação</Step>
    <Step value="3">Habilidades</Step>
    <Step value="4">Objetivo</Step>
    <Step value="5">Revisão</Step>
  </StepList>
  <StepPanels>
    <StepPanel value="1">
      <StepTrajetoria v-model="profile.experiencias" />
    </StepPanel>
    <!-- ... demais steps -->
  </StepPanels>
</Stepper>
```

Botões "Voltar" e "Continuar" em cada step. "Continuar" só habilitado se step válido.

### 2. Step 1 — Trajetória Profissional (`src/components/onboarding/StepTrajetoria.vue`)

Permite múltiplos registros de experiência. Cada registro tem:

| Campo | Componente PrimeVue | Regras |
|---|---|---|
| Cargo | `InputText` | Obrigatório, alfanumérico + acentuação, sem apenas espaços |
| Senioridade | `Select` | Obrigatório. Opções: Estágio, Júnior, Pleno, Sênior, Especialista, Liderança |
| Empresa | `InputText` | Opcional |
| Data Início | `DatePicker` | Obrigatório, formato MM/AAAA, não pode ser futura |
| Data Fim | `DatePicker` | Opcional (vazio = atual), >= Data Início, não futura |

- Botão "Adicionar experiência" para múltiplos registros
- Botão remover (ícone X) em cada registro (exceto se for o único)
- Mínimo 1 experiência para avançar

### 3. Step 2 — Formação Acadêmica (`src/components/onboarding/StepFormacao.vue`)

Permite múltiplos registros. Cada registro:

| Campo | Componente PrimeVue | Regras |
|---|---|---|
| Instituição | `InputText` | Obrigatório, sem apenas espaços |
| Nível | `Select` | Obrigatório. Opções: Ensino Médio, Técnico, Tecnólogo, Bacharelado, Licenciatura, Pós-graduação, MBA, Mestrado, Doutorado, Pós-doutorado |
| Título | `InputText` | Obrigatório |
| Área de Estudo | `InputText` | Obrigatório |
| Data Início | `DatePicker` | Obrigatório, formato DD/MM/AAAA, não futura |
| Data Fim | `DatePicker` | Opcional (vazio = em andamento), >= Data Início, pode ser futura |

- Botão "Adicionar formação"
- Mínimo 1 formação para avançar

### 4. Step 3 — Habilidades (`src/components/onboarding/StepHabilidades.vue`)

- Campo `InputText` para digitar habilidade + botão adicionar (ou Enter)
- Ao adicionar, vira tag/chip (`Chip` do PrimeVue) abaixo do campo
- Cada chip tem botão remover (X)
- Campo limpa automaticamente após adicionar
- Mínimo 1 habilidade para avançar
- Não permitir duplicatas (case insensitive)
- **(Desejável)** Sugestões pré-definidas como chips clicáveis:
  `["React", "Node.js", "Python", "Liderança", "Gestão de Projetos", "UI/UX", "SQL", "Cloud Computing", "Agile", "Inglês"]`

### 5. Step 4 — Objetivo de Carreira (`src/components/onboarding/StepObjetivo.vue`)

- Lista de opções como botões/cards selecionáveis (1 seleção apenas):
  - "Crescer na carreira atual"
  - "Assumir cargos de liderança"
  - "Mudar de área"
- Estado visual claro: não selecionado, selecionado (destaque), hover
- Obrigatório selecionar 1 para avançar

### 6. Step 5 — Revisão (`src/components/onboarding/StepRevisao.vue`)

Resumo de todos os dados preenchidos:
- Lista de experiências (cargo, senioridade, empresa, período)
- Lista de formações (instituição, nível, título, período)
- Chips de habilidades
- Objetivo selecionado

Botão "✨ Gerar Mentoria IA" que:
1. Chama `profileStore.saveProfile()`
2. Redireciona para `/loading`

### 7. Composable useOnboarding (`src/composables/useOnboarding.ts`)

```typescript
// Lógica compartilhada do onboarding
export function useOnboarding() {
  const currentStep = ref('1')
  
  function isStepValid(step: string): boolean { /* validação por step */ }
  function nextStep() { /* avança se válido */ }
  function prevStep() { /* volta */ }
  
  return { currentStep, isStepValid, nextStep, prevStep }
}
```

### 8. Atualizar profileStore (`src/stores/profileStore.ts`)

- Estado `profile` do tipo `ProfileData`
- `saveProfile()` → chama `profileService.saveProfile()`
- `loadProfile()` → chama `profileService.getProfile()`
- `hasProfile` → computed que verifica se perfil existe

## Validação

Cada step valida seus campos antes de permitir avanço:
- Campos obrigatórios preenchidos
- Datas válidas (início <= fim, não futuras onde aplicável)
- Mínimo 1 registro onde exigido
- Feedback visual de erro (mensagem abaixo do campo)

Usar PrimeVue `Message` ou classes de erro nativas dos componentes.

## Critérios de Aceite (do PRD)

- [ ] 5 etapas de onboarding apresentadas com stepper visual
- [ ] Navegação entre etapas (voltar/avançar)
- [ ] Não permite pular etapas obrigatórias (validação)
- [ ] Múltiplos registros de experiência profissional
- [ ] Múltiplos registros de formação acadêmica
- [ ] Habilidades como chips com adição/remoção
- [ ] Sem duplicatas de habilidades
- [ ] Objetivo: seleção única obrigatória
- [ ] Revisão mostra todos os dados
- [ ] Ao concluir, salva perfil e redireciona para /loading
- [ ] Mobile-first (funciona em 320px)

## Arquivos a criar/modificar

- Criar: `src/pages/OnboardingPage.vue`
- Criar: `src/components/onboarding/StepTrajetoria.vue`
- Criar: `src/components/onboarding/StepFormacao.vue`
- Criar: `src/components/onboarding/StepHabilidades.vue`
- Criar: `src/components/onboarding/StepObjetivo.vue`
- Criar: `src/components/onboarding/StepRevisao.vue`
- Criar: `src/composables/useOnboarding.ts`
- Modificar: `src/stores/profileStore.ts`
