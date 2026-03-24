/**
 * Progress Page — Student progress dashboard
 * TODO (Phase 1): Fetch from /api/v1/progress/summary and display real data
 */
function ProgressPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-md mx-auto">
        <a href="/" className="text-gray-400 hover:text-gray-600 text-sm">← Back</a>
        <h1 className="text-2xl font-bold text-gray-800 mt-4 mb-6">My Progress 📊</h1>

        {/* XP Card */}
        <div className="bg-gradient-to-r from-orange-500 to-orange-400 rounded-2xl p-5 text-white mb-4">
          <p className="text-sm opacity-80">Total XP</p>
          <p className="text-4xl font-bold">—</p>
          <p className="text-sm opacity-80 mt-1">0 day streak 🔥</p>
        </div>

        {/* Badges */}
        <div className="bg-white rounded-2xl p-5 mb-4">
          <h2 className="font-semibold text-gray-700 mb-3">Badges</h2>
          <p className="text-sm text-gray-400">No badges yet — start learning to earn them!</p>
        </div>

        {/* Subject stats */}
        <div className="bg-white rounded-2xl p-5">
          <h2 className="font-semibold text-gray-700 mb-3">Subjects</h2>
          <p className="text-sm text-gray-400">
            Subject-wise stats will appear after your first session.
          </p>
        </div>

        <p className="text-center text-xs text-gray-400 mt-6">
          Full progress tracking coming in Phase 1
        </p>
      </div>
    </div>
  )
}

export default ProgressPage
