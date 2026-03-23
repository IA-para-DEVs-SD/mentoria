import type { User } from '@/types'

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms))

export const authService = {
  async loginWithGoogle(): Promise<{ user: User; token: string }> {
    await delay(800)
    const user: User = {
      id: 'google-12345',
      name: 'Alex Silva',
      email: 'alex.silva@email.com',
      photo: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
    }
    const token = 'mock-jwt-token-xyz'
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    return { user, token }
  },

  async refreshToken(): Promise<string> {
    return 'mock-refreshed-token'
  },

  logout(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}
