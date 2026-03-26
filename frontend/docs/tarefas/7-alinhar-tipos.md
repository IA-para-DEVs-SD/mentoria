# Tarefa 7 — Alinhar tipos TypeScript com os schemas do backend

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Nenhuma
**Referência:** `backend/app/auth/schemas.py`, `backend/app/profile/schemas.py`, `backend/app/plans/schemas.py`

## Arquivos a modificar

- `src/types/user.ts`
- `src/types/profile.ts`
- `src/types/plan.ts`
- `src/types/index.ts`

## Contexto

Os tipos do frontend usam nomes em português e valores com acentos. O backend usa snake_case em inglês e enums sem acentos. Reescrever os tipos para refletir exatamente o contrato do backend.

## Mapeamento de campos

### User (`backend: UserOut`)

| Frontend atual | Backend | Observação |
|---|---|---|
| `photo: string` | `photo_url: string \| null` | Pode ser null |
| `id: string` | `id: UUID` | UUID vem como string no JSON |

### Profile (`backend: ProfileIn / ProfileOut`)

| Frontend atual | Backend |
|---|---|
| `experiencias` | `experiences` |
| `formacoes` | `educations` |
| `habilidades` | `skills` |
| `objetivo` | `career_goal` |
| `Experiencia.cargo` | `Experience.role` |
| `Experiencia.senioridade` | `Experience.seniority` |
| `Experiencia.empresa` | `Experience.company` |
| `Experiencia.dataInicio` | `Experience.start_date` |
| `Experiencia.dataFim` | `Experience.end_date` |
| `Formacao.instituicao` | `Education.institution` |
| `Formacao.nivel` | `Education.level` |
| `Formacao.titulo` | `Education.title` |
| `Formacao.areaEstudo` | `Education.study_area` |

### Enums

| Frontend atual | Backend | Valores |
|---|---|---|
| `Senioridade` | `Seniority` | `Estagio`, `Junior`, `Pleno`, `Senior`, `Especialista`, `Lideranca` (sem acentos) |
| `NivelFormacao` | `EducationLevel` | `Ensino_Medio`, `Tecnico`, `Tecnologo`, `Bacharelado`, `Licenciatura`, `Pos_graduacao`, `MBA`, `Mestrado`, `Doutorado`, `Pos_doutorado` |
| `ObjetivoCarreira` | `CareerGoal` | `Crescer_na_carreira_atual`, `Assumir_cargos_de_lideranca`, `Mudar_de_area` |

### Plan (`backend: PlanOut / PlanSummary`)

| Frontend atual | Backend |
|---|---|
| `titulo` | `name` |
| `criadoEm` | `created_at` |
| `acoes` | `actions` |
| `progresso` | `progress` |
| `Gap.skill` | `Gap.description` |
| `Gap.level` / `Gap.ideal` | `Gap.relevance` (number 1-10) |
| `Action.prioridade` | `Action.priority` (`ALTA`, `MEDIA`, `BAIXA` — sem acento) |
| `Action.categoria` | `Action.category` |
| `Action.titulo` | `Action.title` |
| `Action.objetivo` | `Action.objective` |
| `Action.contexto` | `Action.context` |
| `Action.concluida: boolean` | `Action.status: 'pendente' \| 'concluida'` |
| — | `Action.sequence: number` (novo) |
| — | `Gap.id: string` (novo) |

## O que criar

### Tipos auxiliares de API

- `TokenResponse` — `{ access_token: string; token_type: string; has_profile: boolean }`
- `ActionStatusUpdate` — `{ status: 'pendente' | 'concluida' }`
- `ProgressOut` — `{ progress: number }`

### Mapas de labels para exibição nos componentes

Os enums do backend não têm acentos. Criar mapas para exibir em português nos componentes:

```ts
export const SENIORITY_LABELS: Record<Seniority, string> = {
  Estagio: 'Estágio',
  Junior: 'Júnior',
  Pleno: 'Pleno',
  Senior: 'Sênior',
  Especialista: 'Especialista',
  Lideranca: 'Liderança',
}
```

Fazer o mesmo para `EducationLevel` e `CareerGoal`.

### Tipos de formulário vs tipos de API

Manter separação:
- **Tipos de form** (`ExperienceForm`, `EducationForm`, `ProfileForm`): usam `Date | null` para datas. Usados nos componentes de onboarding.
- **Tipos de API** (`Experience`, `Education`, `ProfileData`): usam `string` para datas. Usados nos services e stores.

## Critério de aceite

- `npm run type-check` passa (pode ter erros nos arquivos que ainda referenciam nomes antigos — serão corrigidos nas tarefas seguintes)
- Tipos refletem exatamente os schemas do backend
- Mapas de labels criados para os 3 enums
- Tipos de form e de API separados
