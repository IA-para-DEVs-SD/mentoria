# Documento de Requisitos do Produto (PRD)

## 1. Visão Geral do Produto

### 1.1 Objetivo do Produto

Mentoria.IA é uma plataforma de mentoria de carreira impulsionada por inteligência artificial, projetada para ajudar profissionais a alcançarem seus objetivos de carreira através de análise inteligente de perfil, geração de roadmaps personalizados e acompanhamento contínuo de desenvolvimento. A aplicação utiliza a Inteligência Artificial para processar informações do usuário e gerar recomendações precisas de desenvolvimento profissional.

### 1.2 Fluxo de Usuário

#### Primeiro Acesso
1. Usuário faz login na plataforma
2. Usuário preenche seus dados profissionais em 5 etapas: experiência profissional, formação acadêmica, habilidades e objetivo de carreira, Revisão
3. Sistema envia dados para IA
4. Sistema gera o primeiro plano de desenvolvimento

#### Acessos Posteriores
1. Usuário acessa a página inicial (Home) após login
2. Página inicial exibe lista de todos os planos gerados
3. Cada plano na lista exibe: título, data de geração e progresso
4. Para cada plano, usuário pode: "Ver Detalhes" (abre página do plano) ou "Excluir"

#### Gerar Novo Plano
1. Na página inicial, usuário clica em "Gerar Novo Plano"
2. Sistema abre fluxo de preenchimento de dados (como no primeiro acesso)
3. **Diferença**: Dados vêm pré-preenchidos com informações anteriores
4. Usuário pode atualizar informações ou alterar objetivo de carreira
5. Usuário confirma geração do novo plano
6. Sistema envia dados atualizados para API Gemini
7. Sistema gera novo plano e adiciona à lista

### 1.3 Escopo do Produto

**Incluído no Escopo:**
- Sistema de autenticação com Google - Integração real com OAuth do Google
- Logout com remoção de sessão local e redirecionamento para login
- Onboarding em 5 etapas para coleta de dados do usuário (incluindo etapa de revisão)
- Análise de perfil via IA para identificação de gaps de competência
- Geração de roadmap personalizado com ações de desenvolvimento
- Página inicial (Home) com lista de planos gerados
- Visualização de detalhes de cada plano
- Exclusão de planos
- Persistência de dados - Backend com banco de dados
- Geração de múltiplos planos de desenvolvimento via IA
- Dados pré-preenchidos ao gerar novos planos

**Fora do Escopo:**
- Pagamentos e assinaturas
- Integração com LinkedIn ou outras redes sociais

### 1.4 Benefícios Esperados

- Identificação automática de gaps de competência baseados em perfil profissional
- Roadmap personalizado com ações concretas de desenvolvimento
- Gerenciamento de múltiplos planos de desenvolvimento
- Reutilização de dados de perfil em novos planos

---

## 2. Glossário

- **Mentoria.IA**: Sistema principal - plataforma web de mentoria de carreira com IA
- **Usuário**: Profissional que utiliza a plataforma para desenvolvimento de carreira
- **Roadmap**: Plano de desenvolvimento personalizado com ações e metas (sinônimo de Plano)
- **Plano**: Roadmap de desenvolvimento de carreira gerado via IA
- **IA**: Inteligência artificial utilizada para análise de perfil
- **Onboarding**: Processo de coleta de informações do usuário em 5 etapas
- **Home**: Página inicial após login que lista todos os planos gerados
- **Dados de Perfil**: Informações do usuário: experiência, formação, habilidades e objetivo de carreira

---

## 3. Personas

### Persona 1: Profissional em Transição de Carreira

| Atributo | Descrição |
|----------|-----------|
| **Nome** | Carlos Silva |
| **Idade** | 32 anos |
| **Profissão** | Analista de Sistemas |
| **Objetivos** | Migrar para posição de Tech Lead |
| **Dor** | Dificuldade em identificar quais habilidades desenvolver para alcançar o próximo nível |
| **Comportamento** | Usa LinkedIn diariamente, busca conteúdos sobre liderança e gestão de projetos |

### Persona 2: Profissional em Crescimento

