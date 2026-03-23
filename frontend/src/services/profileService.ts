import type { ProfileData } from '@/types'

const STORAGE_KEY = 'mentoria-profile'

function reviveDates(profile: ProfileData): ProfileData {
  profile.experiencias.forEach((e) => {
    e.dataInicio = e.dataInicio ? new Date(e.dataInicio) : null
    e.dataFim = e.dataFim ? new Date(e.dataFim) : null
  })
  profile.formacoes.forEach((f) => {
    f.dataInicio = f.dataInicio ? new Date(f.dataInicio) : null
    f.dataFim = f.dataFim ? new Date(f.dataFim) : null
  })
  return profile
}

export const profileService = {
  async getProfile(): Promise<ProfileData | null> {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return reviveDates(JSON.parse(raw))
  },

  async saveProfile(data: ProfileData): Promise<ProfileData> {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    return data
  },
}
