# Requirements Document

## Introduction

Este documento descreve os requisitos para a integração completa do frontend MentorIA com o backend FastAPI. O frontend é uma SPA em Vue 3 + PrimeVue + TypeScript que atualmente usa dados mock. O objetivo é substituir toda a camada mock por chamadas HTTP reais, alinhar os tipos TypeScript com os schemas Pydantic do backend, implementar o fluxo OAuth com Google, e garantir que o build final passe sem erros de tipo.

Os fluxos principais cobertos são: autenticação via Google OAuth, onboarding de perfil, geração de plano de mentoria via IA, e visualização/interação com planos na home e na página de detalhes.

## Glossary

- **Frontend**: Aplicação SPA em Vue 3 + PrimeVue + TypeScript
- **Backend**: API REST em FastAPI + PydanticAI + PostgreSQL
- **AuthStore**: Store Pinia responsável pelo estado de autenticação (token JWT, usuário)
- **ProfileStore**: Store Pinia responsável pelo estado do perfil do usuário
- **PlansStore**: Store Pinia responsável pelo estado dos planos de mentoria
- **AuthService**: Módulo de serviço responsável pelas chamadas HTTP de autenticação
- **ProfileService**: Módulo de serviço responsável pelas chamadas HTTP de perfil
- **PlanService**: Módulo de serviço responsável pelas chamadas HTTP de planos
- **TypeSystem**: Conjunto de tipos TypeScript do frontend (`src/types/`)
- **Router**: Vue Router responsável pela navegação e guards de rota
- **AuthCallbackPage**: Página Vue que processa o retorno do fluxo OAuth
- **OnboardingPage**: Página Vue com stepper de coleta de dados de perfil
- **LoadingAIPage**: Página Vue exibida durante a geração do plano pela IA
- **PlanDetailPage**: Página Vue com detalhes completos de um plano de mentoria
- **HomePage**: Página Vue com lista de planos do usuário
- **ProfileForm**: Tipo TypeScript para dados de formulário (datas como `Date | null`)
- **ProfileData**: Tipo TypeScript para dados de API (datas como string `YYYY-MM-DD`)
- **PlanOut**: Schema do backend com plano completo (gaps + actions)
- **PlanSummary**: Schema do backend com resumo do plano (sem gaps e actions)
- **ActionOut**: Schema do backend para uma ação do plano
- **GapOut**: Schema do backend para um gap identificado no perfil
- **TokenResponse**: Schema do backend retornado após autenticação OAuth
- **JWT**: JSON Web Token usado para autenticar requisições ao backend

---

## Requirements

### Requirement 1: Alinhamento de Tipos TypeScript com Schemas do Backend

**User Story:** Como desenvolvedor, quero que os tipos TypeScript do frontend reflitam exatamente os schemas Pydantic do backend, para que não haja divergências de contrato entre as camadas.

#### Acceptance Criteria

