/**
 * API client — Axios instance with base URL and auth interceptor.
 * TODO (Phase 1): Add token refresh logic and error handling.
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
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — handle 401 globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default apiClient