| Atributo | Descrição |
|----------|-----------|
| **Nome** | Mariana Santos |
| **Idade** | 28 anos |
| **Profissão** | Desenvolvedora Frontend Júnior |
| **Objetivos** | Atingir nível Pleno |
| **Dor** | Falta de direcionamento claro sobre quais competências técnicas e comportamentais desenvolver |
| **Comportamento** | Participa de comunidades de desenvolvedores, assiste meetups e conferências |

---

## 4. User Stories

### US 1: Autenticação com Google

**Como** usuário,  
**Eu quero** fazer login com minha conta Google,  
**Para que** eu possa acessar a plataforma de forma rápida e segura.

**Critérios de Aceite:**
1. A Mentoria.IA DEVE exibir botão de login com Google na página inicial.
2. QUANDO o usuário clicar no botão de login, A Mentoria.IA DEVERÁ verificar se o usuário possui dados de perfil salvos.
3. SE existirem dados de perfil, A Mentoria.IA DEVE redirecionar para Home.
4. Senão, A Mentoria.IA DEVERÁ redirecionar para onboarding.
5. A Mentoria.IA DEVERÁ armazenar dados do usuário após autenticação.

_Dados a ser capturado do Login:_
- **Nome**: campo de texto, obrigatório, preenchido automaticamente a partir das informações do login. Não editável pelo usuário.
- **E-mail**: campo de texto, obrigatório, preenchido automaticamente a partir das informações do login. Não editável pelo usuário.
- **Foto**: campo de imagem (URL ou binário), obrigatório, preenchido automaticamente a partir das informações do login. Não editável pelo usuário.


### US 2: Preenchimento de Perfil (Primeiro Acesso)

**Como** usuário,  
**Eu quero** preencher meu perfil profissional em 5 etapas no primeiro acesso,  
**Para que** o sistema tenha informações suficientes para gerar meu primeiro plano de desenvolvimento.

**Critérios de Aceite:**
1. A Mentoria.IA DEVE apresentar 5 etapas de onboarding: Trajetória Profissional, Formação Acadêmica, Habilidades, Objetivo de Carreira e Revisão. Descritos abaixo dos requisitos.
2. QUANDO o usuário concluir todas as etapas e confirmar na etapa de Revisão, A Mentoria.IA DEVERÁ salvar todos os dados do perfil de uma vez.
3. A Mentoria.IA DEVERÁ permitir a navegação entre etapas já concluídas (voltar e avançar)
4. QUANDO todas as etapas forem concluídas, A Mentoria.IA DEVERÁ redirecionar para geração do primeiro plano
5. SE o usuário tentar pular etapas obrigatórias, A Mentoria.IA DEVE exibir mensagem de erro

#### Etapas do Onboarding

**Trajetória Profissional:**
- Permitir múltiplos registros de experiência.

_Campos do formulário:_
- Cargo: Campo do tipo texto livre, obrigatório, não permite apenas espaços em branco, permite caracteres alfanuméricos e acentuação.
- Nível de Senioridade: Campo do tipo seleção, obrigatório. Opções disponíveis: Estágio, Júnior, Pleno, Sênior, Especialista, Liderança (Tech Lead / Manager).
- Empresa: Campo do tipo texto livre, opcional, permite caracteres alfanuméricos e acentuação.
- Data de Início: Campo do tipo data, obrigatório, formato exibido: MM/AAAA. Deve permitir seleção via calendário e/ou digitação. Não pode ser uma data futura. Deve ser menor ou igual à Data de Fim (quando preenchida).
- Data de Fim: Campo do tipo data, opcional. Placeholder: "Vazio = atual". Quando não preenchido, o sistema considera o vínculo como atual/em andamento. Se preenchido: deve ser maior ou igual à Data de Início. Não pode ser uma data futura.
- É obrigatório pelo menos 1 registro de experiência profissional.

_Mensagens sugeridas:_
- Selecione o nível de senioridade.

**Formação Acadêmica:**
- Permitir múltiplos registros de formação.

