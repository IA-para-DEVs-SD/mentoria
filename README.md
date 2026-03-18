# 🎯 MentorIA

> **Mentoria Inteligente para sua Carreira**

## O Problema

Profissionais enfrentam dificuldades em identificar caminhos claros para crescimento profissional, sem acesso a mentoria personalizada e acessível.

## A Solução

Interface intuitiva que transforma dados em insights acionáveis, gerando planos personalizados baseados em análise profunda de IA.

## Como Funciona

1. **Mapa do Perfil** — Captura de informações sobre experiência, habilidades, objetivos e contexto profissional específico.
2. **Análise de IA** — Processamento inteligente que cruza dados pessoais com tendências reais do mercado de trabalho.
3. **Plano Personalizado** — Geração de roadmap específico com ações práticas e cronograma para desenvolvimento profissional.

## Diferenciais

| Diferencial | Descrição |
|---|---|
| Personalização Profunda | Análise contextualizada considerando setor, região, perfil específico e objetivos únicos |
| Dados Reais do Mercado | Informações atualizadas e verificadas sobre demandas reais e tendências profissionais |
| Resultados Concretos | Recomendações baseadas em tendências comprovadas com acompanhamento em tempo real |
| IA que Aprende | Inteligência artificial que melhora constantemente com cada interação |

---

## Arquitetura do Sistema

### Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Frontend | Vue.js 3 + PrimeVue | Componentização rica, UI profissional e responsiva |
| Backend | Python + FastAPI | Alta performance async, tipagem forte, ecossistema IA |
| LLM | Google Gemini via PydanticAI | Estruturação de outputs com validação, agentes inteligentes |
| Banco de Dados | PostgreSQL (container) | Dados relacionais, perfis, histórico de interações |
| Cache | Redis (container) | Sessões, cache de respostas da LLM, rate limiting |
| Infra | Docker Compose em Droplet único | Tudo num só servidor, simples e barato para MVP |
| CI/CD | GitHub Actions | Automação de deploy integrada ao repositório |

### Diagrama de Arquitetura

```
┌──────────────────────────────────────────────────────────────────┐
│                  DigitalOcean — Droplet Único                     │
│                     (Docker Compose)                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Nginx (container)                                        │    │
│  │  - Reverse proxy (API + Frontend)                         │    │
│  │  - SSL (Let's Encrypt / Certbot)                          │    │
│  │  - Serve arquivos estáticos do Vue.js                     │    │
│  └──────────┬──────────────────────────────┬────────────────┘    │
│             │                              │                      │
│             ▼                              ▼                      │
│  ┌──────────────────┐          ┌──────────────────┐              │
│  │  FastAPI (container)│          │  Worker (container)│              │
│  │                    │          │                    │              │
│  │  - Auth            │          │  - Análise IA      │              │
│  │  - Perfil API      │          │  - Geração de      │              │
│  │  - Roadmap API     │          │    Roadmaps        │              │
│  │  - Chat (SSE)      │          │  - Atualização     │              │
│  │  - WebSocket       │          │    de Mercado      │              │
│  └────────┬───────────┘          └─────────┬──────────┘              │
│           │                                │                      │
│           ▼                                ▼                      │
│  ┌──────────────────┐          ┌──────────────────┐              │
│  │  PostgreSQL       │          │  Redis            │              │
│  │  (container)      │          │  (container)      │              │
│  │                   │          │                   │              │
│  │  - Perfis         │          │  - Sessões        │              │
│  │  - Roadmaps       │          │  - Cache LLM      │              │
│  │  - Histórico      │          │  - Rate Limit     │              │
│  └──────────────────┘          └──────────────────┘              │
│                                                                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │  Google Gemini    │
                      │  (via PydanticAI) │
                      │                   │
                      │  - Análise perfil │
                      │  - Tendências     │
                      │  - Roadmap gen    │
                      │  - Chat mentor    │
                      └──────────────────┘
```

### Fluxo de Interação do Usuário

```
┌─────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Início  │────▶│  Cadastro /   │────▶│  Mapa do      │────▶│  Análise IA   │
│          │     │  Login        │     │  Perfil       │     │  (Background) │
└─────────┘     └──────────────┘     └──────────────┘     └──────┬───────┘
                                                                  │
                ┌──────────────┐     ┌──────────────┐            │
                │  Acompanha-   │◀────│  Roadmap      │◀───────────┘
                │  mento        │     │  Personalizado│
                └──────┬───────┘     └──────────────┘
                       │
                       ▼
                ┌──────────────┐     ┌──────────────┐
                │  Chat com     │────▶│  Refinamento  │──── (ciclo contínuo)
                │  Mentor IA    │     │  do Plano     │
                └──────────────┘     └──────────────┘
```

#### Detalhamento do Fluxo

