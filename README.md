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

![Arquitetura do Sistema](/backend/docs/estrutura.png)

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

### Fluxo de Interação do Usuário

```mermaid
flowchart TD
    A[Usuário acessa plataforma] --> B[Login com Google]
    
    B --> C{Autenticado?}
    C -- Não --> D[Exibir erro / retry]
    
    C -- Sim --> E[Verificar dados de perfil]
    
    E --> F{Perfil existe?}
    
    F -- Não --> G[Onboarding]
    G --> H[Preencher dados em etapas]
    H --> I[Enviar dados para IA]
    I --> J[Gerar primeiro plano]
    J --> K[Salvar plano]
    K --> L[Ir para detalhes do plano]
    
    F -- Sim --> M[Ir para Home]
    
    M --> N{Ação do usuário}
    
    N -- Ver planos --> O[Listar planos]
    O --> P[Selecionar plano]
    P --> L
    
    N -- Gerar novo plano --> Q[Onboarding pré-preenchido]
    Q --> R[Atualizar dados]
    R --> I
    
    N -- Excluir plano --> S[Confirmar exclusão]
    S --> T[Remover plano]
    T --> M
    
    L --> U{Interações no plano}
    
    U -- Concluir ação --> V[Atualizar progresso]
    U -- Excluir ação --> W[Remover ação + recalcular]
    U -- Gerar novas ações --> X[Gerar novas ações via IA]
    
    V --> L
    W --> L
    X --> L
    
    L --> Y[Voltar para Home]
    Y --> M
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

```mermaid
erDiagram
    User ||--o| Profile : tem
    Profile ||--o{ Roadmap : gera
    Roadmap ||--|{ RoadmapStep : contém
    User ||--o{ ChatHistory : possui

    User {
        int id PK
        string email
        string password_hash
        datetime created_at
    }

    Profile {
        int id PK
        int user_id FK
        string nome
        string experiencia
        string[] habilidades
        string objetivos
        string setor
        string regiao
        string nivel
    }

    Roadmap {
        int id PK
        int profile_id FK
        string titulo
        string descricao
        json etapas
        string cronograma
        string status
        datetime created_at
    }

    ChatHistory {
        int id PK
        int user_id FK
        string role
        string content
        json context
        datetime created_at
    }

    RoadmapStep {
        int id PK
        int roadmap_id FK
        string titulo
        string descricao
        string prazo
        string[] recursos
        boolean concluido
    }
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