_Campos do formulário:_
- Instituição: Campo do tipo texto, obrigatório, não permite apenas espaços em branco. Permite caracteres alfanuméricos e acentuação.
- Nível de Formação: Campo do tipo seleção, obrigatório. Opções disponíveis (fixas): Ensino Médio, Técnico, Tecnólogo, Bacharelado, Licenciatura, Pós-graduação, MBA, Mestrado, Doutorado, Pós-doutorado, 
- Título da formação: Campo do tipo texto, obrigatório, não permite apenas espaços em branco. 
- Área de Estudo: Campo do tipo texto, obrigatório. Não permite apenas espaços em branco.
- Data de Início: Campo do tipo data, obrigatório. Formato exibido: DD/MM/AAAA. Não pode ser uma data futura. Deve ser menor ou igual à Data de Fim (quando preenchida).
- Data de Fim: Campo do tipo data, opcional. Quando não preenchido, o sistema deve considerar como curso em andamento. Se preenchido: Deve ser maior ou igual à Data de Início. Pode permitir datas futuras (ex: previsão de conclusão).
- É obrigatório pelo menos 1 registro de formação acadêmica.


**Nota de design:** A Formação Acadêmica usa formato DD/MM/AAAA (data completa) enquanto a Trajetória Profissional usa MM/AAAA (mês/ano), pois o dia exato de início/fim de um emprego é irrelevante. A Data de Fim da formação permite datas futuras para acomodar previsão de conclusão, diferente da trajetória profissional onde vínculos futuros não fazem sentido.


_Mensagens Sugeridas:_
- Informe a instituição.
- Selecione o nível de formação.
- Informe o título da formação.
- Informe a área de estudo.
- Data de início inválida.
- Data de fim deve ser posterior à data de início.

**Habilidades:**
- Permitir múltiplos registros de habilidades.
- Deve existir pelo menos 1 habilidade cadastrada para permitir avanço, sem limite máximo.
- Ao adicionar uma habilidade, o valor é convertido em uma tag (chip) exibida abaixo e o campo de texto é limpo automaticamente.
- Cada item adiionado deve ter opção de remoção (ex: ícone “x”), ser visualmente destacado como chip/tag.
- **(Desejável)** Não permitir duplicidade (Normalização): Remover espaços extras, padronizar capitalização (ex: primeira letra maiúscula ou padrão técnico), evitar duplicidade (case insensitive).
- **(Desejável)** Sugestões de Habilidades: Lista pré-definida exibida como sugestões de acordo com a área de estudo e área de formação. Ao clicar em uma sugestão a habilidade é adicionada como tag. 
- **(Desejável)** Autocomplete inteligente.

_Campos do formulário:_
- Campo de Entrada de Habilidade: Campo do tipo texto. obrigatório. Permite caracteres alfanuméricos e acentuação.

_Mensagens Sugeridas:_
- Adicione pelo menos uma habilidade.
- Habilidade já adicionada.

**Objetivo de Carreira**
- O usuário deve selecionar somente 1 objetivo para avançar.
- Cada opção deve ter:
    - Estado padrão (não selecionado); 
    - Estado selecionado (destaque visual claro);
    - Estado hover/foco (acessibilidade).

_Campos do formulário:_
- Componente do tipo lista de seleção. 
- Exibe opções pré-definidas de objetivos profissionais.
- Opções disponíveis: Crescer na carreira atual, Assumir cargos de liderança, Mudar de área.

_Mensagens Sugeridas:_
- Selecione um objetivo para continuar.

**Revisão:**
- Etapa final do onboarding que exibe um resumo de todos os dados preenchidos nas etapas anteriores.
- O usuário pode conferir as informações antes de confirmar a geração do plano.
- Deve exibir: lista de experiências profissionais, formações acadêmicas, habilidades (como chips) e objetivo de carreira selecionado.
- O usuário pode voltar para qualquer etapa anterior para corrigir dados.
- O botão de confirmação ("Gerar Mentoria IA") só é habilitado se todas as etapas anteriores estiverem válidas.

### US 3: Receber Primeiro Plano Personalizado

**Como** usuário,  
**Eu quero** receber um plano personalizado gerado por IA após o primeiro preenchimento,  
**Para que** eu tenha um plano claro de desenvolvimento profissional.

