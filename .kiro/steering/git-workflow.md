---
inclusion: auto
---

# Fluxo de Commit, Push e Pull Request

Quando o usuário solicitar commit, push ou pull request, o agente DEVE seguir rigorosamente
este fluxo padronizado.

## Referência de Commit

As mensagens de commit DEVEM seguir o padrão definido em: #[[file:.kiro/steering/commit-messages.md]]

## Fluxo Completo

### 1. Commit

Ao receber solicitação de commit:

1. Executar `git status` para verificar arquivos alterados/novos
2. Se não houver alterações, informar o usuário e encerrar
3. Executar `git add` apenas dos arquivos relevantes à tarefa (evitar `git add .` indiscriminado)
4. Gerar mensagem de commit seguindo o padrão de `commit-messages.md`:
   - Tipo correto (`feat`, `fix`, `docs`, `refactor`, `test`, etc.)
   - Breve descrição em minúsculas, sem ponto final, no imperativo
   - Primeira linha com no máximo 72 caracteres
   - Descrição detalhada opcional separada por linha em branco
   - Tudo em português (pt-BR)
5. Executar `git commit` com a mensagem gerada

### 2. Push

Ao receber solicitação de push (ou após commit quando o usuário pedir ambos):

1. Identificar a branch atual com `git branch --show-current`
2. Executar `git push origin {branch}`
3. Se o push falhar, informar o erro ao usuário e sugerir solução

### 3. Pull Request

Ao receber solicitação de PR (ou após push quando o usuário pedir o fluxo completo):

1. Identificar a branch atual e confirmar que não é `main`
2. Criar o PR com `gh pr create` contendo:
   - `--base main` (branch de destino)
   - `--head {branch_atual}` (branch de origem)
   - `--title` seguindo o mesmo padrão de commit semântico (tipo: descrição)
   - `--body` com seções:
     - `## Descrição` — resumo do que foi feito
     - `## O que foi feito` — lista concisa das alterações
     - `## Referência` — `Closes #XX` vinculando à issue correspondente (extrair número da branch se possível, ex: `feature/issue-44` → `Closes #44`)
3. Se o PR já existir para a branch, informar o usuário com o link existente

## Regras

1. Sempre verificar `git status` antes de qualquer commit.
2. Nunca commitar arquivos não relacionados à tarefa atual.
3. Se a branch seguir o padrão `feature/issue-XX`, extrair o número da issue para o `Closes #XX` do PR.
4. Mensagens de commit e títulos de PR devem estar em português (pt-BR).
5. Não fazer push para `main` diretamente — sempre via branch + PR.
6. Se o usuário pedir apenas "commit", fazer somente o commit. Se pedir "commit e push", fazer ambos. Se pedir "commit, push e PR", fazer o fluxo completo.
