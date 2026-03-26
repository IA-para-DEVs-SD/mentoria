# Tarefa 10 — Atualizar componentes de onboarding para novos tipos

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Tarefas 1, 2 e 3 concluídas
**Referência:** Tipos e labels da Tarefa 1

## Arquivos a modificar

- `src/components/onboarding/StepTrajetoria.vue`
- `src/components/onboarding/StepFormacao.vue`
- `src/components/onboarding/StepHabilidades.vue`
- `src/components/onboarding/StepObjetivo.vue`
- `src/components/onboarding/StepRevisao.vue`
- `src/composables/useOnboarding.ts`
- `src/pages/OnboardingPage.vue`
- `src/pages/LoadingAIPage.vue`

## StepTrajetoria.vue

- Tipo do model: `Experiencia[]` → `ExperienceForm[]`
- Campos: `exp.cargo` → `exp.role`, `exp.senioridade` → `exp.seniority`, `exp.empresa` → `exp.company`, `exp.dataInicio` → `exp.startDate`, `exp.dataFim` → `exp.endDate`
- Array `SENIORIDADES` (strings em português) → usar `SENIORITY_LABELS` da Tarefa 1
- O `Select` deve mostrar labels em português mas salvar o valor do enum do backend. Usar formato `{ label: string, value: string }` no options:
  ```ts
  const SENIORITY_OPTIONS = Object.entries(SENIORITY_LABELS).map(([value, label]) => ({ label, value }))
  ```
- No Select: `optionLabel="label"` e `optionValue="value"`

## StepFormacao.vue

- Tipo do model: `Formacao[]` → `EducationForm[]`
- Campos: `form.instituicao` → `form.institution`, `form.nivel` → `form.level`, `form.titulo` → `form.title`, `form.areaEstudo` → `form.studyArea`, `form.dataInicio` → `form.startDate`, `form.dataFim` → `form.endDate`
- `NIVEIS` → usar `EDUCATION_LEVEL_LABELS`. Select com `{ label, value }`.

## StepHabilidades.vue

- Mudança mínima — só o tipo do model se mudou o nome (`habilidades` → `skills` é no pai, não aqui). O model continua sendo `string[]`.

## StepObjetivo.vue

- Tipo do model: `ObjetivoCarreira | null` → `CareerGoal | null`
- `OBJETIVOS` → usar `CAREER_GOAL_LABELS`. Os values passam a ser `Crescer_na_carreira_atual`, etc. Labels continuam em português.

## StepRevisao.vue

- Atualizar todos os acessos de campos para os novos nomes
- Usar mapas de labels para exibir valores legíveis:
  - `exp.senioridade` → `SENIORITY_LABELS[exp.seniority]`
  - `form.nivel` → `EDUCATION_LEVEL_LABELS[form.level]`
  - `profile.objetivo` → `CAREER_GOAL_LABELS[profile.careerGoal]`

## useOnboarding.ts

- Atualizar tipo do parâmetro: `ProfileData` → `ProfileForm`
- Atualizar referências de campos nas validações:
  - `profile.experiencias` → `profile.experiences`
  - `e.cargo` → `e.role`
  - `e.senioridade` → `e.seniority`
  - `e.dataInicio` → `e.startDate`
  - `profile.formacoes` → `profile.educations`
  - `f.instituicao` → `f.institution`
  - `f.nivel` → `f.level`
  - `f.titulo` → `f.title`
  - `f.areaEstudo` → `f.studyArea`
  - `f.dataInicio` → `f.startDate`
  - `profile.habilidades` → `profile.skills`
  - `profile.objetivo` → `profile.careerGoal`

## OnboardingPage.vue

- Tipo do `profile` reactive: `ProfileData` → `ProfileForm`
- Atualizar acessos: `profile.experiencias` → `profile.experiences`, `profile.formacoes` → `profile.educations`, `profile.habilidades` → `profile.skills`, `profile.objetivo` → `profile.careerGoal`
- No `handleFinish()`: converter `ProfileForm` → formato da API (datas `Date` → `string` formato `YYYY-MM-DD`) antes de chamar `profileStore.saveProfile()`

## LoadingAIPage.vue

- `plansStore.generatePlan(profileStore.profile)` → `plansStore.generatePlan()` (sem parâmetro)

## Critério de aceite

- Onboarding funciona com os novos tipos
- Selects mostram labels em português, salvam valores do enum do backend
- Validações funcionam com os novos nomes de campos
- `npm run type-check` passa para esses arquivos
