import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { studentService } from '../services/studentService'

function OnboardingPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    full_name: '',
    class_level: 5,
    board: 'CBSE',
    preferred_language: 'English',
    subjects: [],
    state: '',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    studentService
      .getProfile()
      .then((profile) => {
        setForm((prev) => ({
          ...prev,
          full_name: profile.full_name || prev.full_name,
          class_level: profile.class_level || prev.class_level,
          board: profile.board || prev.board,
          preferred_language: profile.preferred_language || prev.preferred_language,
          subjects: profile.subjects || [],
        }))
      })
      .catch(() => {})
  }, [])

  const updateField = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const handleSubjectsChange = (event) => {
    const values = event.target.value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean)
    updateField('subjects', values)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await studentService.saveProfile(form)
      navigate('/chat')
    } catch (submitError) {
      setError(submitError?.response?.data?.detail || 'Unable to save profile')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-b from-orange-50 to-white">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome! 🙏</h1>
        <p className="text-gray-500 mb-6 text-sm">
          Tell me a bit about yourself so I can personalize your learning
        </p>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Name
            </label>
            <input
              type="text"
              placeholder="e.g. Arjun"
              value={form.full_name}
              onChange={(event) => updateField('full_name', event.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Class
            </label>
            <select
              value={form.class_level}
              onChange={(event) => updateField('class_level', Number(event.target.value))}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            >
              <option value="">Select class</option>
              {[...Array(10)].map((_, i) => (
                <option key={i + 1} value={i + 1}>
                  Class {i + 1}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Board
            </label>
            <select
              value={form.board}
              onChange={(event) => updateField('board', event.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            >
              <option>CBSE</option>
              <option>ICSE</option>
              <option>State Board</option>
              <option>Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Language
            </label>
            <select
              value={form.preferred_language}
              onChange={(event) => updateField('preferred_language', event.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            >
              <option>English</option>
              <option>Hindi</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Subjects (comma separated)
            </label>
            <input
              type="text"
              placeholder="Mathematics, Science"
              value={form.subjects.join(', ')}
              onChange={handleSubjectsChange}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            />
          </div>

          {error && <p className="text-xs text-red-600">{error}</p>}

          <button
            type="submit"
            disabled={saving}
            className="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold disabled:opacity-60"
          >
            {saving ? 'Saving...' : 'Start Learning →'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default OnboardingPage
