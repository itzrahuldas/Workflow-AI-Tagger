# 🏷️ Workflow-AI-Tagger

> An AI-powered text tagging API that extracts structured **Tags** and **Summary** from any large text using Groq LLM with function calling.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Node.js](https://img.shields.io/badge/Node.js-24.x-339933?style=flat-square&logo=node.js)](https://nodejs.org/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat-square)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 🏗️ Architecture

```
Client / Postman
     │
     ▼ POST /api/tag
┌─────────────────────┐
│  Node.js Express    │  :3000
│  Middleware Layer   │  • Rate Limiting
│  (Validation, CORS) │  • Request Logging
└────────┬────────────┘  • Input Validation
         │ Proxy → /analyze
         ▼
┌─────────────────────┐
│  FastAPI Backend    │  :8000
│  Python             │  • OpenAI-compatible API
│  (AI Logic)         │  • Function Calling
└────────┬────────────┘  • Structured Output
         │
         ▼
    Groq API (llama-3.3-70b-versatile)
    → Returns { tags, summary }
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone the repo
```bash
git clone https://github.com/itzrahuldas/Workflow-AI-Tagger.git
cd Workflow-AI-Tagger
```

### 2. Setup FastAPI Backend
```bash
cd backend
cp .env.example .env
# Edit .env → add your GROQ_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Setup Express Middleware
```bash
cd middleware
cp .env.example .env
npm install
node src/index.js
```

### 4. Test the API
```bash
curl -X POST http://localhost:3000/api/tag \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming healthcare through machine learning algorithms that detect diseases from medical images with high accuracy.",
    "max_tags": 5
  }'
```

---

## 📡 API Reference

### `POST /api/tag` (Express — Port 3000)

**Request:**
```json
{
  "text": "Your large text here...",
  "max_tags": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tags": ["artificial intelligence", "healthcare", "machine learning", "medical imaging", "disease detection"],
    "summary": "AI and ML are revolutionizing healthcare by enabling accurate disease detection from medical images.",
    "model": "llama-3.3-70b-versatile",
    "usage": {
      "prompt_tokens": 85,
      "completion_tokens": 42,
      "total_tokens": 127
    }
  },
  "timestamp": "2026-07-04T06:00:00.000Z"
}
```

### `POST /analyze` (FastAPI direct — Port 8000)

Direct access to the AI backend (bypasses middleware).

### `GET /health` (FastAPI — Port 8000)

```json
{ "status": "healthy", "model": "llama-3.3-70b-versatile" }
```

---

## 🐳 Docker Setup

```bash
# Copy env files first
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env
# Edit both .env files with your GROQ_API_KEY

docker-compose up --build
```

---

## 🔐 Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | **Required** |
| `MODEL_NAME` | LLM model to use | `llama-3.3-70b-versatile` |
| `MAX_TOKENS` | Max completion tokens | `500` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Middleware (`middleware/.env`)
| Variable | Description | Default |
|----------|-------------|---------|
| `FASTAPI_URL` | FastAPI backend URL | `http://localhost:8000` |
| `PORT` | Express server port | `3000` |
| `RATE_LIMIT_MAX` | Max requests per window | `100` |
| `RATE_LIMIT_WINDOW_MS` | Rate limit window (ms) | `900000` |

---

## 📁 Project Structure

```
Workflow-AI-Tagger/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── main.py           # App entry point & routes
│   │   ├── schemas.py        # Pydantic models
│   │   ├── config.py         # Settings
│   │   └── services/
│   │       └── tagger.py     # Groq function calling logic
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── middleware/               # Express.js middleware
│   ├── src/
│   │   ├── index.js          # Server entry point
│   │   ├── config.js         # Config
│   │   ├── routes/
│   │   │   └── tagRoutes.js  # /api/tag route
│   │   └── middleware/
│   │       ├── rateLimiter.js
│   │       ├── logger.js
│   │       └── validator.js
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Backend | FastAPI (Python 3.11) |
| LLM | Groq API — llama-3.3-70b-versatile |
| Middleware | Node.js + Express.js |
| Validation | Pydantic (Python) + Express middleware |
| Containerization | Docker + Docker Compose |
| Function Calling | OpenAI-compatible API |

---

## 📄 License

MIT © [itzrahuldas](https://github.com/itzrahuldas)