**Critérios de Aceite:**
1. QUANDO o onboarding for concluído, a Mentoria.IA DEVERÁ enviar dados do perfil para API Gemini.
2. A API Gemini DEVERÁ analisar o perfil e gerar plano de desenvolvimento.
3. Deve haver pelo menos 1 Gap de Competência identificado, ou seja, áreas onde o usuário precisa evoluir. Não há limite máximo de gaps. Os Gaps baseam-se em:
    - Objetivo do usuário
    - Trajetória profissional
    - Habilidades 
    - Formação acadêmica
4. Gerar um plano de ação personalizado e relacionadas aos gaps identificados:
    - Identificar lacunas (gap analysis)
    - Priorizar competências críticas
    - Gerar trilha progressiva:
        - Fundamentos
        - Aplicação
        - Avançado / Estratégico
5. O plano gerado deve respeitar os seguintes limites:
   - Mínimo de 3 ações por plano. Não há limite máximo.
   - Mínimo de 1 gap de competência. Não há limite máximo.
   - Título de cada ação: máximo de 100 caracteres
   - Objetivo de cada ação: máximo de 300 caracteres
   - Contexto de cada ação: máximo de 500 caracteres
   - O conteúdo deve ser personalizado com base no perfil do usuário (não genérico)
6. A Mentoria.IA DEVERÁ salvar o plano.
7. A Mentoria.IA DEVERÁ redirecionar para a página de detalhes do plano ![US 4: Ver Detalhes de um Plano](#us-4-ver-detalhes-de-um-plano)
8. CASO a API retorne erro, o Mentoria.IA DEVE exibir mensagem de erro e permitir nova tentativa.
9. Estados possíveis: Carregando (loading); Plano gerado; Erro na geração; Plano vazio (fallback).
10. Cada plano gerado deve conter um nome gerado automaticamente pela IA, contextualizado com base no perfil e objetivo do usuário.

_Mensagens sugeridas:_
- Estamos gerando seu plano personalizado...
- Não foi possível gerar o plano. Tente novamente.

### US 4: Ver Detalhes de um Plano

**Como** usuário,  
**Eu quero** visualizar os detalhes de um plano específico,  
**Para que** eu possa acompanhar as ações de desenvolvimento daquele plano.

**Critérios de Aceite:**

1. QUANDO o plano for gerado após o onboarding ou QUANDO o usuário clicar em "Ver Detalhes", A Mentoria.IA DEVE exibir a página com detalhes do plano.
2. DEVERÁ exibir um cabeçalho contendo:
    - Título do plano gerado automaticamente
    - Subtítulo: nome do usuário 
    - Ícone/avatar do usuário
3. A Mentoria.IA DEVERÁ exibir o Progresso do Roadmap
    - Componente: barra de progresso (%)
    - Valor inicial: 0%
    - Deve refletir: Quantidade de ações concluídas ÷ total de ações
    - Regras:
        - Atualização em tempo real ao concluir etapas
        - Persistência do progresso
        - Fórmula: _progresso = (ações concluídas / total de ações) * 100_
4. A Mentoria.IA DEVERÁ listar todos os Gaps de Competência Identificados.
5. A lista de Gaps deve ser ordenada por relevância (maior impacto primeiro).
    - A importância do impacto deve ser gerada pela IA
6. A Mentoria.IA DEVERÁ listar de ações organizadas em formato de timeline/etapas.
7. Cada item deve conter:
    - Prioridade: ALTA, MÉDIA, BAIXA
    - Categoria (ex: Liderança, Desenvolvimento Geral)
    - Título: Nome da ação (ex: "Desenvolvimento de Inteligência Emocional...")
    - Objetivo: Descrição clara do que será desenvolvido
    - Contexto: Explicação personalizada baseada no perfil do usuário
8. A timeline das ações deve ser ordenada por prioridade e sequência lógica de aprendizado, oriundas da IA, prevalescendo a ordem de prioridade em caso de conflitos.
9. A Mentoria.IA DEVE permitir ao usuário marcar ações como concluídas.
10. QUANDO uma ação estiver marcada como concluída, A Mentoria.IA DEVERÁ atualizar o progresso do plano.
11. A Mentoria.IA DEVE permitir ao usuário a exclusão de item do Plano de Ação (Timeline), exceto se for o único item do plano:    
    - Solicitar confirmação do usuário
    - Ao excluir, deve recalcular automaticamente o progresso e atualizar UI em tempo real    
    - O sistema deve registrar que o usuário rejeitou aquela ação para:
        - Evitar gerar conteúdos similares, ou seja, que contenham o mesmo sentido semânticamente
        - Ajustar o modelo de recomendação
    - Gaps não devem ser removidos
12. A Mentoria.IA DEVE permitir ao usuário gerar mais ações ao Plano de Ação (Timeline).
    - Criar novas ações com base no progresso atual
    - Itens excluídos considerar como restrição
    - Evitar repetição de conteúdos
    - Deve recalcular o progresso
    - Atualizar UI em tempo real
    - A geração de novas ações deve retornar pelo menos 1 ação. A quantidade é determinada pela IA com base nos gaps e no progresso atual do plano. Não há limite máximo.
13. A página deverá exibir botão para retornar à Home
    
_Mesagens Sugeridas:_
- Confirmação da Exclusão: "Essa ação removerá esta atividade do seu plano de desenvolvimento.
- Exclusão bem-sucedida exibir feedback: "Item removido do plano"
- Erro na exclusão exibir mensagem: "Não foi possível remover o item. Tente novamente."
- Último item exibir: "Seu plano precisa ter pelo menos uma ação"


### US 5: Visualizar Lista de Planos na Home

**Como** usuário,  
**Eu quero** visualizar todos os meus planos gerados na página inicial,  
**Para que** eu possa gerenciar e acompanhar meus planos de desenvolvimento.

**Critérios de Aceite:**
1. A Mentoria.IA DEVERÁ exibir lista de todos os planos salvos.
2. A Lista DEVERÁ exibir para cada plano: 
    - Título do plano
    - Data da geração
    - Percentual de progresso
3. A Mentoria.IA DEVE exibir o botão "Gerar Novo Plano" na Home.
4. A Mentoria.IA DEVERÁ exibir a opção "Ver Detalhes" para cada plano.
5. A Mentoria.IA DEVERÁ exibir a opção "Excluir" para cada plano ![US 6: Excluir um Plano](#us-6-excluir-um-plano).
6. CASO não haja planos salvos (inclusive se todos foram excluídos), A Mentoria.IA DEVERÁ exibir empty state com mensagem "Você ainda não tem planos de desenvolvimento" e botão "Gerar Primeiro Plano". O usuário permanece na Home.

**Nota de design:** A listagem de planos na Home carrega todos os planos do usuário sem paginação. Para o MVP, não há limite de planos exibidos. Paginação poderá ser implementada em versão futura caso o volume justifique.

### US 6: Excluir um Plano

**Como** usuário,  
**Eu quero** excluir um plano que não é mais necessário,  
**Para que** eu possa manter minha lista de planos organizada.

**Critérios de Aceite:**
1. QUANDO o usuário clicar em "Excluir", A Mentoria.IA DEVERÁ exibir modal de confirmação
2. SE o usuário confirmar, A Mentoria.IA DEVERÁ remover o plano.
3. A Mentoria.IA VAI atualizar a lista de planos na Home.
4. SE o último plano for excluído, A Mentoria.IA DEVERÁ exibir o empty state com mensagem orientativa e botão "Gerar Primeiro Plano". O usuário permanece na Home.

_Mensagens Sugeridas:_
- Ao solicitar confirmação: "Ao excluir este plano, você perderá seu progresso e histórico de desenvolvimento. Essa ação não pode ser desfeita."
- Sucesso ao excluir: "Plano excluído. Você pode criar um novo plano a qualquer momento."
- Erro na exclusão: "Não foi possível excluir o plano. Tente novamente."

### US 7: Gerar Novo Plano (Acessos Posteriores)

**Como** usuário,  
**Eu quero** gerar um novo plano de desenvolvimento a partir da Home,  
**Para que** eu possa explorar diferentes abordagens de carreira.

**Critérios de Aceite:**
1. QUANDO o usuário clicar em "Gerar Novo Plano", A Mentoria.IA DEVERÁ abrir fluxo de onboargins novamente.
2. A Mentoria.IA DEVE pré-preencher os campos com dados do perfil salvos, que foram preenchidos no onboarding.
3. A Mentoria.IA DEVE permitir ao usuário modificar qualquer informação.
4. QUANDO o usuário confirmar geração, a API Gemini DEVE gerar novo plano de desenvolvimento, conforme ![US 3: Receber Primeiro Plano Personalizado](#us-3-receber-primeiro-plano-personalizado).
5. A Mentoria.IA DEVERÁ salvar o novo plano.
6. A Mentoria.IA DEVERÁ redirecionar para a página de detalhes do plano.

---

6. A Mentoria.IA DEVERÁ redirecionar para a página de detalhes do plano.

### US 8: Logout

**Como** usuário,  
**Eu quero** sair da plataforma,  
**Para que** minha sessão seja encerrada e meus dados protegidos.

**Critérios de Aceite:**
1. A Mentoria.IA DEVE exibir opção de logout acessível em todas as páginas autenticadas.
2. QUANDO o usuário clicar em "Sair", A Mentoria.IA DEVERÁ remover o token JWT armazenado localmente (localStorage).
3. A Mentoria.IA DEVERÁ redirecionar o usuário para a página de login.
4. Após logout, qualquer tentativa de acessar páginas autenticadas DEVE redirecionar para a página de login.
5. O token JWT possui validade de 24 horas. QUANDO o token expirar, A Mentoria.IA DEVERÁ retornar erro 401 e redirecionar para a página de login.
6. Não há refresh token. Após expiração, o usuário deve realizar novo login com Google.

_Mensagens sugeridas:_
- Token expirado: "Sua sessão expirou. Faça login novamente."

> **Nota de implementação:** O logout é client-side (remoção do token do localStorage). Não há endpoint de logout no backend, pois o JWT é stateless — a invalidação ocorre pela remoção local e pela expiração natural do token.

### US 9: Fallback de Indisponibilidade da IA

**Como** usuário,  
**Eu quero** ser informado quando a IA estiver indisponível após múltiplas tentativas,  
**Para que** eu não fique preso em um loop de erros e saiba que devo tentar mais tarde.

**Critérios de Aceite:**
1. A Mentoria.IA DEVERÁ implementar retry automático de até 3 tentativas na chamada à API Gemini (geração de plano e geração de mais ações).
2. A Mentoria.IA DEVERÁ aguardar intervalo progressivo entre tentativas (1s, 2s, 4s).
3. Após 3 falhas consecutivas, o backend DEVERÁ retornar erro 503 com mensagem clara.
4. As falhas DEVEM ser registradas em log para monitoramento.
5. Na tela de geração de plano: após 3 tentativas falhas do botão "Tentar novamente", A Mentoria.IA DEVERÁ substituir o botão por mensagem: "O serviço de IA está temporariamente indisponível. Tente novamente mais tarde."
6. Na tela de detalhes do plano: ao gerar mais ações, após falha, A Mentoria.IA DEVERÁ exibir toast com mensagem: "Não foi possível gerar novas ações. Tente novamente mais tarde."
7. Após exibir mensagem de indisponibilidade, A Mentoria.IA DEVE oferecer botão para voltar à Home.

_Mensagens sugeridas:_
- Indisponibilidade: "O serviço de IA está temporariamente indisponível. Tente novamente mais tarde."
- Falha ao gerar ações: "Não foi possível gerar novas ações. Tente novamente mais tarde."

---

## 5. Requisitos Não-Funcionais a página inicial em menos de 3 segundos.
- A Mentoria.IA DEVERÁ processar respostas da API Gemini em menos de 10 segundos.
- A Mentoria.IA DEVERÁ responder a interações do usuário em menos de 100ms.

### RNF 2: Segurança

- São considerados dados sensíveis: token JWT, credenciais OAuth (client_secret) e chave da API Gemini. Esses dados DEVEM ser armazenados exclusivamente em variáveis de ambiente (.env), fora do repositório.
- Dados do perfil do usuário (nome, e-mail, experiências, formações, habilidades) são protegidos por autenticação (JWT) e HTTPS em trânsito. Não há criptografia em repouso no MVP.
- A Mentoria.IA DEVERÁ validar dados de entrada em todos os formulários.
- A Mentoria.IA DEVERÁ implementar proteção contra XSS em entradas de usuário.

### RNF 3: Usabilidade e Acessibilidade

- A Mentoria.IA DEVERÁ ser intuitivo para novos usuários sem treinamento.
- A Mentoria.IA DEVERÁ fornecer feedback visual de todas as operações.
- A Mentoria.IA DEVERÁ funcionar em dispositivos com tela a partir de 320px de largura.
- A Mentoria.IA DEVERÁ atender ao nível A das diretrizes WCAG 2.1 como meta mínima, incluindo: labels acessíveis em controles interativos (aria-label), navegação por teclado e contraste mínimo de texto.

### RNF 4: Compatibilidade

- A Mentoria.IA DEVERÁ funcionar nos navegadores: Chrome, Firefox, Safari, Edge (versões atuais).
- A Mentoria.IA DEVERÁ ser responsivo para dispositivos móveis e desktop.
- A Mentoria.IA DEVERÁ suportar integração com API REST do Google Gemini.

### RNF 5: Confiabilidade

- SE ocorrer falha na API Gemini, A Mentoria.IA DEVERÁ exibir mensagem de erro clara.

---

## 6. Casos de Uso

### UC 1: Login e Autenticação

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário (Profissional em transição/crescimento) |
| **Pré-condições** | Usuário possui conta Google; navegador com acesso à internet |
| **Fluxo Principal** | 1. Usuário acessa a página inicial do Mentoria.IA <br> 2. Usuário clica no botão "Entrar com Google" <br> 3. Sistema processa autenticação <br> 4. Sistema verifica se dados de perfil existem <br> 5. Se existem: redirecionar para Home <br> 6. Se não existem: redirecionar para onboarding <br> 7. Dados do usuário salvos |
| **Pós-condições** | Usuário autenticado e redirecionado para Home ou onboarding |
| **Fluxo Alternativo** | Usuário já possui sessão ativa: carregamento automático |
| **Exceções** | Falha na autenticação: exibir mensagem de erro e opção de retry |

### UC 2: Primeiro Acesso - Onboarding e Geração do Primeiro Plano

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário autenticado sem dados de perfil |
| **Pré-condições** | Usuário está autenticado e redirecionado para onboarding |
| **Fluxo Principal** | 1. Usuário preenche dados pessoais <br> 2. Usuário adiciona trajetórias profissionais <br> 3. Usuário informa formação acadêmica <br> 4. Usuário lista habilidades atuais <br> 5. Usuário define objetivo de carreira <br> 6. Sistema envia dados para API Gemini <br> 7. Sistema gera primeiro plano de desenvolvimento <br> 8. Sistema salva plano <br> 9. Sistema redireciona para detalhes do plano |
| **Pós-condições** | Primeiro plano gerado e salvo; usuário vê PLano |
| **Fluxo Alternativo** | Usuário retorna em etapa posterior: carregar dados salvos |
| **Exceções** | API Gemini indisponível: exibir erro e permitir retry; dados inválidos: exibir mensagem específica |

### UC 3: Acessos Posteriores - Visualização da Home

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário autenticado com dados de perfil |
| **Pré-condições** | Usuário está autenticado e possui dados de perfil salvos |
| **Fluxo Principal** | 1. Usuário acessa a aplicação <br> 2. Sistema verifica dados de perfil existentes <br> 3. Sistema redireciona para Home <br> 4. Home lista todos os planos salvos <br> 5. Cada plano exibe título, data e progresso |
| **Pós-condições** | Usuário visualiza lista de planos na Home |
| **Fluxo Alternativo** | Nenhum plano salvo (inclusive se todos foram excluídos): exibir empty state com mensagem "Você ainda não tem planos de desenvolvimento" e botão "Gerar Primeiro Plano". O usuário permanece na Home — não é redirecionado para o onboarding. |
| **Exceções** | Falha na comunicação: exibir erro e oferecer recuperação |

### UC 4: Visualização de Detalhes do Plano

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário com planos salvos |
| **Pré-condições** | Usuário está na Home com lista de planos |
| **Fluxo Principal** | 1. Usuário clica em "Ver Detalhes" de um plano <br> 2. Sistema carrega detalhes do plano <br> 3. Sistema exibe página com todas as ações <br> 4. Usuário visualiza ações e seus status <br> 5. Usuário pode marcar ações como concluídas <br> 6. Sistema atualiza progresso |
| **Pós-condições** | Detalhes do plano visualizados; progresso atualizado |
| **Fluxo Alternativo** | Usuário retorna para Home: clique no botão de voltar |
| **Exceções** | Plano não encontrado: exibir erro e retornar para Home |

### UC 5: Exclusão de Plano

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário com planos salvos |
| **Pré-condições** | Usuário está na Home com lista de planos |
| **Fluxo Principal** | 1. Usuário clica em "Excluir" de um plano <br> 2. Sistema exibe modal de confirmação <br> 3. Usuário confirma exclusão <br> 4. Sistema remove plano <br> 5. Sistema atualiza lista de planos |
| **Pós-condições** | Plano excluído; lista atualizada |
| **Fluxo Alternativo** | Usuário cancela exclusão: modal fechado sem alteração |
| **Exceções** | Último plano excluído: exibir mensagem para gerar novo plano |

### UC 6: Geração de Novo Plano

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário autenticado com dados de perfil |
| **Pré-condições** | Usuário está na Home |
| **Fluxo Principal** | 1. Usuário clica em "Gerar Novo Plano" <br> 2. Sistema abre fluxo de preenchimento <br> 3. Sistema pré-preenche campos com dados do perfil <br> 4. Usuário pode atualizar informações <br> 5. Usuário confirma geração <br> 6. Sistema envia dados para API Gemini <br> 7. API Gemini gera novo plano <br> 8. Sistema salva novo plano <br> 9. Sistema redireciona para Detalhes do plano |
| **Pós-condições** | Novo plano salvo e visível na lista |
| **Fluxo Alternativo** | Usuário cancela: retorna para Home sem alteração |
| **Exceções** | API Gemini retorna erro: exibir mensagem e permitir retry |

### UC 7: Logout

| Campo | Descrição |
|-------|-----------|
| **Ator** | Usuário autenticado |
| **Pré-condições** | Usuário possui sessão ativa (token JWT válido armazenado no localStorage) |
| **Fluxo Principal** | 1. Usuário clica em "Sair" <br> 2. Sistema remove o token JWT do localStorage <br> 3. Sistema limpa o estado de autenticação da aplicação <br> 4. Sistema redireciona para a página de login |
| **Pós-condições** | Sessão encerrada; usuário redirecionado para login; acesso a páginas autenticadas bloqueado |
| **Fluxo Alternativo** | Token JWT expira (24h): sistema retorna erro 401, redireciona para login |
| **Exceções** | Nenhuma — logout é client-side e não depende de comunicação com o backend |

---

## 7. Definition Of Done (DOD)

### 7.1 Critérios de Aceite do Produto

- [ ] Todos os requisitos funcionais (US 1 à 9) implementados e testados
- [ ] Todos os requisitos não-funcionais atendidos
- [ ] Interface de usuário intuitiva e acessível (WCAG 2.1 nível A)
- [ ] Fluxo de primeiro acesso funcionando corretamente
- [ ] Fluxo de acessos posteriores com lista de planos funcionando
- [ ] Dados pré-preenchidos ao gerar novo plano
- [ ] Testes unitários com cobertura mínima de 70%
- [ ] Testes de integração passando
- [ ] Validação de segurança contra XSS implementada

### 7.2 Critérios de Aceite de Release

- [ ] Zero defeitos críticos abertos
- [ ] Zero defeitos maiores abertos
- [ ] Performance dentro dos parâmetros definidos (< 3s carregamento, < 10s API)
- [ ] Compatibilidade validada nos navegadores suportados

---

## 8. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Indisponibilidade da API Gemini | Alto | Média | Implementar cache local e mensagens de erro claras |
| Lentidão na geração de plano | Médio | Média | Exibir indicador de progresso e timeout adequado |

---

**Versão:** 1.0  
**Data de Criação:** 21-03-2026 
**Última Atualização:** 30-03-2026  
**Autor:** Mentoria.IA - Grupo 6  
**Status:** Rascunho