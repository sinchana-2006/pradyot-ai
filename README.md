# Pradyot AI 🎓

**AI-powered personal mentor for Indian students (Class 1–10).**  
Making quality education accessible, personalized, and fun — especially for kids in rural India.

---

## 🌟 Vision

Pradyot AI is a conversational AI tutor that feels like a **patient, knowledgeable friend** — available 24/7, speaking in the student's own language, explaining concepts with Indian cultural examples, and adapting to each student's pace and level.

### Why Pradyot AI?
- ₹500–₹2,000/month saved vs private tutors
- Works on budget Android phones with low bandwidth
- Supports CBSE, ICSE, and State Boards
- Covers Class 1–10 across all subjects
- Regional language support (Hindi, Kannada, Tamil, Telugu, Marathi, Bengali)

---

## 🎯 Target Users

| User | Description |
|------|-------------|
| **Students** (Primary) | Class 1–10, rural/semi-urban India, CBSE/ICSE/State boards |
| **Parents** (Secondary) | Progress dashboards, study time tracking |
| **Teachers** (Future) | Batch-level analytics |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React (Vite), Vercel hosting |
| **Backend** | FastAPI (Python 3.11+), Render hosting |
| **Database** | Supabase (PostgreSQL) |
| **AI** | Groq API (Llama 3), Gemini as fallback |
| **Voice** | Bhashini API (20+ Indian languages) |
| **Auth** | Supabase Auth (email + Google OAuth) |

---

## 📁 Project Structure

```
pradyot-ai/
├── frontend/               # React (Vite) application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Route-level pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client functions
│   │   ├── store/          # State management
│   │   └── utils/          # Helper utilities
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/            # Route handlers
│   │   ├── core/           # Config, security, dependencies
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic (AI, voice, etc.)
│   │   └── db/             # Database connection & queries
│   ├── main.py
│   └── requirements.txt
├── database/               # DB schema and migrations
│   ├── schema.sql          # PostgreSQL DDL
│   └── migrations/         # Version-controlled migrations
├── docs/                   # Project documentation
│   ├── ARCHITECTURE.md
│   ├── API_DESIGN.md
│   ├── DATABASE_SCHEMA.md
│   ├── SETUP_GUIDE.md
│   └── ENV_TEMPLATE.md
├── docker-compose.yml      # Local development stack
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Supabase project
- Groq API key

### 1. Clone the repository
```bash
git clone https://github.com/sinchana-2006/pradyot-ai.git
cd pradyot-ai
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Fill in your API keys
uvicorn main:app --reload
```

### 3. Set up the frontend
```bash
cd frontend
npm install
cp .env.example .env      # Fill in your API URL
npm run dev
```

Visit `http://localhost:5173` for the frontend and `http://localhost:8000/docs` for the API docs.

> 📖 See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed setup instructions.

---

## 📋 Features (Planned)

### Phase 1 — MVP
- [ ] Student onboarding (name, class, board, language)
- [ ] AI chatbot for doubt solving (English + Hindi)
- [ ] Subject-wise conversation routing
- [ ] PYQ practice for CBSE Class 10
- [ ] Session chat history saved to Supabase
- [ ] XP points and basic gamification

### Phase 2 — Enhancement
- [ ] Regional languages via Bhashini API
- [ ] Voice input/output
- [ ] Offline mode (downloadable practice sets)
- [ ] Parent progress dashboard
- [ ] Push notifications & study streaks
- [ ] PWA support

### Phase 3 — Scale
- [ ] WhatsApp bot for rural students
- [ ] School/teacher admin dashboard
- [ ] Batch analytics
- [ ] CSR/NGO partnership portal

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and component overview |
| [API_DESIGN.md](docs/API_DESIGN.md) | REST API contracts |
| [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | PostgreSQL schema design |
| [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Local development setup |
| [ENV_TEMPLATE.md](docs/ENV_TEMPLATE.md) | Environment variables reference |

---

## 🤝 Contributing

This project is currently in active development (Phase 0). Contribution guidelines will be published with the Phase 1 release.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with ❤️ for Bharat's students.*
