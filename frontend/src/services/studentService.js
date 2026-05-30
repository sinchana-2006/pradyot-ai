import apiClient from './apiClient'

export const studentService = {
  async saveProfile(payload) {
    const response = await apiClient.post('/students/profile', payload)
    return response.data
  },

  async getProfile() {
    const response = await apiClient.get('/students/profile')
    return response.data
  },
}
