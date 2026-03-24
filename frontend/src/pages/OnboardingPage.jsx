/**
 * Onboarding Page — Student profile creation
 * TODO (Phase 1): Connect to backend /api/v1/students/profile endpoint
 */
function OnboardingPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome! 🙏</h1>
        <p className="text-gray-500 mb-6 text-sm">
          Tell me a bit about yourself so I can personalize your learning
        </p>

        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Name
            </label>
            <input
              type="text"
              placeholder="e.g. Arjun"
              disabled
              className="w-full border rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Class
            </label>
            <select
              disabled
              className="w-full border rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
            >
              <option>Select class</option>
              {[...Array(10)].map((_, i) => (
                <option key={i + 1}>Class {i + 1}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Board
            </label>
            <select
              disabled
              className="w-full border rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
            >
              <option>CBSE</option>
              <option>ICSE</option>
              <option>State Board</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Language
            </label>
            <select
              disabled
              className="w-full border rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
            >
              <option>English</option>
              <option>Hindi</option>
            </select>
          </div>

          <button
            type="button"
            disabled
            className="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold opacity-50 cursor-not-allowed"
          >
            Start Learning →
          </button>
        </form>

        <p className="text-center text-xs text-gray-400 mt-4">
          Onboarding form — full implementation in Phase 1
        </p>
      </div>
    </div>
  )
}

export default OnboardingPage
