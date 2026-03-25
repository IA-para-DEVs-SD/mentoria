# Documento de Requisitos — Mentoria.IA API

## Introdução

Este documento descreve os requisitos funcionais e não-funcionais da API REST backend da plataforma Mentoria.IA, implementada em FastAPI (Python). A API é responsável por autenticação via Google OAuth, gerenciamento de perfil do usuário, geração e gerenciamento de planos de desenvolvimento de carreira via integração com a API Google Gemini, e persistência de dados em banco relacional.

O frontend não faz parte do escopo desta spec. Todos os requisitos aqui descritos referem-se exclusivamente ao comportamento da API.

---

## Glossário

- **API**: A API REST backend da plataforma Mentoria.IA, implementada em FastAPI.
- **Usuario**: Profissional autenticado que utiliza a plataforma para desenvolvimento de carreira.
- **Perfil**: Conjunto de dados do Usuario: trajetória profissional, formação acadêmica, habilidades e objetivo de carreira.
- **Plano**: Roadmap de desenvolvimento de carreira gerado pela API Gemini com base no Perfil do Usuario.
- **Acao**: Item individual do Plano de desenvolvimento, com prioridade, categoria, título, objetivo e contexto.
- **Gap**: Lacuna de competência identificada pela API Gemini com base no Perfil do Usuario.
- **Gemini_Client**: Componente responsável pela comunicação com a API Google Gemini.
- **Auth_Service**: Componente responsável pela autenticação e autorização via Google OAuth 2.0.
- **Profile_Service**: Componente responsável pelo gerenciamento do Perfil do Usuario.
- **Plan_Service**: Componente responsável pelo gerenciamento de Planos e Acoes.
- **Token_JWT**: Token de acesso emitido pela API após autenticação bem-sucedida, usado para autorizar requisições subsequentes.
- **Rejeicao**: Registro de que o Usuario removeu uma Acao, usado para influenciar futuras recomendações do Gemini_Client.
- **Progresso**: Percentual calculado como (Acoes concluídas / total de Acoes) * 100 para um dado Plano.

---

## Requisitos

### Requisito 1: Autenticação com Google OAuth

**User Story:** Como usuário, eu quero autenticar com minha conta Google, para que eu possa acessar a API de forma segura sem gerenciar senhas.

#### Critérios de Aceite

1. THE Auth_Service SHALL expor um endpoint que inicia o fluxo de autorização OAuth 2.0 com o Google.
2. WHEN o Google retornar um authorization code válido, THE Auth_Service SHALL trocar o code por tokens de acesso e obter os dados do Usuario (nome, e-mail, foto).
3. WHEN a autenticação for bem-sucedida, THE Auth_Service SHALL persistir os dados do Usuario (nome, e-mail, URL da foto) e emitir um Token_JWT com tempo de expiração de 24 horas.
4. WHEN a autenticação for bem-sucedida e o Usuario já possuir Perfil completo, THE Auth_Service SHALL incluir no payload da resposta o campo `has_profile: true`.
5. WHEN a autenticação for bem-sucedida e o Usuario não possuir Perfil completo, THE Auth_Service SHALL incluir no payload da resposta o campo `has_profile: false`.
6. IF o authorization code for inválido ou expirado, THEN THE Auth_Service SHALL retornar HTTP 401 com mensagem de erro descritiva.
7. IF o Token_JWT estiver ausente ou inválido em uma requisição autenticada, THEN THE Auth_Service SHALL retornar HTTP 401.
8. IF o Token_JWT estiver expirado, THEN THE Auth_Service SHALL retornar HTTP 401 com indicação de expiração.
9. THE Auth_Service SHALL validar o Token_JWT em todas as rotas protegidas antes de processar a requisição.

---

### Requisito 2: Gerenciamento de Perfil do Usuario

**User Story:** Como usuário, eu quero salvar e atualizar meu perfil profissional, para que a API possa gerar planos de desenvolvimento personalizados.

#### Critérios de Aceite

