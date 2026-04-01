# Tarefas de Integração Frontend ↔ Backend

**Executor:** agente mentoria-frontend (Opus 4.6)

## Tarefas

| # | Arquivo | Escopo | Dependência |
|---|---|---|---|
| 7 | [7-alinhar-tipos.md](docs/tarefas/7-alinhar-tipos.md) | Alinhar tipos TypeScript com schemas do backend | — |
| 8 | [8-reescrever-services.md](docs/tarefas/8-reescrever-services.md) | Reescrever services (mock → API real) | 7 |
| 9 | [9-atualizar-stores.md](docs/tarefas/9-atualizar-stores.md) | Atualizar stores para novos tipos e contratos | 7, 8 |
| 10 | [10-atualizar-onboarding.md](docs/tarefas/10-atualizar-onboarding.md) | Atualizar componentes de onboarding | 7, 8, 9 |
| 11 | [11-atualizar-plan-home.md](docs/tarefas/11-atualizar-plan-home.md) | Atualizar componentes de plano e home | 7, 8, 9 |
| 12 | [12-fluxo-oauth.md](docs/tarefas/12-fluxo-oauth.md) | Implementar fluxo OAuth (callback page, router) | 7, 8, 9 |
| 13 | [13-validacao-final.md](docs/tarefas/13-validacao-final.md) | `.env.example` + validação final (`npm run build`) | Todas |

## Ordem de execução

```
Tarefa 7 (tipos)
    ↓
Tarefa 8 (services)
    ↓
Tarefa 9 (stores)
    ↓
  ┌──────┼──────┐
  ↓      ↓      ↓
  T10    T11    T12     ← paralelas
  ↓      ↓      ↓
  └──────┼──────┘
         ↓
      Tarefa 13 (validação final)
```

## Notas para o agente

- **Não alterar** a estrutura de pastas nem criar arquivos fora do padrão definido nas instruções.
- **Não adicionar** dependências novas sem perguntar.
- **Não criar** testes (a menos que solicitado).
- Consultar os schemas do backend (`backend/app/*/schemas.py`) como fonte de verdade para os tipos.
- Ao encontrar divergência entre o contrato do frontend e do backend, priorizar o backend.
- O backend não tem endpoint `GET /auth/me`. Se precisar de dados do usuário logado, usar `GET /profile` ou decodificar o JWT.
- O backend não tem endpoint `POST /auth/refresh`. Remover qualquer referência a refresh token.
