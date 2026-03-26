import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authService } from '@/services/authService'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  function loginRedirect() {
    authService.loginWithGoogle()
  }

  function handleCallback(accessToken: string, hasProfile: boolean): boolean {
    localStorage.setItem('token', accessToken)
    token.value = accessToken
    return hasProfile
  }

  function logout() {
    authService.logout()
    user.value = null
    token.value = null
  }

  return { user, token, isAuthenticated, loginRedirect, handleCallback, logout }
})
