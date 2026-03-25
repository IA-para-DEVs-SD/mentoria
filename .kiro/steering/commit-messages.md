---
inclusion: auto
---

# Padrão de Mensagens de Commit

Ao gerar mensagens de commit, siga rigorosamente o padrão de commit semântico abaixo.

## Formato

```
tipo: breve descrição

descrição mais detalhada (opcional)
```

## Tipos permitidos

- `feat`: Nova funcionalidade
- `fix`: Correções
- `docs`: Documentações
- `refactor`: Refatorações
- `test`: Testes unitários, de integração, etc.
- `style`: Formatação, ponto e vírgula, espaços (sem alteração de lógica)
- `chore`: Tarefas de manutenção, configs, dependências
- `ci`: Alterações em pipelines de CI/CD
- `build`: Alterações no sistema de build ou dependências externas
- `perf`: Melhorias de performance
- `revert`: Reversão de um commit anterior

## Regras

1. A primeira linha deve conter apenas o tipo e uma breve descrição, separados por `: `.
2. A breve descrição deve ser escrita em letras minúsculas, sem ponto final, e no imperativo (ex: "adiciona filtro de busca").
3. A descrição detalhada é opcional e deve ser separada da primeira linha por uma linha em branco.
4. Mantenha a primeira linha com no máximo 72 caracteres.
5. Escreva as mensagens em português (pt-BR).

## Exemplos

```
feat: adiciona autenticação via Google OAuth
```

```
fix: corrige redirecionamento após login expirado

O token expirado não estava sendo tratado corretamente,
causando um loop de redirecionamento na página de login.
```

```
refactor: extrai lógica de validação do formulário de onboarding
```

```
docs: atualiza README com instruções de setup local
```

```
tests: adiciona testes para o serviço de planos
```