1. THE Profile_Service SHALL expor endpoints para criar, ler e atualizar o Perfil do Usuario autenticado.
2. THE Profile_Service SHALL persistir os seguintes dados de trajetória profissional: cargo (texto, obrigatório), nível de senioridade (enum: Estagio, Junior, Pleno, Senior, Especialista, Lideranca), empresa (texto, opcional), data de início (obrigatória, não futura) e data de fim (opcional).
3. WHEN a data de fim da trajetória profissional for fornecida, THE Profile_Service SHALL validar que ela é maior ou igual à data de início e não é futura.
4. THE Profile_Service SHALL persistir os seguintes dados de formação acadêmica: instituição (texto, obrigatório), nível de formação (enum: Ensino_Medio, Tecnico, Tecnologo, Bacharelado, Licenciatura, Pos_graduacao, MBA, Mestrado, Doutorado, Pos_doutorado), título da formação (texto, obrigatório), área de estudo (texto, obrigatório), data de início (obrigatória, não futura) e data de fim (opcional, pode ser futura).
5. WHEN a data de fim da formação acadêmica for fornecida, THE Profile_Service SHALL validar que ela é maior ou igual à data de início.
6. THE Profile_Service SHALL persistir habilidades como lista de strings, exigindo ao menos 1 habilidade.
7. THE Profile_Service SHALL persistir o objetivo de carreira como enum com os valores: Crescer_na_carreira_atual, Assumir_cargos_de_lideranca, Mudar_de_area.
8. IF algum campo obrigatório do Perfil estiver ausente ou inválido, THEN THE Profile_Service SHALL retornar HTTP 422 com detalhes dos campos inválidos.
9. WHEN o Perfil for salvo com sucesso, THE Profile_Service SHALL retornar HTTP 200 com o Perfil atualizado.
10. THE Profile_Service SHALL permitir múltiplos registros de trajetória profissional e formação acadêmica por Usuario.
11. WHEN o Usuario autenticado solicitar seu Perfil, THE Profile_Service SHALL retornar os dados completos incluindo todas as trajetórias, formações, habilidades e objetivo.

---

### Requisito 3: Geração de Plano via Gemini (Primeiro Plano e Novos Planos)

**User Story:** Como usuário, eu quero solicitar a geração de um plano de desenvolvimento, para que a API Gemini analise meu perfil e retorne um roadmap personalizado.

#### Critérios de Aceite

1. WHEN o Usuario autenticado solicitar geração de Plano, THE Plan_Service SHALL verificar que o Perfil está completo antes de chamar o Gemini_Client.
2. IF o Perfil estiver incompleto, THEN THE Plan_Service SHALL retornar HTTP 400 com mensagem indicando quais dados estão faltando.
3. WHEN o Perfil estiver completo, THE Plan_Service SHALL enviar ao Gemini_Client os dados de trajetória profissional, formação acadêmica, habilidades, objetivo de carreira e lista de Rejeicoes do Usuario.
4. THE Gemini_Client SHALL construir um prompt estruturado contendo o Perfil do Usuario e as Rejeicoes, solicitando à API Gemini: identificação de Gaps, geração de Acoes priorizadas (ALTA, MEDIA, BAIXA) e um nome para o Plano.
5. WHEN a API Gemini retornar resposta válida, THE Plan_Service SHALL persistir o Plano com: nome gerado automaticamente, data de criação, lista de Gaps e lista de Acoes.
6. THE Plan_Service SHALL gerar o nome do Plano seguindo a estrutura: "Plano [Objetivo] [Contexto] [Data]", com base nos dados retornados pelo Gemini_Client.
7. WHEN o Plano for persistido, THE Plan_Service SHALL retornar HTTP 201 com o Plano completo incluindo Gaps e Acoes.
8. IF a API Gemini retornar erro ou timeout após 30 segundos, THEN THE Plan_Service SHALL retornar HTTP 502 com mensagem de erro e não persistir dados parciais.
9. THE Plan_Service SHALL incluir as Rejeicoes do Usuario no contexto enviado ao Gemini_Client para evitar repetição de conteúdos similares aos rejeitados.
10. WHEN um novo Plano for gerado, THE Plan_Service SHALL usar o Perfil mais recente do Usuario, incluindo quaisquer atualizações feitas antes da solicitação.

---

### Requisito 4: Visualização de Detalhes do Plano

