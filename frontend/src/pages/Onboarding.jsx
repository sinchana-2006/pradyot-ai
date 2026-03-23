/**
 * Page 1: Student Onboarding Form
 * Collects name, class, board, subject, and preferred language.
 * Stores data in sessionStorage and passes to Chat via navigation state.
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config';
import './Onboarding.css';

const BOARDS = ['CBSE', 'ICSE', 'State Board'];
const SUBJECTS = ['Mathematics', 'Science', 'English', 'Social Studies', 'Hindi', 'Other'];
const LANGUAGES = ['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Bengali', 'Marathi', 'Other'];

function Onboarding() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    name: '',
    class_level: 1,
    board: 'CBSE',
    subject: 'Mathematics',
    preferred_language: 'English',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === 'class_level' ? parseInt(value, 10) : value,
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) {
      setError('Please enter your name');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_URL}/api/onboard`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Onboarding failed');

      const studentWithId = data.student;
      sessionStorage.setItem('pradyot_student', JSON.stringify(studentWithId));
      navigate('/chat', { state: { student: studentWithId } });
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding">
      <header className="onboarding-header">
        <img src="/pradyot-logo.png" alt="PradyotAI" className="onboarding-logo" />
        <h1 className="onboarding-title">PradyotAI</h1>
        <p className="onboarding-subtitle">Your Personal AI Tutor</p>
      </header>

      <div className="onboarding-card">
        <form className="onboarding-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Your Name</label>
            <input
              id="name"
              name="name"
              type="text"
              placeholder="Enter your name"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="class_level">Class (1-10)</label>
            <select
              id="class_level"
              name="class_level"
              value={form.class_level}
              onChange={handleChange}
            >
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((c) => (
                <option key={c} value={c}>Class {c}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="board">Board</label>
            <select id="board" name="board" value={form.board} onChange={handleChange}>
              {BOARDS.map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="subject">Subject</label>
            <select id="subject" name="subject" value={form.subject} onChange={handleChange}>
              {SUBJECTS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="preferred_language">Preferred Language</label>
            <select
              id="preferred_language"
              name="preferred_language"
              value={form.preferred_language}
              onChange={handleChange}
            >
              {LANGUAGES.map((l) => (
                <option key={l} value={l}>{l}</option>
              ))}
            </select>
          </div>

          {error && <p className="form-error">{error}</p>}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Getting ready...' : 'Start Learning →'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Onboarding;
