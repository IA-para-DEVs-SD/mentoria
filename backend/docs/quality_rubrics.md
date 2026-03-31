# 📊 Rubrica de Qualidade — Mentoria.IA

Rubrica para avaliação técnica do projeto com base em quatro critérios ponderados.

Escala: 0 (inexistente) a 100 (excelente).

| Critério | Peso |
|---|---|
| Qualidade de Código | 30% |
| Clareza da Documentação | 20% |
| Segurança | 20% |
| Cobertura de Testes com Estratégia Clara | 30% |

---

## 1. Qualidade de Código (Peso: 30%)

### O que é avaliado neste critério

- **Arquitetura e separação de responsabilidades:** O código segue um padrão arquitetural claro (ex: camadas router/service/model)? Cada módulo tem responsabilidade única?
- **Tipagem e validação:** O projeto utiliza tipagem estática, enums e validação de dados para prevenir erros em tempo de execução?
- **Legibilidade e convenções:** O código segue convenções de nomenclatura consistentes? É fácil de ler e entender sem comentários excessivos?
- **Reutilização e DRY:** Existe duplicação desnecessária? Componentes, funções e lógica são reutilizados adequadamente?
- **Configuração e build:** O projeto possui Dockerfiles otimizados, configuração externalizada e build reproduzível?
- **Ferramentas de qualidade:** Linters, formatters e análise estática estão configurados e integrados ao fluxo de desenvolvimento?

---

## 2. Clareza da Documentação (Peso: 20%)

### O que é avaliado neste critério

- **Completude do PRD:** Todas as funcionalidades possuem User Stories com critérios de aceite mensuráveis e testáveis?
- **Glossário e terminologia:** Existe um glossário que padroniza termos usados no projeto? A terminologia é consistente entre documentos?
- **Decisões de design documentadas:** Decisões técnicas e de produto estão explicitadas com justificativas (notas de design)?
- **Documentação de arquitetura:** Existe documento descrevendo a arquitetura, fluxo de dados, infraestrutura e decisões técnicas?
- **README e onboarding:** Um novo desenvolvedor consegue entender o projeto, instalar e rodar apenas lendo o README?
- **Rastreabilidade:** É possível rastrear uma funcionalidade desde o requisito (PRD) até a issue, branch, commit e PR?
- **Automação de padrões:** Existem steerings ou guias que automatizam e padronizam a criação de artefatos (commits, issues, evidências)?

---

## 3. Segurança (Peso: 20%)

### O que é avaliado neste critério

- **Autenticação e autorização:** O sistema implementa autenticação robusta? Todas as rotas protegidas validam identidade do usuário?
- **Proteção de credenciais:** Segredos (API keys, tokens, senhas) estão fora do código-fonte e do repositório?
- **Validação e sanitização de entrada:** Todos os dados recebidos do usuário são validados e sanitizados antes de processamento?
- **Proteção contra ataques comuns:** Existem proteções contra XSS, CSRF, injection e exposição de informações sensíveis em erros?
- **Rate limiting:** O sistema limita requisições para prevenir abuso e ataques de força bruta?
- **Criptografia:** Dados sensíveis são protegidos em trânsito (HTTPS) e em repouso (criptografia no banco)?
- **Configuração segura de infraestrutura:** Docker, CORS, headers HTTP e firewall estão configurados adequadamente?

---

## 4. Cobertura de Testes com Estratégia Clara (Peso: 30%)

### O que é avaliado neste critério

- **Estratégia de teste em camadas:** Os testes cobrem diferentes camadas da aplicação (models, schemas, services, endpoints) de forma organizada?
- **Isolamento de dependências:** Testes usam mocks para dependências externas (APIs, banco de dados, cache)? Nenhum teste depende de serviço externo real?
- **Cobertura de cenários de erro:** Existem testes para caminhos de erro (404, 401, 409, 500, timeout)? Não apenas o caminho feliz?
- **Fixtures e reutilização:** Existem fixtures compartilhadas que evitam duplicação e facilitam a criação de cenários de teste?
- **Testes de integração:** Existem testes que validam o fluxo completo de um endpoint (request → response) com banco de dados?
- **Cobertura de frontend:** Existem testes para componentes, stores ou fluxos do frontend?
- **Medição de cobertura:** A cobertura de código é medida e reportada? Existe meta mínima definida?
- **Testes no pipeline de CI:** Os testes são executados automaticamente em cada push/PR?

---

## Resumo

| Critério | Peso | Nota (0-100) | Contribuição |
|---|---|---|---|
| Qualidade de Código | 30% | | |
| Clareza da Documentação | 20% | | |
| Segurança | 20% | | |
| Cobertura de Testes | 30% | | |
| **Nota Final Ponderada** | **100%** | | |
