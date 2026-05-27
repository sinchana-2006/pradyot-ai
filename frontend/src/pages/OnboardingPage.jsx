/**
 * Onboarding Page — Student profile creation.
 * Saves to backend /api/v1/students/profile and redirects to /chat.
 */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { studentService } from '../services/studentService'
import useAppStore from '../store/useAppStore'

const LANGUAGES = ['English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Bengali']
const BOARDS = ['CBSE', 'ICSE', 'State Board']

function OnboardingPage() {
  const navigate = useNavigate()
  const setProfile = useAppStore((s) => s.setProfile)

  const [fullName, setFullName] = useState('')
  const [classLevel, setClassLevel] = useState('')
  const [board, setBoard] = useState('CBSE')
  const [language, setLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const profile = await studentService.createOrUpdateProfile({
        full_name: fullName,
        class_level: parseInt(classLevel, 10),
        board,
        preferred_language: language,
        subjects: [],
      })
      setProfile(profile)
      navigate('/chat')
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        'Failed to save profile. Please try again.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome! 🙏</h1>
        <p className="text-gray-500 mb-6 text-sm">
          Tell me a bit about yourself so I can personalize your learning
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Name
            </label>
            <input
              type="text"
              placeholder="e.g. Arjun"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Class
            </label>
            <select
              value={classLevel}
              onChange={(e) => setClassLevel(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            >
              <option value="">Select class</option>
              {[...Array(10)].map((_, i) => (
                <option key={i + 1} value={i + 1}>
                  Class {i + 1}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Board
            </label>
            <select
              value={board}
              onChange={(e) => setBoard(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            >
              {BOARDS.map((b) => (
                <option key={b}>{b}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            >
              {LANGUAGES.map((l) => (
                <option key={l}>{l}</option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? 'Saving…' : 'Start Learning →'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default OnboardingPage
