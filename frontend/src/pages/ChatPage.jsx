/**
 * Chat Page — Main AI tutor chat interface
 * TODO (Phase 1): Implement full chat UI with message list, input, and AI responses
 */
function ChatPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-4 py-3 flex items-center gap-3">
        <a href="/" className="text-gray-400 hover:text-gray-600">←</a>
        <div>
          <h1 className="font-semibold text-gray-800">Pradyot AI</h1>
          <p className="text-xs text-gray-500">Your AI mentor</p>
        </div>
      </header>

      {/* Messages area */}
      <div className="flex-1 p-4 overflow-y-auto">
        {/* Placeholder message */}
        <div className="bg-orange-100 rounded-xl p-4 max-w-sm">
          <p className="text-gray-700 text-sm">
            👋 Namaste! I'm Pradyot, your AI mentor. Which subject would you
            like to study today?
          </p>
        </div>
        <p className="text-center text-xs text-gray-400 mt-8">
          Full chat implementation coming in Phase 1
        </p>
      </div>

      {/* Input area */}
      <div className="bg-white border-t p-4 flex gap-2">
        <input
          type="text"
          placeholder="Ask me anything..."
          disabled
          className="flex-1 border rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
        />
        <button
          disabled
          className="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm opacity-50 cursor-not-allowed"
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default ChatPage
