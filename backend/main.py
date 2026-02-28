from fastapi import FastAPI, HTTPException
import os
import psycopg2

from utils import retrieve_chunks, build_prompt, generate_answer  

app = FastAPI()

DB_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/health")
def health():
    return {"ok": True}


def get_db_conn():
    if not DB_URL:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(DB_URL)


@lru_cache(maxsize=1)
def get_openai_client():
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)


@app.post("/rag/answer")
def rag_answer(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question'")

    client = get_openai_client()
    conn = get_db_conn()

    try:
        retrieved = retrieve_chunks(question, client, conn)
        if not retrieved:
            return {"answer": "I don't have enough information in my knowledge base.", "citations": [], "confidence": 0.0}

        prompt = build_prompt(question, retrieved)
        answer = generate_answer(client, prompt)

    
        similarities = []
        citations = []
        for r in retrieved:
            title = r[3]
            url = r[4]
            sim = float(r[5])

            similarities.append(sim)
            citations.append({"title": title, "url": url, "similarity": sim})

        confidence = round(sum(similarities) / len(similarities), 3)

        return {"answer": answer, "citations": citations, "confidence": confidence}

    finally:
        conn.close()