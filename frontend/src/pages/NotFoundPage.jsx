/**
 * 404 Not Found Page
 */
function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
      <p className="text-6xl mb-4">🤔</p>
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Page Not Found</h1>
      <p className="text-gray-500 mb-6">
        Hmm, this page doesn&apos;t exist. Let&apos;s get you back on track!
      </p>
      <a
        href="/"
        className="bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
      >
        Go Home
      </a>
    </div>
  )
}

export default NotFoundPage
