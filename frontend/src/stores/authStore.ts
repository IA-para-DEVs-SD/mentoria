import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authService } from '@/services/authService'
import { useProfileStore } from '@/stores/profileStore'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const savedUser = localStorage.getItem('user')
  const user = ref<User | null>(savedUser ? JSON.parse(savedUser) : null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function login(): Promise<{ hasProfile: boolean }> {
    const result = await authService.loginWithGoogle()
    user.value = result.user
    token.value = result.token

    const profileStore = useProfileStore()
    await profileStore.loadProfile()
    return { hasProfile: !!profileStore.profile }
  }

  function logout() {
    authService.logout()
    user.value = null
    token.value = null
  }

  return { user, token, isAuthenticated, login, logout }
})
