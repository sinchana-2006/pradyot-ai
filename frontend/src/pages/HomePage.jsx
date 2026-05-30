import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/authService'

function HomePage() {
  const navigate = useNavigate()
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      if (isLogin) {
        await authService.login(email, password)
        navigate('/chat')
      } else {
        await authService.register(email, password, fullName)
        await authService.login(email, password)
        navigate('/onboarding')
      }
    } catch (submitError) {
      setError(submitError?.response?.data?.detail || 'Unable to continue')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="max-w-2xl text-center w-full">
        <h1 className="text-4xl font-bold text-orange-600 mb-4">
          🎓 Pradyot AI
        </h1>
        <p className="text-xl text-gray-700 mb-2">
          Your personal AI mentor for Class 1–10
        </p>
        <p className="text-gray-500 mb-8">
          Doubt solving • PYQ practice • Regional languages • Available 24/7
        </p>
        <form
          onSubmit={handleSubmit}
          className="max-w-md mx-auto bg-white rounded-2xl shadow-sm p-5 text-left space-y-3"
        >
          {!isLogin && (
            <input
              type="text"
              placeholder="Full name"
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
              required
            />
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm"
            required
          />
          {error && <p className="text-xs text-red-600">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors disabled:opacity-60"
          >
            {loading ? 'Please wait...' : isLogin ? 'Login' : 'Create Account'}
          </button>
          <button
            type="button"
            className="text-sm text-orange-600 underline"
            onClick={() => setIsLogin((value) => !value)}
          >
            {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default HomePage