**User Story:** Como usuário, eu quero consultar os detalhes de um plano específico, para que eu possa acompanhar meus Gaps, Acoes e progresso.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint GET `/plans/{plan_id}` que retorna o Plano completo com Gaps, Acoes e Progresso.
2. WHEN o endpoint for chamado, THE Plan_Service SHALL retornar: nome do Plano, data de criação, Progresso calculado, lista de Gaps ordenada por relevância e lista de Acoes ordenada por prioridade e sequência lógica.
3. THE Plan_Service SHALL calcular o Progresso como `(quantidade de Acoes com status concluido / total de Acoes) * 100`, arredondado para inteiro.
4. IF o `plan_id` não existir ou não pertencer ao Usuario autenticado, THEN THE Plan_Service SHALL retornar HTTP 404.
5. THE Plan_Service SHALL incluir em cada Acao os campos: id, prioridade (ALTA, MEDIA, BAIXA), categoria, título, objetivo, contexto e status (pendente, concluida).

---

### Requisito 5: Listagem de Planos na Home

**User Story:** Como usuário, eu quero listar todos os meus planos, para que eu possa gerenciar e acompanhar meu histórico de desenvolvimento.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint GET `/plans` que retorna todos os Planos do Usuario autenticado.
2. WHEN o endpoint for chamado, THE Plan_Service SHALL retornar para cada Plano: id, nome, data de criação e Progresso calculado.
3. WHEN o Usuario não possuir Planos, THE Plan_Service SHALL retornar HTTP 200 com lista vazia.
4. THE Plan_Service SHALL ordenar a lista de Planos por data de criação decrescente (mais recente primeiro).

---

### Requisito 6: Exclusão de Plano

**User Story:** Como usuário, eu quero excluir um plano, para que eu possa manter minha lista organizada.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint DELETE `/plans/{plan_id}` para exclusão de Plano.
2. WHEN o Usuario confirmar a exclusão, THE Plan_Service SHALL remover o Plano e todas as Acoes e Gaps associados.
3. WHEN a exclusão for bem-sucedida, THE Plan_Service SHALL retornar HTTP 204.
4. IF o `plan_id` não existir ou não pertencer ao Usuario autenticado, THEN THE Plan_Service SHALL retornar HTTP 404.

---

### Requisito 7: Marcar Ação como Concluída e Atualizar Progresso

**User Story:** Como usuário, eu quero marcar ações como concluídas, para que o progresso do meu plano seja atualizado automaticamente.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint PATCH `/plans/{plan_id}/actions/{action_id}` que aceita o campo `status` com valores `pendente` ou `concluida`.
2. WHEN o status de uma Acao for atualizado para `concluida`, THE Plan_Service SHALL recalcular e persistir o Progresso do Plano.
3. WHEN o status de uma Acao for atualizado para `pendente`, THE Plan_Service SHALL recalcular e persistir o Progresso do Plano.
4. WHEN a atualização for bem-sucedida, THE Plan_Service SHALL retornar HTTP 200 com a Acao atualizada e o novo Progresso do Plano.
5. IF o `action_id` não pertencer ao `plan_id` informado ou não pertencer ao Usuario autenticado, THEN THE Plan_Service SHALL retornar HTTP 404.

---

### Requisito 8: Exclusão de Ação e Registro de Rejeição

**User Story:** Como usuário, eu quero excluir ações do meu plano e registrar minha rejeição, para que futuras recomendações evitem conteúdos similares.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint DELETE `/plans/{plan_id}/actions/{action_id}` para exclusão de Acao.
2. WHEN a Acao for excluída, THE Plan_Service SHALL criar um registro de Rejeicao contendo: id do Usuario, categoria da Acao, título da Acao e data da rejeição.
3. WHEN a Acao for excluída, THE Plan_Service SHALL recalcular e persistir o Progresso do Plano com base nas Acoes restantes.
4. WHEN a exclusão for bem-sucedida, THE Plan_Service SHALL retornar HTTP 200 com o novo Progresso do Plano.
5. IF o Plano possuir apenas 1 Acao, THEN THE Plan_Service SHALL retornar HTTP 409 e não realizar a exclusão.
6. IF o `action_id` não pertencer ao `plan_id` informado ou não pertencer ao Usuario autenticado, THEN THE Plan_Service SHALL retornar HTTP 404.

---

