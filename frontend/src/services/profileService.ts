import api from './api'
import type { ProfileData, ProfileOut } from '@/types'

export const profileService = {
  async getProfile(): Promise<ProfileOut | null> {
    try {
      const { data } = await api.get<ProfileOut>('/profile')
      return data
    } catch (error: any) {
      if (error.response?.status === 404) return null
      throw error
    }
  },

  async saveProfile(profile: ProfileData): Promise<ProfileOut> {
    const { data } = await api.post<ProfileOut>('/profile', profile)
    return data
  },
}
