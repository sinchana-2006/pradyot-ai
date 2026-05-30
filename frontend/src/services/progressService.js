import apiClient from './apiClient'

export const progressService = {
  async getSummary() {
    const response = await apiClient.get('/progress/summary')
    return response.data
  },
}