1. THE TypeSystem SHALL definir o tipo `User` com os campos `id: string`, `name: string`, `email: string`, `photo_url: string | null` e `created_at: string`, correspondendo ao schema `UserOut` do backend.
2. THE TypeSystem SHALL definir o tipo `Experience` com os campos `role`, `seniority`, `company`, `start_date` e `end_date` em snake_case, correspondendo ao schema `ExperienceIn/ExperienceOut` do backend.
3. THE TypeSystem SHALL definir o tipo `Education` com os campos `institution`, `level`, `title`, `study_area`, `start_date` e `end_date` em snake_case, correspondendo ao schema `EducationIn/EducationOut` do backend.
4. THE TypeSystem SHALL definir o enum `Seniority` com os valores `Estagio`, `Junior`, `Pleno`, `Senior`, `Especialista` e `Lideranca` sem acentos, correspondendo ao enum do backend.
5. THE TypeSystem SHALL definir o enum `EducationLevel` com os valores `Ensino_Medio`, `Tecnico`, `Tecnologo`, `Bacharelado`, `Licenciatura`, `Pos_graduacao`, `MBA`, `Mestrado`, `Doutorado` e `Pos_doutorado`, correspondendo ao enum do backend.
6. THE TypeSystem SHALL definir o enum `CareerGoal` com os valores `Crescer_na_carreira_atual`, `Assumir_cargos_de_lideranca` e `Mudar_de_area`, correspondendo ao enum do backend.
7. THE TypeSystem SHALL definir o tipo `PlanOut` com os campos `id`, `name`, `created_at`, `progress`, `gaps` e `actions`, correspondendo ao schema `PlanOut` do backend.
8. THE TypeSystem SHALL definir o tipo `PlanSummary` com os campos `id`, `name`, `created_at` e `progress`, correspondendo ao schema `PlanSummary` do backend.
9. THE TypeSystem SHALL definir o tipo `ActionOut` com os campos `id`, `priority`, `category`, `title`, `objective`, `context`, `status` e `sequence`, onde `status` é `'pendente' | 'concluida'` e `priority` é `'ALTA' | 'MEDIA' | 'BAIXA'`.
10. THE TypeSystem SHALL definir o tipo `GapOut` com os campos `id`, `description` e `relevance: number`, correspondendo ao schema `GapOut` do backend.
11. THE TypeSystem SHALL definir o tipo `TokenResponse` com os campos `access_token: string`, `token_type: string` e `has_profile: boolean`.
12. THE TypeSystem SHALL definir mapas de labels (`SENIORITY_LABELS`, `EDUCATION_LEVEL_LABELS`, `CAREER_GOAL_LABELS`) que mapeiam cada valor de enum para sua representação em português com acentos.
13. THE TypeSystem SHALL manter tipos de formulário separados dos tipos de API: `ExperienceForm` e `EducationForm` usam `Date | null` para datas, enquanto `Experience` e `Education` usam `string`.
14. WHEN `npm run type-check` é executado após a atualização dos tipos, THE TypeSystem SHALL compilar sem erros nos arquivos de tipos.

---

### Requirement 2: Reescrita dos Services para API Real

**User Story:** Como desenvolvedor, quero que os services do frontend façam chamadas HTTP reais ao backend, para que a aplicação funcione com dados reais em vez de mocks.

#### Acceptance Criteria

1. THE AuthService SHALL implementar o método `loginWithGoogle()` que executa `window.location.href = '${VITE_API_URL}/auth/google/login'` para iniciar o fluxo OAuth redirect.
2. THE AuthService SHALL implementar o método `logout()` que remove o token JWT do `localStorage`.
3. THE AuthService SHALL não conter nenhuma referência a `refreshToken`, dados mock, `delay()`, `setTimeout` ou arrays hardcoded.
4. THE ProfileService SHALL implementar o método `getProfile()` que faz `GET /profile` e retorna `ProfileData | null`, tratando resposta 404 como `null` sem lançar erro.
5. THE ProfileService SHALL implementar o método `saveProfile(data: ProfileData)` que faz `POST /profile` com o body serializado e retorna `ProfileOut`.
6. THE ProfileService SHALL converter campos de data do tipo `Date` para string no formato `YYYY-MM-DD` antes de enviar ao backend.
7. THE PlanService SHALL implementar o método `getPlans()` que faz `GET /plans` e retorna `PlanSummary[]`.
8. THE PlanService SHALL implementar o método `getPlanById(id: string)` que faz `GET /plans/${id}` e retorna `PlanOut`.
9. THE PlanService SHALL implementar o método `generatePlan()` que faz `POST /plans` sem body e retorna `PlanOut`.
10. THE PlanService SHALL implementar o método `deletePlan(id: string)` que faz `DELETE /plans/${id}` e retorna void.
11. THE PlanService SHALL implementar o método `updateActionStatus(planId, actionId, status)` que faz `PATCH /plans/${planId}/actions/${actionId}` com body `{ status }` e retorna `ActionOut`.
12. THE PlanService SHALL implementar o método `deleteAction(planId, actionId)` que faz `DELETE /plans/${planId}/actions/${actionId}` e retorna `{ progress: number }`.
13. THE PlanService SHALL implementar o método `generateMoreActions(planId)` que faz `POST /plans/${planId}/actions/generate` sem body e retorna `ActionOut[]`.
14. IF uma chamada HTTP retorna erro 401, THEN THE AuthService SHALL remover o token do `localStorage` e redirecionar para a página de login.
15. THE PlanService SHALL não conter nenhuma referência a dados mock, `delay()`, arrays em memória ou funções de geração de dados fake.

