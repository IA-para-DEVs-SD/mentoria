export type Senioridade = 'Estágio' | 'Júnior' | 'Pleno' | 'Sênior' | 'Especialista' | 'Liderança'

export type NivelFormacao =
  | 'Ensino Médio' | 'Técnico' | 'Tecnólogo' | 'Bacharelado' | 'Licenciatura'
  | 'Pós-graduação' | 'MBA' | 'Mestrado' | 'Doutorado' | 'Pós-doutorado'

export type ObjetivoCarreira = 'Crescer na carreira atual' | 'Assumir cargos de liderança' | 'Mudar de área'

export interface Experiencia {
  cargo: string
  senioridade: Senioridade | null
  empresa?: string
  dataInicio: Date | null
  dataFim?: Date | null
}

export interface Formacao {
  instituicao: string
  nivel: NivelFormacao | null
  titulo: string
  areaEstudo: string
  dataInicio: Date | null
  dataFim?: Date | null
}

export interface ProfileData {
  experiencias: Experiencia[]
  formacoes: Formacao[]
  habilidades: string[]
  objetivo: ObjetivoCarreira | null
}
