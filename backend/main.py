from fastapi import FastAPI
import psycopg2
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from utils import retrieve_chunks, build_prompt

app = FastAPI()
DB_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/rag/answer")
def rag_answer(payload: dict):
    question = payload["question"]

    conn = psycopg2.connect(DB_URL)

    retrieved = retrieve_chunks(question, model, conn)
    prompt = build_prompt(question, retrieved)
    answer = generate_answer(client, prompt)

    confidence = round(sum([r[5] for r in retrieved]) / len(retrieved), 3)

    conn.close()

    citations = [
        {
            "title": r[3],
            "url": r[4],
            "similarity": float(r[5]),
        }
        for r in retrieved
    ]

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence
    }