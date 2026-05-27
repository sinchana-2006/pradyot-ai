import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/authService'
import useAppStore from '../store/useAppStore'

function LoginPage() {
  const navigate = useNavigate()
  const setUser = useAppStore((s) => s.setUser)

  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function bootstrapOAuthSession() {
      const appUser = authService.getUserFromAppToken()
      if (appUser?.id) {
        setUser(appUser)
        navigate('/chat', { replace: true })
        return
      }

      const supabaseSession = await authService.getSupabaseSession()
      const oauthToken = supabaseSession?.access_token
      if (!oauthToken) return

      try {
        const data = await authService.exchangeGoogleAccessToken(oauthToken)
        setUser({ id: data.user_id, email: supabaseSession.user?.email || null })
        navigate('/chat', { replace: true })
      } catch {
        // Keep user on login page and show manual action prompt.
        setError('Google sign-in completed, but token exchange failed. Please try again.')
      }
    }
    bootstrapOAuthSession()
  }, [navigate, setUser])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (mode === 'login') {
        const data = await authService.login(email, password)
        setUser({ id: data.user_id, email })
        navigate('/chat')
      } else {
        const data = await authService.register(email, password, fullName)
        localStorage.setItem('access_token', data.access_token)
        setUser({ id: data.user_id, email })
        navigate('/onboarding')
      }
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (mode === 'login' ? 'Login failed. Check your credentials.' : 'Registration failed. Try again.')
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  async function handleGoogleLogin() {
    setError('')
    setLoading(true)
    try {
      await authService.signInWithGoogle(`${window.location.origin}/login`)
    } catch (err) {
      setError(err.message || 'Google login failed.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">
          {mode === 'login' ? 'Welcome back! 🙏' : 'Create an account 🎓'}
        </h1>
        <p className="text-gray-500 text-sm mb-6">
          {mode === 'login'
            ? 'Sign in to continue your learning journey'
            : 'Join thousands of students learning with Pradyot AI'}
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                type="text"
                placeholder="e.g. Arjun Sharma"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              placeholder="Min 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading
              ? mode === 'login'
                ? 'Signing in…'
                : 'Creating account…'
              : mode === 'login'
              ? 'Sign In'
              : 'Create Account'}
          </button>
        </form>

        <div className="mt-4">
          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            Continue with Google
          </button>
        </div>

        <p className="text-center text-sm text-gray-500 mt-4">
          {mode === 'login' ? (
            <>
              Don&apos;t have an account?{' '}
              <button
                onClick={() => { setMode('register'); setError('') }}
                className="text-orange-500 font-medium hover:underline"
              >
                Sign up
              </button>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <button
                onClick={() => { setMode('login'); setError('') }}
                className="text-orange-500 font-medium hover:underline"
              >
                Sign in
              </button>
            </>
          )}
        </p>
      </div>
    </div>
  )
}

export default LoginPage
