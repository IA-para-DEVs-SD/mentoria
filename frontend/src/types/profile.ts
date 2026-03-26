// Alinhado com backend: profile/schemas.py

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

export type Seniority =
  | 'Estagio' | 'Junior' | 'Pleno' | 'Senior' | 'Especialista' | 'Lideranca'

export type EducationLevel =
  | 'Ensino_Medio' | 'Tecnico' | 'Tecnologo' | 'Bacharelado' | 'Licenciatura'
  | 'Pos_graduacao' | 'MBA' | 'Mestrado' | 'Doutorado' | 'Pos_doutorado'

export type CareerGoal =
  | 'Crescer_na_carreira_atual' | 'Assumir_cargos_de_lideranca' | 'Mudar_de_area'

// ---------------------------------------------------------------------------
// Label maps (exibição em português)
// ---------------------------------------------------------------------------

export const SENIORITY_LABELS: Record<Seniority, string> = {
  Estagio: 'Estágio',
  Junior: 'Júnior',
  Pleno: 'Pleno',
  Senior: 'Sênior',
  Especialista: 'Especialista',
  Lideranca: 'Liderança',
}

export const EDUCATION_LEVEL_LABELS: Record<EducationLevel, string> = {
  Ensino_Medio: 'Ensino Médio',
  Tecnico: 'Técnico',
  Tecnologo: 'Tecnólogo',
  Bacharelado: 'Bacharelado',
  Licenciatura: 'Licenciatura',
  Pos_graduacao: 'Pós-graduação',
  MBA: 'MBA',
  Mestrado: 'Mestrado',
  Doutorado: 'Doutorado',
  Pos_doutorado: 'Pós-doutorado',
}

export const CAREER_GOAL_LABELS: Record<CareerGoal, string> = {
  Crescer_na_carreira_atual: 'Crescer na carreira atual',
  Assumir_cargos_de_lideranca: 'Assumir cargos de liderança',
  Mudar_de_area: 'Mudar de área',
}

// ---------------------------------------------------------------------------
// Tipos de API (strings para datas — usados em services/stores)
// ---------------------------------------------------------------------------

export interface Experience {
  role: string
  seniority: Seniority
  company: string | null
  start_date: string
  end_date: string | null
}

export interface Education {
  institution: string
  level: EducationLevel
  title: string
  study_area: string
  start_date: string
  end_date: string | null
}

export interface ProfileData {
  experiences: Experience[]
  educations: Education[]
  skills: string[]
  career_goal: CareerGoal
}

export interface ExperienceOut extends Experience {
  id: string
}

export interface EducationOut extends Education {
  id: string
}

export interface ProfileOut {
  id: string
  career_goal: CareerGoal
  skills: string[]
  experiences: ExperienceOut[]
  educations: EducationOut[]
  created_at: string
  updated_at: string
}

// ---------------------------------------------------------------------------
// Tipos de formulário (Date | null para datas — usados nos componentes)
// ---------------------------------------------------------------------------

export interface ExperienceForm {
  role: string
  seniority: Seniority | null
  company: string
  start_date: Date | null
  end_date: Date | null
}

export interface EducationForm {
  institution: string
  level: EducationLevel | null
  title: string
  study_area: string
  start_date: Date | null
  end_date: Date | null
}

export interface ProfileForm {
  experiences: ExperienceForm[]
  educations: EducationForm[]
  skills: string[]
  career_goal: CareerGoal | null
}
