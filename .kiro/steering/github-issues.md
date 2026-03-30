---
inclusion: auto
---

# Padrão de Criação de Issues (User Stories) no GitHub

Ao criar issues para o board do projeto ([Board do Projeto](https://github.com/orgs/IA-para-DEVs-SD/projects/24/views/2)), siga rigorosamente o padrão abaixo.

## Referência

Todas as issues devem estar alinhadas com as User Stories e critérios de aceite definidos no PRD: #[[file:backend/docs/PRD.md]]

## Formato do Título

```
[US-X] Breve descrição da funcionalidade
```

- `US-X` corresponde à User Story do PRD (ex: US-1, US-2, etc.)
- A descrição deve ser curta, objetiva e no infinitivo (ex: "Implementar autenticação com Google OAuth")
- Se a issue não estiver vinculada a uma US específica, use um prefixo adequado: `[TECH]` para tarefas técnicas, `[BUG]` para correções, `[DOCS]` para documentação

## Formato da Descrição

A descrição da issue deve seguir este template:

```markdown
## Descrição
Breve explicação do que deve ser feito e por quê.

## User Story
**Como** [tipo de usuário],
**Eu quero** [ação desejada],
**Para que** [benefício esperado].

## Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

## Observações
Informações adicionais, restrições, dependências ou links relevantes.
```

## Regras

1. Sempre vincular a issue à User Story correspondente do PRD quando aplicável.
2. Os critérios de aceite devem ser copiados ou derivados diretamente do PRD.
3. Escrever tudo em português (pt-BR).
4. Cada issue deve representar uma entrega funcional testável — evitar issues genéricas ou muito amplas.
5. Se uma US for grande demais, quebre em sub-issues menores mantendo o prefixo `[US-X]`.
6. Incluir labels adequadas: `frontend`, `backend`, `ia`, `infra`, `docs`, `bug`.
7. Toda issue deve ser atribuída a pelo menos um responsável.
8. **Toda issue criada DEVE ser vinculada ao board do projeto** usando o comando `gh project item-add 24 --owner IA-para-DEVs-SD --url <URL_DA_ISSUE>` imediatamente após a criação da issue.
9. **Após criar a issue, DEVE ser criada uma branch local** seguindo o padrão `feature/issue-X`, onde `X` é o número da issue criada no GitHub. A branch deve ser criada a partir da `main` atualizada.

## Vinculação ao Board

Após criar cada issue com `gh issue create`, execute obrigatoriamente:

```bash
gh project item-add 24 --owner IA-para-DEVs-SD --url <URL_DA_ISSUE_CRIADA>
```

Isso garante que a issue apareça automaticamente no [board do projeto](https://github.com/orgs/IA-para-DEVs-SD/projects/24).

## Criação de Branch

Após criar a issue e vinculá-la ao board, crie a branch local a partir da `main` atualizada:

```bash
git checkout main
git pull
git checkout -b feature/issue-<NUMERO_DA_ISSUE>
```

Exemplo: para a issue #42, a branch será `feature/issue-42`.

## Exemplos

### Título
```
[US-1] Implementar autenticação com Google OAuth
```

### Descrição
```markdown
## Descrição
Implementar o fluxo de login via Google OAuth 2.0, incluindo criação do usuário no banco e redirecionamento condicional (Home ou Onboarding).

## User Story
**Como** usuário,
**Eu quero** fazer login com minha conta Google,
**Para que** eu possa acessar a plataforma de forma rápida e segura.

## Critérios de Aceite
- [ ] Exibir botão de login com Google na página inicial
- [ ] Após autenticação, verificar se o usuário possui dados de perfil salvos
- [ ] Se existirem dados de perfil, redirecionar para Home
- [ ] Se não existirem, redirecionar para Onboarding
- [ ] Armazenar nome, e-mail e foto do usuário após autenticação

## Observações
- Dados capturados do login (nome, e-mail, foto) não são editáveis pelo usuário.
- Labels: `backend`, `frontend`
```

### Título (tarefa técnica)
```
[TECH] Configurar Docker Compose com PostgreSQL e Redis
```

### Descrição
```markdown
## Descrição
Configurar o docker-compose.yml com os serviços de banco de dados (PostgreSQL) e cache (Redis) para o ambiente de desenvolvimento local.

## Critérios de Aceite
- [ ] PostgreSQL acessível na porta 5432 com volume persistente
- [ ] Redis acessível na porta 6379
- [ ] Arquivo .env.example atualizado com as variáveis necessárias
- [ ] Serviços sobem corretamente com `docker compose up -d`

## Observações
- Labels: `infra`
```
