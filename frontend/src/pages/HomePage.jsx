/**
 * Home Page — Landing page for Pradyot AI
 * TODO (Phase 1): Add auth check and redirect to /chat if logged in
 */
function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold text-orange-600 mb-4">
          🎓 Pradyot AI
        </h1>
        <p className="text-xl text-gray-700 mb-2">
          Your personal AI mentor for Class 1–10
        </p>
        <p className="text-gray-500 mb-8">
          Doubt solving • PYQ practice • Regional languages • Available 24/7
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/onboarding"
            className="bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
          >
            Get Started
          </a>
          <a
            href="/chat"
            className="border border-orange-500 text-orange-500 px-6 py-3 rounded-lg font-semibold hover:bg-orange-50 transition-colors"
          >
            Start Learning
          </a>
        </div>
        <p className="mt-8 text-sm text-gray-400">
          Phase 0 — Foundation setup complete. Full features coming in Phase 1.
        </p>
      </div>
    </div>
  )
}

export default HomePage