---

### Requirement 3: Atualização das Stores Pinia

**User Story:** Como desenvolvedor, quero que as stores Pinia usem os novos tipos e chamem os services reais, para que o estado da aplicação reflita dados do backend.

#### Acceptance Criteria

1. THE AuthStore SHALL implementar o método `loginRedirect()` que chama `authService.loginWithGoogle()` sem await (redirect síncrono).
2. THE AuthStore SHALL implementar o método `handleCallback(token: string, hasProfile: boolean)` que salva o token no `localStorage`, atualiza o estado `token` e retorna `hasProfile`.
3. THE AuthStore SHALL calcular `isAuthenticated` verificando apenas a presença do token no `localStorage`.
4. THE AuthStore SHALL implementar o método `logout()` que limpa o token e o usuário do `localStorage` e do estado reativo.
5. THE AuthStore SHALL não conter referências a `login()` com retorno de `{ hasProfile }`, `refreshToken()` ou dados mock de usuário.
6. THE AuthStore SHALL manter o campo `user` como opcional (`User | null`), sem bloquear funcionalidades quando `user` for `null`.
7. THE ProfileStore SHALL implementar o método `loadProfile()` que chama `profileService.getProfile()` e trata 404 como `profile = null`.
8. THE ProfileStore SHALL implementar o método `saveProfile(data: ProfileData)` que chama `profileService.saveProfile(data)`.
9. THE PlansStore SHALL implementar o método `generatePlan()` sem parâmetros, chamando `planService.generatePlan()`.
10. THE PlansStore SHALL implementar o método `updateActionStatus(planId, actionId, status)` que chama `planService.updateActionStatus()` e recarrega o plano completo via `loadPlan(planId)` após sucesso.
11. THE PlansStore SHALL implementar o método `deleteAction(planId, actionId)` que chama `planService.deleteAction()` e atualiza o estado local com o novo `progress` retornado.
12. THE PlansStore SHALL implementar o método `generateMoreActions(planId)` que chama `planService.generateMoreActions()` e recarrega o plano completo via `loadPlan(planId)`.
13. WHEN as stores são compiladas, THE AuthStore, ProfileStore e PlansStore SHALL compilar sem erros de tipo TypeScript.
14. THE PlansStore SHALL não conter referências a nomes de campos em português como `titulo`, `acoes`, `progresso`, `prioridade`, `categoria` ou `concluida` como nome de campo.

---

### Requirement 4: Fluxo de Autenticação OAuth

**User Story:** Como usuário, quero fazer login com minha conta Google, para que eu possa acessar o MentorIA de forma segura sem criar uma senha.

#### Acceptance Criteria

