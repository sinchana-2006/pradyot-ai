/**
 * Auth service — email/password + Google OAuth exchange.
 */
import apiClient from './apiClient'
import { supabaseClient } from './supabaseClient'

function decodeJwt(token) {
  try {
    const [, payload] = token.split('.')
    if (!payload) return null
    const parsed = JSON.parse(window.atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
    if (parsed.exp && Date.now() >= parsed.exp * 1000) return null
    return parsed
  } catch {
    return null
  }
}

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

  async exchangeGoogleAccessToken(accessToken) {
    const response = await apiClient.post('/auth/google/exchange', {
      access_token: accessToken,
    })
    const { access_token } = response.data
    localStorage.setItem('access_token', access_token)
    return response.data
  },

  async signInWithGoogle(redirectTo) {
    if (!supabaseClient) {
      throw new Error('Supabase client is not configured.')
    }
    const { data, error } = await supabaseClient.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo },
    })
    if (error) throw error
    return data
  },

  async getSupabaseSession() {
    if (!supabaseClient) return null
    const { data, error } = await supabaseClient.auth.getSession()
    if (error) return null
    return data.session
  },

  getUserFromAppToken() {
    const token = localStorage.getItem('access_token')
    if (!token) return null
    const payload = decodeJwt(token)
    if (!payload?.sub) return null
    return { id: payload.sub, email: payload.email || null }
  },

  logout() {
    localStorage.removeItem('access_token')
    if (supabaseClient) {
      supabaseClient.auth.signOut().catch(() => {})
    }
    window.location.href = '/'
  },

  isAuthenticated() {
    return !!this.getUserFromAppToken()
  },
}
