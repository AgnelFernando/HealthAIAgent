# HealthAIAgent

A wearable-integrated, **RAG-grounded, agentic AI system** that analyzes sleep, activity, and physiological signals to generate **personalized health insights and action workflows**.

🔗 [Live Website](https://agnelfernando.github.io/HealthAIAgent/#/)

---

## Project Overview

HealthAIAgent is a **production-oriented AI system** that combines:

* Structured wearable time-series data
* Medical knowledge retrieval (CDC / NIH / WHO)
* LLM-based reasoning
* Backend analytics tools (trends + anomaly detection)
* Personalized recommendation generation

Unlike a simple chatbot, this system:

* Grounds responses in medical guidelines (**RAG**)
* Personalizes insights using user profile + historical data
* Performs quantitative trend + anomaly analysis
* Uses **agent-style orchestration** across multiple data sources
* Returns structured outputs with citations + confidence

---

## Key Features

### 1. Retrieval-Augmented Generation (RAG)

* Embedding-based retrieval using **pgvector**
* Context-grounded answers with citations
* Knowledge sourced from CDC, WHO, NIH

---

### 2. Metrics Dashboard (Time-Series Intelligence)

* Sleep duration (7-day)
* Resting heart rate
* HRV (heart rate variability)
* Steps / activity

Each card includes:

* Current average
* Trend direction
* Mini visualization

---

### 3. User Personalization Layer

User profile includes:

* Goal (sleep, fat loss, endurance, etc.)
* Sleep target
* Workout intensity preference
* Physical attributes

This enables responses like:

> “Based on your goal of improving sleep…”

---

### 4. Sleep Trend Analysis Tool

Endpoint:

```
GET /analysis/sleep-trends
```

Outputs:

* Average sleep
* Sleep debt
* Consistency score
* Sleep stage breakdown
* Natural language summary

---

### 5. Anomaly Detection Engine

Endpoint:

```
GET /analysis/anomalies
```

Detects:

* Elevated resting HR
* Low HRV (stress signal)
* Sleep deprivation patterns
* Recovery imbalance

---

### 6. Agentic Personalized Chat (Core Feature)

Endpoint:

```
POST /chat
```

Combines:

* Retrieved medical knowledge
* Recent metrics summary
* Anomaly signals
* User profile preferences

#### Example Questions:

* “Why am I tired this week?”
* “Am I getting enough sleep?”
* “Should I reduce workout intensity?”

#### Response Structure:

* Summary
* What changed in your data
* Relevant guidance
* Sources
* Confidence score

---

## System Architecture

```
User Query
    ↓
Agent Router
    ↓
 ┌──────────────┬──────────────────┬──────────────────┐
 │ RAG Engine   │ Metrics Engine   │ Profile Context  │
 │ (pgvector)   │ (Postgres)       │ (User Data)      │
 └──────────────┴──────────────────┴──────────────────┘
    ↓
Analytics Tools
(sleep trends + anomalies)
    ↓
LLM Reasoning Layer
    ↓
Structured Personalized Response
    ↓
Citations + Confidence Score
```

---

## Tech Stack

### Backend

* **FastAPI**
* **PostgreSQL + pgvector**
* **Sentence Transformers** (embeddings)
* **OpenAI API**

### Frontend

* **Vue 3 + Vite**
* Component-based dashboard + chat UI
* GitHub Pages deployment

### Data

* Structured time-series (daily_metrics)
* Knowledge chunks (vector indexed)
* User profile + preferences

---

## Example Response (RAG)

```json
{
  "answer": "Most adults need at least 7 hours of sleep each night.",
  "citations": [
    {
      "title": "About Sleep",
      "url": "https://www.cdc.gov/sleep/about/",
      "similarity": 0.60
    }
  ],
  "confidence": 0.57
}
```

---

## Example Response (Personalized Chat)

```json
{
  "summary": "Your fatigue this week is likely due to reduced sleep and elevated resting heart rate.",
  "what_changed": [
    "Sleep decreased by 12% vs baseline",
    "Resting HR increased by 10%"
  ],
  "guidance": [
    "Aim for at least 7 hours of sleep",
    "Reduce workout intensity for recovery"
  ],
  "confidence": 0.81
}
```

## Example Personalized Chat Response

**User:**
Why am I tired this week?

**AI Agent**

**Summary**
You're feeling tired this week likely due to insufficient sleep, as you've been below your target of 8 hours every night.

**What changed in your data**

* You averaged **406.2 minutes of sleep**, below your target of **480 minutes (8 hours)**.
* You accumulated **7.5 hours of sleep debt** over the past week.

**Relevant guidance**

* Establish a more consistent bedtime routine.
* Reduce screen time and caffeine intake before bed.

**Sources**

* *Sleep timing and consistency are associated with the standardised test performance of Icelandic adolescents* — similarity: **0.55**
* *Short Sleep Duration: Children’s Mental, Behavioral, and Developmental Disorders and Demographic, Neighborhood, and Family Context in a Nationally Representative Sample, 2016–2019* — similarity: **0.54**

**Confidence**
**79%**


---

## How to Run

### Backend

```bash
git clone https://github.com/yourname/HealthAIAgent
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Environment Variables

```
DATABASE_URL=
OPENAI_API_KEY=
```

👉 Turn this into a **resume bullet section (VERY high impact for ML roles)**
👉 Or add **system diagrams for GitHub (looks 10x more professional)**