1. WHEN o usuário clica no botão de login, THE Router SHALL redirecionar o browser para `${VITE_API_URL}/auth/google/login` via `window.location.href`.
2. THE Router SHALL registrar a rota `/auth/callback` mapeada para `AuthCallbackPage.vue` como rota pública.
3. THE Router SHALL permitir acesso às rotas `/` e `/auth/callback` sem token JWT válido no `localStorage`.
4. WHEN o usuário acessa qualquer rota que não seja `/` ou `/auth/callback` sem token JWT, THE Router SHALL redirecionar para `/`.
5. WHEN a `AuthCallbackPage` é carregada, THE AuthCallbackPage SHALL ler os query params `token` e `has_profile` da URL.
6. WHEN os query params `token` e `has_profile` estão presentes, THE AuthCallbackPage SHALL chamar `authStore.handleCallback(token, hasProfile)` para persistir o token.
7. WHEN `has_profile` é `'true'`, THE AuthCallbackPage SHALL redirecionar para `/home` após processar o callback.
8. WHEN `has_profile` é `'false'`, THE AuthCallbackPage SHALL redirecionar para `/onboarding` após processar o callback.
9. IF os query params `token` ou `has_profile` estão ausentes na URL, THEN THE AuthCallbackPage SHALL redirecionar para `/` e exibir uma mensagem de erro via toast.
10. WHILE o callback OAuth está sendo processado, THE AuthCallbackPage SHALL exibir um `ProgressSpinner` do PrimeVue com o texto "Autenticando...".
11. THE LoginPage SHALL chamar `authStore.loginRedirect()` diretamente no handler do botão, sem `async/await` e sem estado de loading local.

---

### Requirement 5: Atualização dos Componentes de Onboarding

**User Story:** Como usuário, quero preencher meu perfil profissional no onboarding, para que a IA possa gerar um plano de mentoria personalizado.

#### Acceptance Criteria

1. THE StepTrajetoria SHALL usar o tipo `ExperienceForm[]` para o model, com campos `role`, `seniority`, `company`, `startDate` e `endDate`.
2. THE StepTrajetoria SHALL exibir as opções de senioridade usando `SENIORITY_LABELS` com formato `{ label: string, value: Seniority }`, onde o Select salva o valor do enum e exibe o label em português.
3. THE StepFormacao SHALL usar o tipo `EducationForm[]` para o model, com campos `institution`, `level`, `title`, `studyArea`, `startDate` e `endDate`.
4. THE StepFormacao SHALL exibir as opções de nível de formação usando `EDUCATION_LEVEL_LABELS` com formato `{ label: string, value: EducationLevel }`.
5. THE StepObjetivo SHALL usar o tipo `CareerGoal | null` para o model e exibir as opções usando `CAREER_GOAL_LABELS`.
6. THE StepRevisao SHALL exibir os valores dos enums usando os mapas de labels (`SENIORITY_LABELS`, `EDUCATION_LEVEL_LABELS`, `CAREER_GOAL_LABELS`) para mostrar texto em português com acentos.
7. THE useOnboarding SHALL usar o tipo `ProfileForm` com campos `experiences`, `educations`, `skills` e `careerGoal` nas validações.
8. WHEN o usuário conclui o onboarding, THE OnboardingPage SHALL converter o `ProfileForm` para `ProfileData` (datas `Date` → string `YYYY-MM-DD`) antes de chamar `profileStore.saveProfile()`.
9. THE LoadingAIPage SHALL chamar `plansStore.generatePlan()` sem parâmetros.
10. THE OnboardingPage SHALL não conter referências a campos em português como `experiencias`, `formacoes`, `habilidades`, `objetivo`, `cargo`, `senioridade`, `dataInicio` ou `dataFim` como nomes de campo.

---

### Requirement 6: Atualização dos Componentes de Plano e Home

**User Story:** Como usuário, quero visualizar e interagir com meus planos de mentoria, para que eu possa acompanhar meu progresso e marcar ações como concluídas.

#### Acceptance Criteria

