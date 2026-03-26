// TODO: requer ajuste no backend para redirecionar para o frontend com token na URL

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const authService = {
  loginWithGoogle(): void {
    window.location.href = `${API_BASE_URL}/auth/google/login`
  },

  logout(): void {
    localStorage.removeItem('token')
  },
}
