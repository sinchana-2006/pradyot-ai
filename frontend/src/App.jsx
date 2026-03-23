/**
 * PradyotAI - Main App Component
 * Routes: / (Onboarding) -> /chat (Chat Interface)
 */

import { Routes, Route } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Chat from './pages/Chat';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Onboarding />} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
  );
}

export default App;
