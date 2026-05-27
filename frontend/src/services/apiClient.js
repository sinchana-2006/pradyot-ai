/**
 * API client — Axios instance with base URL and auth interceptor.
 * Includes global 401 handling and normalized error shape for UI messages.
 */
import axios from 'axios'

const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/${
    import.meta.env.VITE_API_VERSION || 'v1'
  }`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — attach JWT token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  config._withAuthToken = Boolean(token)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — handle 401 globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && error.config?._withAuthToken) {
      localStorage.removeItem('access_token')
      window.location.href = '/'
    }

    if (!error.response) {
      error.response = {
        status: 0,
        data: { detail: 'Network error. Please check your connection and try again.' },
      }
      return Promise.reject(error)
    }

    if (!error.response.data?.detail) {
      const fallbackDetail = error.message || 'Request failed. Please try again.'
      const existingData =
        typeof error.response.data === 'object' && error.response.data !== null
          ? error.response.data
          : {}
      error.response.data = { ...existingData, detail: fallbackDetail }
    }

    return Promise.reject(error)
  }
)

export default apiClient
