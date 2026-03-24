/**
 * Chat service — session management and messaging
 * TODO (Phase 1): Implement actual API calls
 */
import apiClient from './apiClient'

export const chatService = {
  async startSession(subject, topic = null) {
    const response = await apiClient.post('/chat/session', { subject, topic })
    return response.data
  },

  async sendMessage(sessionId, message, language = 'English') {
    const response = await apiClient.post('/chat/message', {
      session_id: sessionId,
      message,
      language,
    })
    return response.data
  },

  async getSessions(page = 1, limit = 10, subject = null) {
    const params = { page, limit }
    if (subject) params.subject = subject
    const response = await apiClient.get('/chat/sessions', { params })
    return response.data
  },

  async getSessionMessages(sessionId) {
    const response = await apiClient.get(`/chat/session/${sessionId}/messages`)
    return response.data
  },
}
