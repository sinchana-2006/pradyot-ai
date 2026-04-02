/**
 * Chat Page — Main AI tutor chat interface.
 * Creates a session on mount and sends messages to the AI tutor.
 */
import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { chatService } from '../services/chatService'
import { authService } from '../services/authService'
import useAppStore from '../store/useAppStore'

const SUBJECTS = [
  'Mathematics', 'Science', 'English', 'Social Studies',
  'Hindi', 'Sanskrit', 'History', 'Geography',
]

function MessageBubble({ message }) {
  const isStudent = message.role === 'student'
  return (
    <div className={`flex ${isStudent ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isStudent
            ? 'bg-orange-500 text-white rounded-br-sm'
            : 'bg-white border border-gray-100 text-gray-800 rounded-bl-sm shadow-sm'
        }`}
      >
        {!isStudent && (
          <p className="text-xs font-semibold text-orange-500 mb-1">🎓 Pradyot</p>
        )}
        <p className="whitespace-pre-wrap">{message.content}</p>
        {message.xp_earned > 0 && (
          <p className="text-xs mt-1 text-orange-200">+{message.xp_earned} XP</p>
        )}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex justify-start mb-3">
      <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm shadow-sm px-4 py-3">
        <p className="text-xs font-semibold text-orange-500 mb-1">🎓 Pradyot</p>
        <div className="flex gap-1 items-center h-4">
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:0ms]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:150ms]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:300ms]" />
        </div>
      </div>
    </div>
  )
}

function ChatPage() {
  const { subject: urlSubject } = useParams()
  const navigate = useNavigate()

  const { messages, addMessage, clearMessages, currentSessionId, setCurrentSessionId, xpTotal, addXP } =
    useAppStore()

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionReady, setSessionReady] = useState(false)
  const [selectedSubject, setSelectedSubject] = useState(urlSubject || '')
  const [error, setError] = useState('')
  const bottomRef = useRef(null)

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authService.isAuthenticated()) {
      navigate('/login', { replace: true })
    }
  }, [navigate])

  // Start a session when a subject is selected
  useEffect(() => {
    if (!selectedSubject) return
    if (currentSessionId) {
      setSessionReady(true)
      return
    }

    clearMessages()
    setSessionReady(false)

    chatService
      .startSession(selectedSubject)
      .then((data) => {
        setCurrentSessionId(data.session_id)
        setSessionReady(true)
        addMessage({
          role: 'assistant',
          content: `👋 Namaste! I'm Pradyot, your AI mentor. Let's study ${selectedSubject} today! What would you like to learn or ask?`,
          xp_earned: 0,
        })
      })
      .catch(() => {
        setError('Could not start a session. Make sure you have completed onboarding.')
      })
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedSubject])

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function handleSend(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading || !currentSessionId) return

    setInput('')
    setError('')
    addMessage({ role: 'student', content: text, xp_earned: 0 })
    setLoading(true)

    try {
      const data = await chatService.sendMessage(currentSessionId, text)
      addMessage({
        role: 'assistant',
        content: data.response + (data.follow_up_question ? `\n\n${data.follow_up_question}` : ''),
        xp_earned: data.xp_earned || 0,
      })
      if (data.xp_earned) addXP(data.xp_earned)
    } catch (err) {
      const msg =
        err.response?.data?.detail || 'Something went wrong. Please try again.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  function handleLogout() {
    authService.logout()
  }

  // Subject selection screen
  if (!selectedSubject) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <header className="bg-white border-b px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/" className="text-gray-400 hover:text-gray-600">←</a>
            <div>
              <h1 className="font-semibold text-gray-800">Pradyot AI</h1>
              <p className="text-xs text-gray-500">Choose a subject</p>
            </div>
          </div>
          <button onClick={handleLogout} className="text-xs text-gray-400 hover:text-gray-600">
            Logout
          </button>
        </header>

        <div className="flex-1 p-6">
          <p className="text-gray-600 text-sm mb-4">What would you like to study today?</p>
          <div className="grid grid-cols-2 gap-3">
            {SUBJECTS.map((s) => (
              <button
                key={s}
                onClick={() => setSelectedSubject(s)}
                className="bg-white border border-gray-200 rounded-xl p-4 text-left hover:border-orange-400 hover:shadow-sm transition-all"
              >
                <span className="text-sm font-medium text-gray-700">{s}</span>
              </button>
            ))}
          </div>

          <div className="mt-6 flex gap-2">
            <a
              href="/progress"
              className="text-sm text-orange-500 hover:underline"
            >
              📊 View Progress
            </a>
            <span className="text-gray-300">•</span>
            <span className="text-sm text-gray-500">⚡ {xpTotal} XP</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              setSelectedSubject('')
              setCurrentSessionId(null)
              clearMessages()
            }}
            className="text-gray-400 hover:text-gray-600"
          >
            ←
          </button>
          <div>
            <h1 className="font-semibold text-gray-800">Pradyot AI — {selectedSubject}</h1>
            <p className="text-xs text-gray-500">
              {sessionReady ? 'Online' : 'Starting session…'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium text-orange-500">⚡ {xpTotal} XP</span>
          <button onClick={handleLogout} className="text-xs text-gray-400 hover:text-gray-600">
            Logout
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto">
        {!sessionReady && !error && (
          <p className="text-center text-xs text-gray-400 mt-4">Starting your session…</p>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 mb-4">
            {error}
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="bg-white border-t p-4 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={sessionReady ? 'Ask me anything…' : 'Starting session…'}
          disabled={!sessionReady || loading}
          className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:bg-gray-50 disabled:text-gray-400"
        />
        <button
          type="submit"
          disabled={!sessionReady || loading || !input.trim()}
          className="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatPage
