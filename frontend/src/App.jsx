import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage.jsx'
import ChatPage from './pages/ChatPage.jsx'
import OnboardingPage from './pages/OnboardingPage.jsx'
import ProgressPage from './pages/ProgressPage.jsx'
import NotFoundPage from './pages/NotFoundPage.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
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
