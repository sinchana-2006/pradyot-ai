import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import HomePage from './pages/HomePage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import ChatPage from './pages/ChatPage.jsx'
import OnboardingPage from './pages/OnboardingPage.jsx'
import ProgressPage from './pages/ProgressPage.jsx'
import NotFoundPage from './pages/NotFoundPage.jsx'
import { authService } from './services/authService'
import useAppStore from './store/useAppStore'

function App() {
  const setUser = useAppStore((s) => s.setUser)
  const clearUser = useAppStore((s) => s.clearUser)

  useEffect(() => {
    async function restoreSession() {
      const userFromToken = authService.getUserFromAppToken()
      if (userFromToken?.id) {
        setUser(userFromToken)
        return
      }

      const supabaseSession = await authService.getSupabaseSession()
      const oauthToken = supabaseSession?.access_token
      if (!oauthToken) {
        clearUser()
        return
      }

      try {
        const data = await authService.exchangeGoogleAccessToken(oauthToken)
        setUser({ id: data.user_id, email: supabaseSession.user?.email || null })
      } catch {
        clearUser()
      }
    }

    restoreSession()
  }, [clearUser, setUser])

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/chat/:subject" element={<ChatPage />} />
        <Route path="/progress" element={<ProgressPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