### Requisito 9: Geração de Mais Ações para um Plano Existente

**User Story:** Como usuário, eu quero solicitar mais ações para um plano existente, para que eu possa continuar meu desenvolvimento após concluir as ações iniciais.

#### Critérios de Aceite

1. THE Plan_Service SHALL expor um endpoint POST `/plans/{plan_id}/actions/generate` para geração de novas Acoes em um Plano existente.
2. WHEN o endpoint for chamado, THE Plan_Service SHALL enviar ao Gemini_Client: o Perfil atual do Usuario, as Acoes existentes no Plano, o Progresso atual e as Rejeicoes do Usuario.
3. THE Gemini_Client SHALL solicitar à API Gemini novas Acoes que não repitam conteúdos já existentes no Plano e que respeitem as Rejeicoes do Usuario.
4. WHEN o Gemini_Client retornar novas Acoes, THE Plan_Service SHALL adicioná-las ao Plano existente e recalcular o Progresso.
5. WHEN a geração for bem-sucedida, THE Plan_Service SHALL retornar HTTP 200 com as novas Acoes adicionadas e o Progresso atualizado.
6. IF a API Gemini retornar erro ou timeout após 30 segundos, THEN THE Plan_Service SHALL retornar HTTP 502 e não modificar o Plano existente.
7. IF o `plan_id` não existir ou não pertencer ao Usuario autenticado, THEN THE Plan_Service SHALL retornar HTTP 404.

---

### Requisito 10: Segurança e Validação de Entradas

**User Story:** Como operador da plataforma, eu quero que a API valide e sanitize todas as entradas, para que dados maliciosos não comprometam o sistema.

#### Critérios de Aceite

1. THE API SHALL validar o schema de todas as requisições usando Pydantic, retornando HTTP 422 com detalhes para entradas inválidas.
2. THE API SHALL sanitizar campos de texto livre removendo caracteres de controle e limitando o tamanho máximo a 500 caracteres por campo.
3. THE Auth_Service SHALL armazenar apenas a URL da foto do perfil Google, sem armazenar tokens de acesso do Google em banco de dados.
4. THE API SHALL aplicar rate limiting de 60 requisições por minuto por Usuario autenticado nas rotas de geração via Gemini_Client.
5. IF uma requisição exceder o rate limit, THEN THE API SHALL retornar HTTP 429.

---

### Requisito 11: Desempenho da API

**User Story:** Como usuário, eu quero que a API responda rapidamente, para que a experiência de uso seja fluida.

#### Critérios de Aceite

1. THE API SHALL responder a endpoints de leitura (GET) em menos de 500ms para o percentil 95 das requisições, excluindo chamadas ao Gemini_Client.
2. THE Plan_Service SHALL aguardar resposta do Gemini_Client por no máximo 30 segundos antes de retornar erro de timeout.
3. IF a API Gemini não responder dentro de 30 segundos, THEN THE Plan_Service SHALL retornar HTTP 502 com mensagem de timeout.

---

## Requisitos Não-Funcionais

### RNF 1: Stack Técnica

- THE API SHALL ser implementada em Python com FastAPI.
- THE API SHALL usar SQLAlchemy como ORM com suporte a PostgreSQL e SQLite.
- THE API SHALL usar Alembic para gerenciamento de migrações de banco de dados.
- THE Auth_Service SHALL usar a biblioteca `authlib` ou `google-auth` para o fluxo OAuth 2.0.
- THE Gemini_Client SHALL usar o SDK oficial `google-generativeai` para comunicação com a API Gemini.

### RNF 2: Estrutura e Organização

- THE API SHALL organizar o código em módulos separados por domínio: `auth`, `profile`, `plans`, `gemini`.
- THE API SHALL expor documentação automática via Swagger UI em `/docs` e ReDoc em `/redoc`.
- THE API SHALL usar variáveis de ambiente para todas as configurações sensíveis (chaves de API, secrets, URLs de banco).

### RNF 3: Confiabilidade

- IF ocorrer erro interno não tratado, THEN THE API SHALL retornar HTTP 500 com mensagem genérica sem expor detalhes internos.
- THE API SHALL registrar logs estruturados para todas as requisições e erros, incluindo timestamp, método HTTP, rota, status code e tempo de resposta.
