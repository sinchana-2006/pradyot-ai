/**
 * Page 2: Chat Interface
 * Connects to FastAPI backend for AI responses.
 * Uses student context from onboarding for personalized tutoring.
 */

import { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { API_URL } from '../config';
import './Chat.css';

function Chat() {
  const location = useLocation();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const student = location.state?.student || JSON.parse(sessionStorage.getItem('pradyot_student') || 'null');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!student) {
      navigate('/');
    }
  }, [student, navigate]);

  const sendMessage = async (e) => {
    e?.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const userMessage = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          student_id: student.id,
          student_context: student,
          history: messages,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to get response');

      setMessages((prev) => [...prev, { role: 'assistant', content: data.message }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Sorry, something went wrong: ${err.message}. Please try again.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!student) return null;

  return (
    <div className="chat-layout">
      <header className="chat-header">
        <button className="back-btn" onClick={() => navigate('/')} aria-label="Back">
          ←
        </button>
        <img src="/pradyot-logo.png" alt="" className="chat-header-logo" />
        <h1 className="chat-header-title">PradyotAI</h1>
        <span className="chat-header-badge">
          {student.name} · Class {student.class_level} · {student.subject}
        </span>
      </header>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-bubble">
            <p>Hi {student.name}, I&apos;m PradyotAI, your personal tutor.</p>
            <p>Ask me anything about {student.subject}. I&apos;ll explain in a way that makes sense for Class {student.class_level}.</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}

        {loading && (
          <div className="message assistant loading">
            <div className="message-content">
              <span className="typing-dots"><span></span><span></span><span></span></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading || !input.trim()} aria-label="Send">
          <svg className="send-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </form>
    </div>
  );
}

export default Chat;
