/**
 * Student service — profile creation and retrieval
 */
import apiClient from './apiClient'

export const studentService = {
  async createOrUpdateProfile(profileData) {
    const response = await apiClient.post('/students/profile', profileData)
    return response.data
  },

  async getProfile() {
    const response = await apiClient.get('/students/profile')
    return response.data
  },

  async getProgress() {
    const response = await apiClient.get('/progress/summary')
    return response.data
  },
}
