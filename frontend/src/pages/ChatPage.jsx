import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { chatService } from '../services/chatService'

function ChatPage() {
  const { subject } = useParams()
  const [sessionId, setSessionId] = useState(null)
  const [selectedSubject, setSelectedSubject] = useState(subject || 'Mathematics')
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const bootstrap = async () => {
      try {
        const sessionsResponse = await chatService.getSessions(1, 1, selectedSubject)
        const latestSession = sessionsResponse.sessions?.[0]
        if (latestSession?.session_id) {
          setSessionId(latestSession.session_id)
          const history = await chatService.getSessionMessages(latestSession.session_id)
          setMessages(history.messages || [])
          return
        }

        const created = await chatService.startSession(selectedSubject)
        setSessionId(created.session_id)
        setMessages([
          {
            message_id: `intro-${created.session_id}`,
            role: 'assistant',
            content: `Namaste! Let's learn ${selectedSubject} together. What would you like to start with?`,
          },
        ])
      } catch (bootstrapError) {
        setError(bootstrapError?.response?.data?.detail || 'Unable to load chat')
      }
    }
    bootstrap()
  }, [selectedSubject])

  const handleSend = async () => {
    if (!input.trim() || !sessionId || loading) return
    const message = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { message_id: crypto.randomUUID(), role: 'student', content: message }])
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
    } catch (sendError) {
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

      {/* Messages area */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="mb-4">
          <label className="text-xs text-gray-500 block mb-1">Subject</label>
          <select
            value={selectedSubject}
            onChange={(event) => setSelectedSubject(event.target.value)}
            className="border rounded-lg px-3 py-2 text-sm bg-white"
          >
            {['Mathematics', 'Science', 'English', 'Social Science', 'Hindi'].map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>
        {messages.map((message) => (
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
        ))}
        {error && <p className="text-xs text-red-600 mt-2">{error}</p>}
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
