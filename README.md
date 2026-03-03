# 🤖 LLM powered User Support Agent

An intelligent **LLM-powered User Support System** built using:

- FastAPI (Backend API)
- Transformer-based Sentiment Analysis (RoBERTa)
- Persona Detection
- Streamlit (Frontend UI)

The system detects user persona, analyzes sentiment, generates a response, and determines whether escalation is required — all in real-time.

---

## Features

### 1. Sentiment Analysis
- Uses `cardiffnlp/twitter-roberta-base-sentiment`
- Detects:
  - Negative
  - Neutral
  - Positive
- Returns confidence score
- Used for escalation logic

---

### 2. Persona Detection
Automatically identifies user type such as:
- Frustrated Customer
- Curious User
- Technical User
- General User

---

### 3. AI Response Generator
Generates context-aware responses based on:
- Persona
- Sentiment
- Escalation need

---

### 4. Smart Escalation System
Triggers escalation when:
- Sentiment is strongly negative
- Confidence crosses defined threshold

---

### 5. Streamlit UI
- Clean chat interface
- Sidebar with advanced analytics
- Sentiment + confidence display
- Escalation indicator

---

# Architecture
User (Streamlit UI)
↓
FastAPI Backend (/chat)
↓
┌─────────────────────────┐
│ Persona Detection │
│ Sentiment Analyzer │
│ Response Generator │
│ Escalation Logic │
└─────────────────────────┘
↓
JSON Response → UI

---

# Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | FastAPI |
| Frontend    | Streamlit |
| NLP Model   | RoBERTa |
| ML Library  | PyTorch |
| API Server  | Uvicorn |

---

# Installation

##  Clone Repository

```bash
git clone https://github.com/yourusername/ai-support-agent.git
cd ai-support-agent

