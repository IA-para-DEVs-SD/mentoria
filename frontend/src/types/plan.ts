export interface Gap {
  skill: string
  level: string
  ideal: string
}

export interface Action {
  id: string
  prioridade: 'ALTA' | 'MÉDIA' | 'BAIXA'
  categoria: string
  titulo: string
  objetivo: string
  contexto: string
  concluida: boolean
}

export interface Plan {
  id: string
  titulo: string
  criadoEm: string
  gaps: Gap[]
  acoes: Action[]
  progresso: number
}
