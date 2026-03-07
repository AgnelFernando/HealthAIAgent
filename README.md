# HealthAIAgent
A wearable-integrated, RAG-grounded, agentic AI that analyzes sleep, activity, and risk signals to produce personalized health insights and action workflows.
[Live Website](https://agnelfernando.github.io/HealthAIAgent/#/)
## Project Overview

HealthAIAgent is a production-oriented AI system that combines:

* Structured wearable time-series data
* Medical knowledge retrieval (CDC / NIH / WHO)
* LLM-based reasoning
* Tool-calling agent workflows
* Evaluation + grounding metrics

Unlike a simple chatbot, this system:

* Grounds responses in medical guidelines (RAG)
* Personalizes insights using user health history
* Performs quantitative trend analysis
* Returns citations + confidence scores

---

## System Architecture

```
User Query
    ↓
Agent Router
    ↓
 ┌──────────────┬──────────────────┐
 │ RAG Engine   │ Wearable Metrics │
 │ (pgvector)   │ (Postgres)       │
 └──────────────┴──────────────────┘
    ↓
LLM Reasoning Layer
    ↓
Grounded + Personalized Response
    ↓
Citations + Confidence Score
```

### Components

* **FastAPI Backend**
* **Postgres + pgvector** (knowledge + metrics)
* **Embedding pipeline** (chunking + vector indexing)
* **RAG retrieval + citation enforcement**
* **Confidence scoring layer**

---

## Knowledge Base

Sources include:

* CDC sleep guidelines
* WHO physical activity recommendations
* NIH heart health guidance
* Selected peer-reviewed sleep research

All answers are grounded in retrieved documents.

---

## Structured Wearable Data Support

The system supports:

* Sleep duration
* Sleep stage %
* Resting heart rate
* HRV
* Steps
* Activity minutes

Data stored in structured relational format for trend queries.

---

## 🔎 Demo Questions

* How many hours of sleep should adults get?
* What are the health risks associated with insufficient sleep?
* What is sleep hygiene?
* What are recommended physical activity guidelines?

---

## Example RAG Query & Response

### Question

How many hours of sleep should adults get?

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

## How to Run

```bash
git clone https://github.com/yourname/HealthAIAgent
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Environment variables:

```
DATABASE_URL=
OPENAI_API_KEY=
```
