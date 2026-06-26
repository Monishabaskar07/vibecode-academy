# 🚀 VibeCode Academy

An AI-powered learning platform built as the **Google AI Agents Capstone Project**. VibeCode Academy demonstrates how multiple AI agents can collaborate to help learners manage coding sessions, securely store progress, benchmark performance, and update learning challenges.

---

## 📖 Overview

VibeCode Academy combines a modern React frontend with a FastAPI backend and a **5-Agent pipeline** powered by **Google ADK**. Each agent performs a specialized task, creating a modular and extensible AI workflow.

---

## ✨ Features

- 📚 Create and manage learning sessions
- 🔐 Secure Vault for storing user progress
- 📊 Run performance benchmarks
- 🎯 AI-assisted challenge updates
- 🤖 Multi-agent orchestration using Google ADK
- 🌐 Fully deployed on Render

---

## 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React + Vite |
| Backend | FastAPI |
| AI Framework | Google Agent Development Kit (ADK) |
| Database | JSON-based storage |
| Deployment | Render |
| Version Control | Git & GitHub |

---

# 🏗 System Architecture

```
                         USER
                           │
                           ▼
        +----------------------------------+
        |     Frontend (React + Vite)      |
        |      VibeCode Academy UI         |
        +----------------------------------+
                           │
                           ▼
        +----------------------------------+
        |      Backend (FastAPI API)       |
        +----------------------------------+
               │                     │
               │                     ▼
               │          +----------------------+
               │          | JSON Database        |
               │          | sessions.json        |
               │          | vault.json           |
               │          | benchmarks.json      |
               │          | challenges.json      |
               │          +----------------------+
               │
               ▼
        +----------------------------------------------+
        |      Google ADK - 5 Agent Pipeline           |
        +----------------------------------------------+
                           │
                           ▼
    +-----------+ → +-----------+ → +-----------+ → +-----------+ → +-----------+
    | Planner   |   | Research  |   | Code      |   | Review    |   | Refine    |
    | Agent     |   | Agent     |   | Agent     |   | Agent     |   | Agent     |
    +-----------+   +-----------+   +-----------+   +-----------+   +-----------+
           │               │               │               │               │
           └───────────────┴───────────────┴───────────────┴───────────────┘
                                   │
                                   ▼
                      Final Response Returned to User
```

---

# 🤖 5-Agent Pipeline

### 1️⃣ Planner Agent
- Understands the user's request
- Creates an execution plan

### 2️⃣ Research Agent
- Collects relevant information
- Retrieves required context

### 3️⃣ Code Agent
- Generates or modifies content
- Produces the requested solution

### 4️⃣ Review Agent
- Reviews the generated output
- Validates correctness and quality

### 5️⃣ Refine Agent
- Improves the response
- Produces the final optimized result

---

# 📂 Project Structure

```
vibecode-academy/
│
├── frontend/          # React + Vite frontend
├── backend/           # FastAPI backend
│   ├── agents/        # Google ADK agents
│   ├── routes/        # API endpoints
│   ├── database/      # JSON storage
│   └── main.py
│
├── README.md
└── requirements.txt
```

---

# 🚀 Deployment

### Frontend
Hosted on **Render Static Site**

### Backend
Hosted on **Render Web Service**

---

# 📸 Demo

Live Demo:
> https://YOUR-FRONTEND-URL.onrender.com

Backend API:
> https://YOUR-BACKEND-URL.onrender.com/docs

GitHub Repository:
> https://github.com/Monishabaskar07/vibecode-academy

---

# 🎯 Learning Objectives

This project demonstrates:

- Multi-Agent AI systems
- Agent orchestration with Google ADK
- FastAPI REST API development
- React frontend integration
- Secure data management
- Cloud deployment using Render

---

# 📜 License

This project was developed for educational purposes as part of the **Google AI Agents Capstone Project**.

---

⭐ If you found this project interesting, consider giving it a star!
