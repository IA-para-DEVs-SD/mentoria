# Arquitetura — MentorIA

## Visão Geral

O MentorIA segue uma arquitetura de 3 camadas (frontend, backend, IA) com comunicação via REST + SSE, containerizada com Docker Compose e hospedada em um Droplet único na DigitalOcean.

## Decisões Arquiteturais

### Por que FastAPI + PydanticAI?

- FastAPI é nativamente async, ideal para chamadas à LLM que são I/O-bound
- PydanticAI permite definir agentes com outputs estruturados e validados via Pydantic
- A integração com Gemini é nativa no PydanticAI, sem wrappers adicionais
- Tipagem forte end-to-end: schemas Pydantic servem tanto para validação da API quanto para estruturar respostas da LLM

### Por que Vue.js + PrimeVue?

- Vue 3 com Composition API oferece reatividade granular e composables reutilizáveis
- PrimeVue fornece componentes enterprise-ready (DataTable, Timeline, Stepper) que aceleram o desenvolvimento do dashboard e roadmap
- Suporte nativo a temas e acessibilidade

### Por que Gemini?

- Custo-benefício competitivo para aplicações de análise de texto
- Suporte nativo no PydanticAI como provider
- Context window grande, útil para análise de perfis complexos
- Capacidade multimodal (futuro: análise de currículos em PDF)

---

## Agentes PydanticAI

O sistema utiliza 3 agentes especializados:

### 1. ProfileAnalyzer Agent

```python
# Responsabilidade: Analisar perfil e identificar gaps
# Input: Dados do perfil do usuário
# Output: Análise estruturada com pontos fortes, gaps e oportunidades
```

### 2. RoadmapGenerator Agent

```python
# Responsabilidade: Gerar plano de desenvolvimento personalizado
# Input: Análise do perfil + dados de mercado
# Output: Roadmap com etapas, prazos e recursos
# Usa: Dados de mercado como contexto adicional
```

### 3. MentorChat Agent

```python
# Responsabilidade: Conversa interativa de mentoria
# Input: Mensagem do usuário + contexto (perfil, roadmap, histórico)
# Output: Resposta contextualizada com orientações práticas
# Modo: Streaming via SSE
```

---

## Fluxo de Dados Detalhado

### Geração de Roadmap

```
1. Usuário preenche formulário de perfil (Vue.js)
2. Frontend envia POST /api/profile
3. Backend valida com Pydantic schema
4. Persiste no PostgreSQL
5. Dispara task async de análise
6. ProfileAnalyzer Agent processa perfil via Gemini
7. Market Service enriquece com dados de mercado
8. RoadmapGenerator Agent gera plano personalizado
9. Roadmap é persistido no PostgreSQL
10. WebSocket notifica frontend que roadmap está pronto
11. Frontend renderiza roadmap interativo (Timeline PrimeVue)
```

### Chat com Mentor IA

```
1. Usuário envia mensagem no chat
2. Frontend faz POST /api/chat
3. Backend carrega contexto: perfil + roadmap + últimas N mensagens
4. MentorChat Agent processa via Gemini com streaming
5. Resposta é enviada via SSE (Server-Sent Events)
6. Frontend renderiza resposta em tempo real
7. Mensagem é persistida no histórico (PostgreSQL)
```

---

## Infraestrutura DigitalOcean

Tudo roda em um único Droplet via Docker Compose. Simples, barato e suficiente para MVP.

```
Internet
    │
    ▼
┌──────────────────────────────────────────────┐
│         Droplet (4 vCPU / 8 GB RAM)          │
│              Docker Compose                   │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │  Nginx (container)                       │  │
│  │  - Reverse proxy                         │  │
│  │  - SSL (Let's Encrypt)                   │  │
│  │  - Serve frontend estático               │  │
│  └──────────┬──────────────────┬───────────┘  │
│             │                  │               │
│             ▼                  ▼               │
│  ┌────────────────┐  ┌────────────────┐       │
│  │  FastAPI        │  │  Worker         │       │
│  │  (container)    │  │  (container)    │       │
│  └───────┬────────┘  └───────┬────────┘       │
│          │                   │                 │
│          ▼                   ▼                 │
│  ┌────────────────┐  ┌────────────────┐       │
│  │  PostgreSQL     │  │  Redis          │       │
│  │  (container)    │  │  (container)    │       │
│  │  Volume: /data  │  │                 │       │
│  └────────────────┘  └────────────────┘       │
└──────────────────────────────────────────────┘
         │
         ▼
   Google Gemini API
```

### Composição dos Containers

| Container | Porta Interna | Descrição |
|---|---|---|
| nginx | 80, 443 | Reverse proxy + frontend estático |
| fastapi | 8000 | API principal |
| worker | — | Background jobs (análise IA, roadmaps) |
| postgres | 5432 | Banco de dados (volume persistente) |
| redis | 6379 | Cache e sessões |

### Por que Droplet único?

- Custo previsível (~$48/mês para 4vCPU/8GB)
- Zero complexidade de rede entre serviços (tudo em docker network local)
- Deploy simples: SSH + docker compose pull + up
- Suficiente para centenas de usuários simultâneos no MVP
- Migração futura: separar banco e cache para Managed Database quando necessário

---

## Segurança

- Autenticação via JWT (access + refresh tokens)
- HTTPS em todas as comunicações (Let's Encrypt via Certbot no Nginx)
- Rate limiting via Redis no backend
- CORS configurado para domínio específico
- Secrets gerenciados via `.env` no Droplet (fora do repositório)
- Dados sensíveis criptografados em repouso (volume encriptado)
- Firewall do DigitalOcean (Cloud Firewall) — apenas portas 80, 443 e 22 abertas
- Input sanitization em todas as entradas do usuário
- Prompt injection protection nos agentes PydanticAI

---

## Escalabilidade

A arquitetura atual é um Droplet único (MVP). O caminho de evolução:

1. **Fase atual (MVP)** — Tudo no Droplet via Docker Compose
2. **Fase 2** — Separar PostgreSQL e Redis para Managed Database/Redis da DigitalOcean
3. **Fase 3** — Adicionar Load Balancer + múltiplos Droplets para o backend
4. **Fase 4** — Frontend em Spaces + CDN, backend em Droplets com auto-scaling

Otimizações já aplicáveis no MVP:
- Cache de respostas da LLM no Redis (respostas similares)
- Background workers para processamento assíncrono de roadmaps
- Volume persistente para dados do PostgreSQL (sobrevive a recreate do container)