1. THE PlanCard SHALL exibir `plan.name`, `plan.created_at` e `plan.progress` em vez dos campos em português anteriores.
2. THE PlanList SHALL usar o tipo `PlanSummary[]` para a prop `plans`.
3. THE PlanHeader SHALL exibir `plan.name` e tratar `user.photo_url` como nullable, usando um avatar placeholder quando `photo_url` for `null`.
4. THE ProgressCard SHALL aceitar a prop `progress` (em vez de `progresso`) do tipo `number`.
5. THE GapsList SHALL exibir `gap.description` como label e usar `gap.relevance * 10` como percentual para a barra de progresso.
6. THE GapsList SHALL exibir o valor numérico de `gap.relevance` no formato "Relevância: X/10".
7. THE ActionItem SHALL usar `action.status === 'concluida'` para determinar se uma ação está concluída, em vez de `action.concluida`.
8. THE ActionItem SHALL usar os campos `action.priority`, `action.category`, `action.title`, `action.objective` e `action.context` em inglês.
9. THE ActionTimeline SHALL aceitar a prop `actions` (em vez de `acoes`) do tipo `ActionOut[]`.
10. WHEN o usuário clica para alternar o status de uma ação, THE PlanDetailPage SHALL chamar `plansStore.updateActionStatus(planId, actionId, newStatus)` onde `newStatus` é `'concluida'` se o status atual for `'pendente'`, e `'pendente'` caso contrário.
11. THE PlanDetailPage SHALL usar `currentPlan.progress` e `currentPlan.actions` em vez dos campos em português.
12. THE HomePage SHALL usar o tipo `PlanSummary[]` para a lista de planos exibida.

---

### Requirement 7: Configuração de Ambiente e Validação Final

**User Story:** Como desenvolvedor, quero que o projeto tenha um `.env.example` atualizado e compile sem erros, para que novos desenvolvedores possam configurar o ambiente facilmente e o deploy seja confiável.

#### Acceptance Criteria

1. THE Frontend SHALL conter o arquivo `frontend/.env.example` com a variável `VITE_API_URL=http://localhost:8000`.
2. WHEN `npm run type-check` é executado, THE Frontend SHALL completar sem erros de tipo TypeScript.
3. WHEN `npm run build` é executado, THE Frontend SHALL compilar sem erros e gerar os artefatos de produção.
4. THE Frontend SHALL não conter nenhuma referência a `delay()`, `setTimeout` com dados mock, arrays hardcoded de planos ou ações, ou dados fake de usuário nos arquivos de service.
5. THE Frontend SHALL não conter referências a nomes de campos em português (`titulo`, `criadoEm`, `acoes`, `progresso`, `prioridade`, `categoria`, `experiencias`, `formacoes`, `habilidades`, `senioridade`, `instituicao`, `areaEstudo`, `dataInicio`, `dataFim`) como nomes de campo em tipos, props ou acessos a objetos.
6. THE Frontend SHALL não conter referências a `refreshToken` em nenhum arquivo de service ou store.
7. WHERE a variável de ambiente `VITE_API_URL` não está definida, THE Frontend SHALL usar `http://localhost:8000` como valor padrão.

---

### Requirement 8: Documentação de Como Rodar o Projeto

**User Story:** Como desenvolvedor, quero ter instruções claras de como rodar o projeto localmente, para que eu possa configurar o ambiente de desenvolvimento rapidamente sem depender de conhecimento prévio.

#### Acceptance Criteria

1. THE Frontend SHALL conter o arquivo `frontend/rodar_projeto.md` atualizado com os pré-requisitos (Node.js 20.19+ ou 22.12+) e os passos para primeira execução.
2. THE `rodar_projeto.md` SHALL incluir o passo de copiar `.env.example` para `.env` e configurar a variável `VITE_API_URL` apontando para o backend.
3. THE `rodar_projeto.md` SHALL documentar o comando `npm install` para instalação de dependências e `npm run dev` para subir o servidor de desenvolvimento.
4. THE `rodar_projeto.md` SHALL informar a URL de acesso local da aplicação (`http://localhost:5173`).
5. THE `rodar_projeto.md` SHALL documentar os comandos adicionais: `npm run build` (build de produção com type-check) e `npm run preview` (preview do build).
6. THE `rodar_projeto.md` SHALL incluir uma seção descrevendo a dependência do backend estar rodando em `http://localhost:8000` para que o login OAuth e as chamadas de API funcionem.
7. WHEN um desenvolvedor segue os passos do `rodar_projeto.md` em um ambiente limpo, THE Frontend SHALL iniciar sem erros e exibir a tela de login.
