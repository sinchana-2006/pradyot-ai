import { useEffect, useState } from 'react'
import { progressService } from '../services/progressService'

function ProgressPage() {
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    progressService
      .getSummary()
      .then((data) => setSummary(data))
      .catch((loadError) => {
        setError(loadError?.response?.data?.detail || 'Unable to load progress')
      })
  }, [])

  const subjects = Object.entries(summary?.subjects_covered || {})

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-md mx-auto">
        <a href="/" className="text-gray-400 hover:text-gray-600 text-sm">← Back</a>
        <h1 className="text-2xl font-bold text-gray-800 mt-4 mb-6">My Progress 📊</h1>

        {/* XP Card */}
        <div className="bg-gradient-to-r from-orange-500 to-orange-400 rounded-2xl p-5 text-white mb-4">
          <p className="text-sm opacity-80">Total XP</p>
          <p className="text-4xl font-bold">{summary?.xp_total ?? '—'}</p>
          <p className="text-sm opacity-80 mt-1">
            {summary?.study_streak_days ?? 0} day streak 🔥
          </p>
        </div>

        {/* Badges */}
        <div className="bg-white rounded-2xl p-5 mb-4">
          <h2 className="font-semibold text-gray-700 mb-3">Badges</h2>
          {summary?.badges?.length ? (
            <div className="flex flex-wrap gap-2">
              {summary.badges.map((badge) => (
                <span
                  key={badge}
                  className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full"
                >
                  {badge}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400">No badges yet — start learning to earn them!</p>
          )}
        </div>

        {/* Subject stats */}
        <div className="bg-white rounded-2xl p-5">
          <h2 className="font-semibold text-gray-700 mb-3">Subjects</h2>
          {subjects.length ? (
            <div className="space-y-2">
              {subjects.map(([name, stat]) => (
                <div key={name} className="text-sm text-gray-700">
                  <p className="font-medium">{name}</p>
                  <p className="text-xs text-gray-500">
                    Sessions: {stat.sessions} • XP: {stat.xp} • Strength: {stat.strength}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400">
              Subject-wise stats will appear after your first session.
            </p>
          )}
        </div>
        {error && <p className="text-center text-xs text-red-600 mt-6">{error}</p>}
      </div>
    </div>
  )
}

export default ProgressPage
