/**
 * Progress Page — Student progress dashboard.
 * Fetches real data from /api/v1/progress/summary.
 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { studentService } from '../services/studentService'
import { authService } from '../services/authService'

function ProgressPage() {
  const navigate = useNavigate()
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      navigate('/login', { replace: true })
      return
    }

    studentService
      .getProgress()
      .then((data) => setProgress(data))
      .catch((err) => {
        const msg =
          err.response?.data?.detail ||
          'Could not load progress. Please try again.'
        setError(msg)
      })
      .finally(() => setLoading(false))
  }, [navigate])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-400 text-sm">Loading progress…</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-md mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <a href="/chat" className="text-gray-400 hover:text-gray-600 text-sm">
            ← Back
          </a>
          <h1 className="text-2xl font-bold text-gray-800">My Progress 📊</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 mb-4">
            {error}
          </div>
        )}

        {progress && (
          <>
            {/* XP Card */}
            <div className="bg-gradient-to-r from-orange-500 to-orange-400 rounded-2xl p-5 text-white mb-4">
              <p className="text-sm opacity-80">
                Hey, {progress.student_name}! Total XP
              </p>
              <p className="text-4xl font-bold">{progress.xp_total.toLocaleString()}</p>
              <p className="text-sm opacity-80 mt-1">
                {progress.study_streak_days} day streak 🔥 &nbsp;·&nbsp;{' '}
                {progress.xp_this_week} XP this week
              </p>
            </div>

            {/* Badges */}
            <div className="bg-white rounded-2xl p-5 mb-4">
              <h2 className="font-semibold text-gray-700 mb-3">Badges 🏅</h2>
              {progress.badges.length === 0 ? (
                <p className="text-sm text-gray-400">
                  No badges yet — keep learning to earn them!
                </p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {progress.badges.map((b) => (
                    <span
                      key={b}
                      className="bg-orange-50 text-orange-600 text-xs font-medium px-3 py-1 rounded-full border border-orange-200"
                    >
                      {b}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Subject stats */}
            <div className="bg-white rounded-2xl p-5 mb-4">
              <h2 className="font-semibold text-gray-700 mb-3">Subjects</h2>
              {Object.keys(progress.subjects_covered).length === 0 ? (
                <p className="text-sm text-gray-400">
                  Subject stats will appear after your first session.
                </p>
              ) : (
                <div className="space-y-2">
                  {Object.entries(progress.subjects_covered).map(([subject, stats]) => (
                    <div
                      key={subject}
                      className="flex items-center justify-between text-sm"
                    >
                      <span className="text-gray-700 font-medium">{subject}</span>
                      <span className="text-orange-500 font-semibold">
                        {stats.xp || 0} XP
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Weak topics */}
            {progress.weak_topics.length > 0 && (
              <div className="bg-white rounded-2xl p-5">
                <h2 className="font-semibold text-gray-700 mb-3">
                  Topics to Revise 📚
                </h2>
                <div className="flex flex-wrap gap-2">
                  {progress.weak_topics.map((t) => (
                    <span
                      key={t}
                      className="bg-yellow-50 text-yellow-700 text-xs px-3 py-1 rounded-full border border-yellow-200"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default ProgressPage
