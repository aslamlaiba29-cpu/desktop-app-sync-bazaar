# AI Study Buddy 🎓

> A smart, AI-powered study assistant that combines the Pomodoro Technique, Active Recall quizzes, and an intelligent tutoring chatbot to help students study more effectively.

![CI](https://github.com/zahra227ng/final-project/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

AI Study Buddy is a full-stack web application built as a final project for a Software Construction & Development university course. It helps students manage their study sessions, test their knowledge through AI-generated quizzes, and get instant explanations via a built-in chatbot — all in one platform.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🍅 Pomodoro Timer | 25-minute focused study sessions with automatic logging |
| 🧠 Quiz Engine | AI-generated questions based on subject input for active recall |
| 🤖 AI Chatbot | Ask questions and receive simplified explanations (Feynman Technique) |
| 📊 Analytics Dashboard | Track study hours, quiz scores, and daily streaks |
| 🔐 Authentication | Secure JWT-based login and registration with bcrypt hashing |
| 📝 Task Planner | Create, update, and track study tasks with Pomodoro estimates |

---

## 🏗️ Architecture

```
3-Tier Architecture:
┌─────────────────────────────────────┐
│  Frontend  │  HTML + CSS + JS (SPA) │
├─────────────────────────────────────┤
│  Backend   │  Python Flask REST API │
├─────────────────────────────────────┤
│  Database  │  SQLite + SQLAlchemy   │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
final-project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── planner.py
│   │   │   ├── quiz.py
│   │   │   └── ai.py
│   │   └── services/
│   │       └── ai_engine.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_planner.py
│   │   ├── test_quiz.py
│   │   └── test_ai.py
│   └── run.py
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── docs/
│   ├── final_report.md
│   ├── sprint_plan.md
│   ├── peer_review_log.md
│   ├── agile_scrum_details.md
│   └── testing_report.md
├── legacy_demo/
│   ├── spaghetti_app_bad.py
│   └── refactoring_explanation.md
├── microservices/
├── .github/workflows/ci.yml
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/zahra227ng/final-project.git
cd final-project
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the backend server
```bash
cd backend
python run.py
```

The Flask server will start at `http://localhost:5000`. The SQLite database is created automatically on first run.

### Step 4 — Open the frontend
Open `frontend/index.html` in your browser, or serve it with:
```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v --tb=short
```

Test coverage includes:
- `test_auth.py` — user registration, login, JWT validation
- `test_quiz.py` — quiz generation, submission, scoring
- `test_planner.py` — task CRUD operations
- `test_ai.py` — chatbot responses and recommendation logic

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and receive JWT token |
| GET | `/api/auth/profile` | Get user profile and streak |

### Tasks / Planner
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks for logged-in user |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/<id>` | Update task status or details |
| DELETE | `/api/tasks/<id>` | Delete a task |

### Quiz
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/quiz/generate` | Generate quiz questions by subject |
| POST | `/api/quiz/submit` | Submit answers and save score |

### AI Assistant
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat` | Send a question to the chatbot |
| GET | `/api/ai/recommendations` | Get personalized study suggestions |

---

## 🗄️ Database Schema

```
Users       — id, username, email, password_hash, streak, last_active, daily_goal_minutes
Tasks       — id, user_id (FK), title, description, due_date, subject, status, pomodoros
Quizzes     — id, user_id (FK), title, subject, questions (JSON), score, total_questions
StudyLogs   — id, user_id (FK), subject, duration_minutes, activity_type, date
```

---

## ⚙️ CI/CD Pipeline

This project uses **GitHub Actions** for automated testing on every push to `main`.

Pipeline steps:
1. Install Python dependencies from `requirements.txt`
2. Run `pytest` across all test modules
3. Block merge if any test fails

See `.github/workflows/ci.yml` for the full configuration.

---

## 🔄 Agile Development Process

This project was developed using the **Agile Incremental Model** across 3 sprints:

| Sprint | Duration | Key Deliverables |
|--------|----------|-----------------|
| Sprint 1 | Weeks 1–2 | Authentication, database models, project setup |
| Sprint 2 | Weeks 3–4 | Quiz engine, Pomodoro timer, task planner |
| Sprint 3 | Weeks 5–6 | AI chatbot, analytics dashboard, testing, CI/CD |

Full sprint details and retrospectives are documented in [`docs/sprint_plan.md`](docs/sprint_plan.md).

---

## 📐 Software Engineering Practices

- **Refactoring** — Legacy spaghetti code in `legacy_demo/` refactored into modular, layered architecture. See [`legacy_demo/refactoring_explanation.md`](legacy_demo/refactoring_explanation.md).
- **Version Control** — Feature branches, meaningful commit messages, `.gitignore` configured.
- **Peer Reviews** — Code walkthroughs and inspection logs documented in [`docs/peer_review_log.md`](docs/peer_review_log.md).
- **Exception Handling** — Database errors, JWT failures, and invalid inputs all return structured JSON error responses.
- **Lehman's Laws** — Justification for system evolution documented in the final report.

---

## 🛠️ Technologies Used

- **Backend:** Python 3.13, Flask, SQLAlchemy, PyJWT, bcrypt
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (SPA)
- **Database:** SQLite
- **Testing:** PyTest
- **CI/CD:** GitHub Actions
- **Version Control:** Git / GitHub

---

## 🔭 Future Improvements

- Migrate database to PostgreSQL for production use
- Deploy to cloud (Render / Railway / AWS)
- Add real-time collaborative study rooms
- Integrate a live LLM API (OpenAI / Gemini) for the chatbot
- Build a mobile app version (React Native)
- Add Docker + Kubernetes support

---

## 👥 Team

| Name | Role |
|------|------|
| Zahra | Project Manager & Backend Developer |
| *(Team Member 2)* | Frontend Developer |
| *(Team Member 3)* | Database Designer & Tester |

---

## 📄 Documentation

All project documentation is in the [`docs/`](docs/) folder:

- [`final_report.md`](docs/final_report.md) — Full software engineering report
- [`sprint_plan.md`](docs/sprint_plan.md) — Agile sprint breakdown
- [`peer_review_log.md`](docs/peer_review_log.md) — Code inspection records
- [`testing_report.md`](docs/testing_report.md) — Test cases and results
- [`agile_scrum_details.md`](docs/agile_scrum_details.md) — Scrum process details

---

*Built for Software Construction & Development — University Course Project*
