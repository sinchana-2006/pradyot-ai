/**
 * Auth service — login, register, logout
 * TODO (Phase 1): Implement actual API calls
 */
import apiClient from './apiClient'

export const authService = {
  async register(email, password, fullName) {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    })
    return response.data
  },

  async login(email, password) {
    const response = await apiClient.post('/auth/login', { email, password })
    const { access_token } = response.data
    localStorage.setItem('access_token', access_token)
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
    window.location.href = '/'
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },
}
