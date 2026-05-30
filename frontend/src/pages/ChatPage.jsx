import { useCallback, useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { chatService } from '../services/chatService'

const SUBJECTS = ['Mathematics', 'Science', 'English', 'Social Science', 'Hindi']

function ChatPage() {
  const { subject } = useParams()
  const [sessionId, setSessionId] = useState(null)
  const [selectedSubject, setSelectedSubject] = useState(subject || 'Mathematics')
  const [sessions, setSessions] = useState([])
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingSessions, setLoadingSessions] = useState(false)
  const [loadingMessages, setLoadingMessages] = useState(false)
  const [error, setError] = useState('')

  const loadSessions = useCallback(async (subjectName, preferredSessionId = null) => {
    const sessionsResponse = await chatService.getSessions(1, 20, subjectName)
    const fetchedSessions = sessionsResponse.sessions || []
    setSessions(fetchedSessions)
    if (preferredSessionId) {
      const found = fetchedSessions.find((item) => item.session_id === preferredSessionId)
      if (found) return found
    }
    return fetchedSessions[0]
  }, [])

  const loadMessages = async (targetSessionId) => {
    setLoadingMessages(true)
    try {
      const history = await chatService.getSessionMessages(targetSessionId)
      setMessages(history.messages || [])
    } finally {
      setLoadingMessages(false)
    }
  }

  const createSession = useCallback(async (subjectName) => {
    const created = await chatService.startSession(subjectName)
    setSessionId(created.session_id)
    setMessages([
      {
        message_id: `intro-${created.session_id}`,
        role: 'assistant',
        content: `Namaste! Let's learn ${subjectName} together. What would you like to start with?`,
      },
    ])
    await loadSessions(subjectName, created.session_id)
  }, [loadSessions])

  useEffect(() => {
    const bootstrap = async () => {
      try {
        setLoadingSessions(true)
        const latestSession = await loadSessions(selectedSubject)
        if (latestSession?.session_id) {
          setSessionId(latestSession.session_id)
          await loadMessages(latestSession.session_id)
          return
        }
        await createSession(selectedSubject)
      } catch (bootstrapError) {
        setError(bootstrapError?.response?.data?.detail || 'Unable to load chat')
      } finally {
        setLoadingSessions(false)
      }
    }
    bootstrap()
  }, [selectedSubject, loadSessions, createSession])

  const handleSelectSession = async (targetSessionId) => {
    if (!targetSessionId || targetSessionId === sessionId || loadingMessages) return
    setError('')
    try {
      setSessionId(targetSessionId)
      await loadMessages(targetSessionId)
    } catch (loadError) {
      setError(loadError?.response?.data?.detail || 'Unable to load session messages')
    }
  }

  const handleCreateSession = async () => {
    if (loadingSessions || loadingMessages || loading) return
    setError('')
    setLoadingSessions(true)
    try {
      await createSession(selectedSubject)
    } catch (createError) {
      setError(createError?.response?.data?.detail || 'Unable to create new session')
    } finally {
      setLoadingSessions(false)
    }
  }

  const handleSend = async () => {
    if (!input.trim() || !sessionId || loading) return
    const message = input.trim()
    const pendingId = crypto.randomUUID()
    setInput('')
    setMessages((prev) => [...prev, { message_id: pendingId, role: 'student', content: message }])
    setLoading(true)
    setError('')
    try {
      const response = await chatService.sendMessage(sessionId, message, 'English')
      setMessages((prev) => [
        ...prev,
        {
          message_id: response.message_id,
          role: 'assistant',
          content: response.response,
        },
      ])
      await loadSessions(selectedSubject, sessionId)
    } catch (sendError) {
      setMessages((prev) => prev.filter((item) => item.message_id !== pendingId))
      setError(sendError?.response?.data?.detail || 'Unable to send message')
    } finally {
      setLoading(false)
    }
  }

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

      <div className="flex-1 flex overflow-hidden">
        <aside className="hidden md:flex md:w-72 border-r bg-white flex-col">
          <div className="p-4 border-b">
            <label className="text-xs text-gray-500 block mb-1">Subject</label>
            <select
              value={selectedSubject}
              onChange={(event) => setSelectedSubject(event.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm bg-white"
            >
              {SUBJECTS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={handleCreateSession}
              disabled={loadingSessions}
              className="w-full mt-3 bg-orange-500 text-white px-3 py-2 rounded-lg text-sm disabled:opacity-60"
            >
              {loadingSessions ? 'Creating...' : 'New chat'}
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-2">
            {sessions.map((session) => (
              <button
                type="button"
                key={session.session_id}
                onClick={() => handleSelectSession(session.session_id)}
                className={`w-full text-left p-3 rounded-lg mb-2 border ${
                  session.session_id === sessionId ? 'border-orange-300 bg-orange-50' : 'border-gray-200 bg-white'
                }`}
              >
                <p className="text-sm font-medium text-gray-800 truncate">{session.topic || session.subject}</p>
                <p className="text-xs text-gray-500">{session.message_count || 0} messages</p>
              </button>
            ))}
          </div>
        </aside>

        <div className="flex-1 p-4 overflow-y-auto">
          <div className="md:hidden mb-4 flex gap-2">
            <select
              value={selectedSubject}
              onChange={(event) => setSelectedSubject(event.target.value)}
              className="flex-1 border rounded-lg px-3 py-2 text-sm bg-white"
            >
              {SUBJECTS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={handleCreateSession}
              disabled={loadingSessions}
              className="bg-orange-500 text-white px-3 py-2 rounded-lg text-sm disabled:opacity-60"
            >
              New
            </button>
          </div>
          {loadingMessages ? (
            <p className="text-sm text-gray-500">Loading messages...</p>
          ) : (
            messages.map((message) => (
              <div
                key={message.message_id}
                className={`rounded-xl p-3 max-w-sm mb-3 ${
                  message.role === 'student'
                    ? 'bg-white border ml-auto'
                    : 'bg-orange-100'
                }`}
              >
                <p className="text-gray-700 text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
            ))
          )}
          {loading && (
            <div className="rounded-xl p-3 max-w-sm mb-3 bg-orange-100">
              <p className="text-gray-700 text-sm">Thinking...</p>
            </div>
          )}
          {error && <p className="text-xs text-red-600 mt-2">{error}</p>}
        </div>
      </div>

      {/* Input area */}
      <div className="bg-white border-t p-4 flex gap-2">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              event.preventDefault()
              handleSend()
            }
          }}
          className="flex-1 border rounded-lg px-3 py-2 text-sm bg-white"
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm disabled:opacity-60"
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default ChatPage
