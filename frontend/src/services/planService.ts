import type { Plan, Action, ProfileData } from '@/types'

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms))

let nextId = 3

const MONTH_NAMES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

function buildTitle(profile: ProfileData): string {
  const objetivo = profile.objetivo ?? 'Desenvolvimento'
  const senioridade = profile.experiencias[0]?.senioridade ?? 'Profissional'
  const now = new Date()
  return `Plano de ${objetivo} — ${senioridade} — ${MONTH_NAMES[now.getMonth()]} ${now.getFullYear()}`
}

function buildGaps(profile: ProfileData) {
  const gapsByObjetivo: Record<string, { skill: string; level: string; ideal: string }[]> = {
    'Assumir cargos de liderança': [
      { skill: 'Gestão de Pessoas', level: 'Iniciante', ideal: 'Avançado' },
      { skill: 'Comunicação Executiva', level: 'Intermediário', ideal: 'Avançado' },
      { skill: 'Pensamento Estratégico', level: 'Iniciante', ideal: 'Intermediário' },
    ],
    'Crescer na carreira atual': [
      { skill: 'Arquitetura de Software', level: 'Intermediário', ideal: 'Avançado' },
      { skill: 'Resolução de Problemas Complexos', level: 'Intermediário', ideal: 'Avançado' },
      { skill: 'Mentoria de Pares', level: 'Iniciante', ideal: 'Intermediário' },
    ],
    'Mudar de área': [
      { skill: 'Fundamentos da Nova Área', level: 'Iniciante', ideal: 'Intermediário' },
      { skill: 'Networking Estratégico', level: 'Iniciante', ideal: 'Avançado' },
      { skill: 'Adaptabilidade', level: 'Intermediário', ideal: 'Avançado' },
    ],
  }
  return gapsByObjetivo[profile.objetivo ?? ''] ?? gapsByObjetivo['Crescer na carreira atual']!
}

function buildAcoes(profile: ProfileData, planId: string): Action[] {
  const cargo = profile.experiencias[0]?.cargo ?? 'profissional'
  const acoesByObjetivo: Record<string, Omit<Action, 'id' | 'concluida'>[]> = {
    'Assumir cargos de liderança': [
      { prioridade: 'ALTA', categoria: 'Liderança', titulo: 'Desenvolvimento de Inteligência Emocional', objetivo: 'Desenvolver habilidades de gestão emocional para liderar equipes', contexto: `Como ${cargo}, essa competência é essencial para assumir posições de liderança` },
      { prioridade: 'ALTA', categoria: 'Gestão', titulo: 'Prática de Delegação e Feedback', objetivo: 'Aprender a delegar tarefas e dar feedback construtivo', contexto: `Líderes eficazes delegam com clareza e desenvolvem seus liderados` },
      { prioridade: 'MÉDIA', categoria: 'Comunicação', titulo: 'Comunicação com Stakeholders', objetivo: 'Apresentar ideias técnicas para públicos não-técnicos', contexto: `Traduzir complexidade em linguagem acessível é chave para liderança` },
      { prioridade: 'MÉDIA', categoria: 'Estratégia', titulo: 'Visão Estratégica de Produto', objetivo: 'Entender métricas de negócio e alinhar decisões técnicas', contexto: `Conectar tecnologia a resultados de negócio diferencia líderes técnicos` },
      { prioridade: 'BAIXA', categoria: 'Desenvolvimento Geral', titulo: 'Construir Marca Pessoal', objetivo: 'Participar de eventos e produzir conteúdo técnico', contexto: `Visibilidade na comunidade fortalece sua trajetória de liderança` },
    ],
    'Crescer na carreira atual': [
      { prioridade: 'ALTA', categoria: 'Técnico', titulo: 'Aprofundar Conhecimentos em Arquitetura', objetivo: 'Dominar padrões arquiteturais e design de sistemas escaláveis', contexto: `Para crescer como ${cargo}, visão arquitetural sólida é fundamental` },
      { prioridade: 'ALTA', categoria: 'Técnico', titulo: 'Dominar Testes e Qualidade de Código', objetivo: 'Implementar estratégias de testes automatizados', contexto: `Profissionais seniores garantem qualidade através de testes robustos` },
      { prioridade: 'MÉDIA', categoria: 'Colaboração', titulo: 'Mentoria de Colegas Júnior', objetivo: 'Desenvolver habilidade de ensinar e guiar outros desenvolvedores', contexto: `Mentorar pares demonstra maturidade e acelera seu crescimento` },
      { prioridade: 'MÉDIA', categoria: 'Processo', titulo: 'Contribuir em Decisões Técnicas', objetivo: 'Participar ativamente de code reviews e ADRs', contexto: `Influenciar decisões técnicas é marca de profissionais seniores` },
      { prioridade: 'BAIXA', categoria: 'Desenvolvimento Geral', titulo: 'Explorar Tecnologias Complementares', objetivo: 'Ampliar repertório com tecnologias adjacentes à sua stack', contexto: `Versatilidade técnica abre portas para projetos mais complexos` },
    ],
    'Mudar de área': [
      { prioridade: 'ALTA', categoria: 'Fundamentos', titulo: 'Mapear Competências da Nova Área', objetivo: 'Identificar skills essenciais e criar plano de estudo', contexto: `Como ${cargo} em transição, o primeiro passo é entender o terreno` },
      { prioridade: 'ALTA', categoria: 'Networking', titulo: 'Conectar-se com Profissionais da Área', objetivo: 'Construir rede de contatos na nova área de atuação', contexto: `Networking acelera transições de carreira e abre oportunidades` },
      { prioridade: 'MÉDIA', categoria: 'Prática', titulo: 'Desenvolver Projeto Prático', objetivo: 'Criar portfólio com projetos relevantes para a nova área', contexto: `Projetos práticos demonstram capacidade mesmo sem experiência formal` },
      { prioridade: 'MÉDIA', categoria: 'Formação', titulo: 'Buscar Formação Complementar', objetivo: 'Cursos e certificações relevantes para a transição', contexto: `Formação direcionada preenche gaps de conhecimento rapidamente` },
      { prioridade: 'BAIXA', categoria: 'Desenvolvimento Geral', titulo: 'Aproveitar Competências Transferíveis', objetivo: 'Identificar e comunicar skills que se aplicam à nova área', contexto: `Sua experiência como ${cargo} traz perspectivas valiosas` },
    ],
  }
  const base = acoesByObjetivo[profile.objetivo ?? ''] ?? acoesByObjetivo['Crescer na carreira atual']!
  return base!.map((a, i) => ({ ...a, id: `${planId}-a${i + 1}`, concluida: false }))
}

function createMockPlan(id: string, titulo: string, criadoEm: string): Plan {
  return {
    id,
    titulo,
    criadoEm,
    gaps: [
      { skill: 'Gestão de Pessoas', level: 'Básico', ideal: 'Avançado' },
      { skill: 'Arquitetura de Software', level: 'Intermediário', ideal: 'Avançado' },
      { skill: 'Comunicação Executiva', level: 'Básico', ideal: 'Intermediário' },
    ],
    acoes: [
      { id: `${id}-a1`, prioridade: 'ALTA', categoria: 'Liderança', titulo: 'Desenvolver habilidades de gestão de equipe', objetivo: 'Capacitar-se em gestão de pessoas e delegação de tarefas', contexto: 'Como profissional buscando liderança, é essencial dominar gestão de equipes', concluida: false },
      { id: `${id}-a2`, prioridade: 'ALTA', categoria: 'Técnico', titulo: 'Aprofundar conhecimentos em arquitetura de software', objetivo: 'Dominar padrões arquiteturais e design de sistemas escaláveis', contexto: 'Para liderar tecnicamente, é necessário ter visão arquitetural sólida', concluida: false },
      { id: `${id}-a3`, prioridade: 'MÉDIA', categoria: 'Comunicação', titulo: 'Praticar comunicação com stakeholders', objetivo: 'Melhorar a capacidade de apresentar ideias para públicos não-técnicos', contexto: 'Líderes técnicos precisam traduzir complexidade em linguagem acessível', concluida: false },
      { id: `${id}-a4`, prioridade: 'BAIXA', categoria: 'Desenvolvimento Geral', titulo: 'Construir marca pessoal na comunidade tech', objetivo: 'Participar de eventos e produzir conteúdo técnico', contexto: 'Visibilidade na comunidade fortalece a trajetória de liderança', concluida: false },
    ],
    progresso: 0,
  }
}

let mockPlans: Plan[] = [
  createMockPlan('1', 'Plano Liderança — Sênior para Tech Lead — Mar 2026', '2026-03-20'),
  createMockPlan('2', 'Plano Crescimento — Pleno para Sênior — Mar 2026', '2026-03-18'),
]

function calcProgress(plan: Plan): number {
  if (plan.acoes.length === 0) return 0
  return Math.round((plan.acoes.filter((a) => a.concluida).length / plan.acoes.length) * 100)
}

export const planService = {
  async getPlans(): Promise<Plan[]> {
    return [...mockPlans]
  },

  async getPlanById(id: string): Promise<Plan | undefined> {
    return mockPlans.find((p) => p.id === id)
  },

  async generatePlan(profile: ProfileData): Promise<Plan> {
    await delay(2500)
    const id = String(nextId++)
    const plan: Plan = {
      id,
      titulo: buildTitle(profile),
      criadoEm: new Date().toISOString().slice(0, 10),
      gaps: buildGaps(profile),
      acoes: buildAcoes(profile, id),
      progresso: 0,
    }
    mockPlans.unshift(plan)
    return plan
  },

  async deletePlan(id: string): Promise<void> {
    mockPlans = mockPlans.filter((p) => p.id !== id)
  },

  async toggleAction(planId: string, actionId: string): Promise<Plan | undefined> {
    const plan = mockPlans.find((p) => p.id === planId)
    if (!plan) return undefined
    const action = plan.acoes.find((a) => a.id === actionId)
    if (action) action.concluida = !action.concluida
    plan.progresso = calcProgress(plan)
    return { ...plan }
  },

  async deleteAction(planId: string, actionId: string): Promise<Plan | undefined> {
    const plan = mockPlans.find((p) => p.id === planId)
    if (!plan) return undefined
    plan.acoes = plan.acoes.filter((a) => a.id !== actionId)
    plan.progresso = calcProgress(plan)
    return { ...plan }
  },

  async generateMoreActions(planId: string): Promise<Plan | undefined> {
    await delay(1500)
    const plan = mockPlans.find((p) => p.id === planId)
    if (!plan) return undefined
    const newAction: Action = {
      id: `${planId}-a${plan.acoes.length + 1}`,
      prioridade: 'MÉDIA',
      categoria: 'Desenvolvimento Geral',
      titulo: 'Estudar metodologias ágeis avançadas',
      objetivo: 'Dominar frameworks como SAFe e práticas de continuous delivery',
      contexto: 'Complementa sua trajetória com visão de processos e entrega contínua',
      concluida: false,
    }
    plan.acoes.push(newAction)
    plan.progresso = calcProgress(plan)
    return { ...plan }
  },
}
