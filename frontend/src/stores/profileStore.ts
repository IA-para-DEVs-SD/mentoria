import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { profileService } from '@/services/profileService'
import type { ProfileData } from '@/types'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref<ProfileData | null>(null)

  const hasProfile = computed(() => !!profile.value)

  async function loadProfile() {
    profile.value = await profileService.getProfile()
  }

  async function saveProfile(data: ProfileData) {
    profile.value = await profileService.saveProfile(data)
  }

  return { profile, hasProfile, loadProfile, saveProfile }
})