```
Usuário                    Frontend (Vue.js)           Backend (FastAPI)           Gemini (PydanticAI)
  │                              │                           │                           │
  │  1. Acessa plataforma        │                           │                           │
  │─────────────────────────────▶│                           │                           │
  │                              │                           │                           │
  │  2. Preenche perfil          │                           │                           │
  │  (experiência, skills,       │                           │                           │
  │   objetivos, setor, região)  │                           │                           │
  │─────────────────────────────▶│  3. POST /api/profile     │                           │
  │                              │──────────────────────────▶│                           │
  │                              │                           │  4. Valida e persiste     │
  │                              │                           │                           │
  │                              │                           │  5. Envia para análise    │
  │                              │                           │──────────────────────────▶│
  │                              │                           │                           │
  │                              │                           │  6. Gemini analisa perfil │
  │                              │                           │     + dados de mercado    │
  │                              │                           │     + tendências          │
  │                              │                           │◀──────────────────────────│
  │                              │                           │                           │
  │                              │  7. WebSocket: roadmap    │                           │
  │  8. Visualiza roadmap        │◀──────────────────────────│                           │
  │◀─────────────────────────────│                           │                           │
  │                              │                           │                           │
  │  9. Interage com chat IA     │                           │                           │
  │─────────────────────────────▶│  10. POST /api/chat       │                           │
  │                              │──────────────────────────▶│  11. Streaming response   │
  │                              │                           │──────────────────────────▶│
  │  12. Recebe resposta         │  13. SSE stream           │◀──────────────────────────│
  │◀─────────────────────────────│◀──────────────────────────│                           │
  │                              │                           │                           │
  │  14. Acompanha progresso     │                           │                           │
  │─────────────────────────────▶│  15. GET /api/progress    │                           │
  │                              │──────────────────────────▶│                           │
  │  16. Dashboard atualizado    │◀──────────────────────────│                           │
  │◀─────────────────────────────│                           │                           │
```

---

## Estrutura do Projeto

```
mentoria/
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── router/
│       ├── stores/          # Pinia stores
│       ├── composables/     # Lógica reutilizável
│       ├── services/        # Chamadas API
│       ├── components/      # Componentes PrimeVue customizados
│       └── views/
│           ├── LoginView.vue
│           ├── ProfileView.vue
│           ├── RoadmapView.vue
│           ├── ChatView.vue
│           └── DashboardView.vue
│
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── main.py          # FastAPI app
│       ├── config.py        # Settings via pydantic-settings
│       ├── models/          # SQLAlchemy models
│       ├── schemas/         # Pydantic schemas
│       ├── api/
│       │   ├── auth.py
│       │   ├── profile.py
│       │   ├── roadmap.py
│       │   └── chat.py
│       ├── services/
│       │   ├── ai_agent.py  # PydanticAI agents (Gemini)
│       │   ├── market.py    # Dados de mercado
│       │   └── roadmap.py   # Geração de roadmaps
│       └── core/
│           ├── auth.py
│           ├── database.py
│           └── redis.py
│
└── infra/
    ├── terraform/           # IaC para DigitalOcean
    └── nginx/               # Reverse proxy config
```

## Endpoints Principais da API

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/register` | Cadastro de usuário |
| POST | `/api/auth/login` | Autenticação (JWT) |
| POST | `/api/profile` | Criar/atualizar perfil profissional |
| GET | `/api/profile` | Obter perfil do usuário |
| POST | `/api/roadmap/generate` | Gerar roadmap personalizado |
| GET | `/api/roadmap` | Obter roadmap atual |
| PATCH | `/api/roadmap/progress` | Atualizar progresso |
| POST | `/api/chat` | Enviar mensagem ao mentor IA (SSE) |
| GET | `/api/chat/history` | Histórico de conversas |
| GET | `/api/dashboard` | Dados do dashboard de progresso |

## Modelo de Dados Simplificado

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    User       │     │    Profile        │     │    Roadmap        │
├──────────────┤     ├──────────────────┤     ├──────────────────┤
│ id           │──┐  │ id               │──┐  │ id               │
│ email        │  └─▶│ user_id (FK)     │  └─▶│ profile_id (FK)  │
│ password_hash│     │ nome             │     │ titulo           │
│ created_at   │     │ experiencia      │     │ descricao        │
└──────────────┘     │ habilidades[]    │     │ etapas (JSON)    │
                     │ objetivos        │     │ cronograma       │
                     │ setor            │     │ status           │
                     │ regiao           │     │ created_at       │
                     │ nivel            │     └──────────────────┘
                     └──────────────────┘              │
                                                       ▼
                     ┌──────────────────┐     ┌──────────────────┐
                     │  ChatHistory      │     │  RoadmapStep      │
                     ├──────────────────┤     ├──────────────────┤
                     │ id               │     │ id               │
                     │ user_id (FK)     │     │ roadmap_id (FK)  │
                     │ role             │     │ titulo           │
                     │ content          │     │ descricao        │
                     │ context (JSON)   │     │ prazo            │
                     │ created_at       │     │ recursos[]       │
                     └──────────────────┘     │ concluido        │
                                              └──────────────────┘
```

## Como Rodar Localmente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/mentoria.git
cd mentoria

# Subir todos os serviços
docker compose up -d

# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Docs API: http://localhost:8000/docs
```

### Variáveis de Ambiente

```env
# Backend
GEMINI_API_KEY=sua-chave-gemini
DATABASE_URL=postgresql://user:pass@postgres:5432/mentoria
REDIS_URL=redis://redis:6379
JWT_SECRET=sua-chave-secreta

# Frontend
VITE_API_URL=http://localhost:8000
```

### Droplet Recomendado (MVP)

- Droplet: 4 vCPU / 8 GB RAM (~$48/mês)
- Volume adicional de 50 GB para dados do PostgreSQL (persistência fora do container)

## Deploy (DigitalOcean)

O deploy é automatizado via GitHub Actions:

1. Push na branch `main` dispara o pipeline
2. Build das imagens Docker (frontend + backend)
3. Push para DigitalOcean Container Registry (DOCR)
4. SSH no Droplet → `docker compose pull && docker compose up -d`

---

## Licença

MIT
