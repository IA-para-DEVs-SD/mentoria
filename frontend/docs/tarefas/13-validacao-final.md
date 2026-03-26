# Tarefa 7 — Criar `.env.example` e validação final

**Executor:** agente mentoria-frontend (Opus 4.6)
**Dependência:** Todas as tarefas anteriores concluídas

## Arquivos a criar

- `frontend/.env.example`

## Arquivos a verificar

- Todos os modificados nas tarefas 1-6

## O que fazer

### 1. Criar `.env.example`

```
VITE_API_URL=http://localhost:8000
```

### 2. Rodar `npm run type-check`

Corrigir qualquer erro de tipo restante.

### 3. Rodar `npm run build`

Garantir que compila sem erros.

### 4. Verificar que não sobrou nenhum mock

Buscar nos services por:
- `delay(`
- `setTimeout`
- `localStorage` no `planService` ou `profileService` (profileService não deve mais usar localStorage)
- Arrays hardcoded de planos/ações
- Dados fake de usuário

### 5. Verificar que não sobrou referência a nomes antigos

Buscar em **todos os arquivos** `.ts` e `.vue` por:
- `titulo` (fora de labels/strings de exibição)
- `criadoEm`
- `acoes`
- `progresso` (fora de labels)
- `prioridade`
- `categoria`
- `concluida` (como campo de tipo, não como valor de enum)
- `experiencias`
- `formacoes`
- `habilidades`
- `senioridade`
- `instituicao`
- `areaEstudo`
- `dataInicio`
- `dataFim`

Nenhum desses deve aparecer como nome de campo em tipos, props, ou acessos a objetos. Podem aparecer apenas em strings de exibição (labels).

## Critério de aceite

- `npm run build` passa sem erros
- Zero referências a nomes antigos em campos/tipos
- `.env.example` existe com `VITE_API_URL`
- Nenhum mock restante nos services
