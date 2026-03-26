// Alinhado com backend: plans/schemas.py

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

export type ActionStatus = 'pendente' | 'concluida'

export type Priority = 'ALTA' | 'MEDIA' | 'BAIXA'

// ---------------------------------------------------------------------------
// Tipos de API
// ---------------------------------------------------------------------------

export interface Gap {
  id: string
  description: string
  relevance: number
}

export interface Action {
  id: string
  priority: Priority
  category: string
  title: string
  objective: string
  context: string
  status: ActionStatus
  sequence: number
}

export interface Plan {
  id: string
  name: string
  created_at: string
  progress: number
  gaps: Gap[]
  actions: Action[]
}

export interface PlanSummary {
  id: string
  name: string
  created_at: string
  progress: number
}

// ---------------------------------------------------------------------------
// Input schemas
// ---------------------------------------------------------------------------

export interface ActionStatusUpdate {
  status: ActionStatus
}

export interface ProgressOut {
  progress: number
}
