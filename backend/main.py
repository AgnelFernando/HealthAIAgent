from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import psycopg2
import os

import utils

DB_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://agnelfernando.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/rag/answer")
def rag_answer(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question'")

    client = get_openai_client()
    conn = get_db_conn()

    try:
        retrieved = utils.retrieve_chunks(question, client, conn)
        if not retrieved:
            return {"answer": "I don't have enough information in my knowledge base.", "citations": [], "confidence": 0.0}

        prompt = utils.build_prompt(question, retrieved)
        answer = utils.generate_answer(client, prompt)

    
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


@app.get("/metrics/summary")
def metrics_summary(user_id: str, days: int = 7):
    conn = get_db_conn()
    try:
        summary = utils.fetch_metrics_summary(conn, user_id, days)
        if not summary:
            raise HTTPException(status_code=404, detail="No metrics found for this user/range")
        return {"user_id": user_id, "days": days, "summary": summary}
    finally:
        conn.close()


@app.get("/metrics/compare")
def metrics_compare(user_id: str, days: int = 7, baseline_days: int = 30):
    conn = get_db_conn()
    try:
        s7 = utils.fetch_metrics_summary(conn, user_id, days)
        s30 = utils.fetch_metrics_summary(conn, user_id, baseline_days)
        if not s7:
            raise HTTPException(status_code=404, detail="No metrics found for this user/range")
        if not s30:
            return {"user_id": user_id, "days": days, "baseline_days": baseline_days, "summary": s7, "baseline": None, "changes": None}

        changes = {
            "sleep_change_pct": utils.pct_change(s7.get("avg_sleep"), s30.get("avg_sleep")),
            "resting_hr_change_pct": utils.pct_change(s7.get("avg_resting_hr"), s30.get("avg_resting_hr")),
            "hrv_change_pct": utils.pct_change(s7.get("avg_hrv"), s30.get("avg_hrv")),
            "steps_change_pct": utils.pct_change(s7.get("total_steps"), s30.get("total_steps")),
        }
        return {"user_id": user_id, "days": days, "baseline_days": baseline_days, "summary": s7, "baseline": s30, "changes": changes}
    finally:
        conn.close()

@app.post("/chat")
def chat(payload: dict):
    user_id = payload.get("user_id")
    message = payload.get("message")
    days = int(payload.get("days", 7))
    baseline_days = int(payload.get("baseline_days", 30))

    if not user_id or not message:
        raise HTTPException(status_code=400, detail="Missing 'user_id' or 'message'")

    client = get_openai_client()
    conn = get_db_conn()

    try:
        metrics_context = None
        flags = []
        changes = None

        if utils.should_use_metrics(message):
            s_curr = utils.fetch_metrics_summary(conn, user_id, days)
            s_base = utils.fetch_metrics_summary(conn, user_id, baseline_days)

            if s_curr:
                metrics_context = {
                    "days": days,
                    "summary": s_curr,
                    "baseline_days": baseline_days,
                    "baseline": s_base,
                }

                if s_base:
                    changes = {
                        "sleep_change_pct": utils.pct_change(s_curr.get("avg_sleep"), s_base.get("avg_sleep")),
                        "resting_hr_change_pct": utils.pct_change(s_curr.get("avg_resting_hr"), s_base.get("avg_resting_hr")),
                        "hrv_change_pct": utils.pct_change(s_curr.get("avg_hrv"), s_base.get("avg_hrv")),
                        "steps_change_pct": utils.pct_change(s_curr.get("total_steps"), s_base.get("total_steps")),
                    }

                flags = utils.compute_health_flags(s_curr)


        flags_text = ""
        if flags:
            flags_text = " ".join([f.get("flag") if isinstance(f, dict) else str(f) for f in flags])

        retrieval_query = message if not flags_text else f"{message}\nContext signals: {flags_text}"
        retrieved = utils.retrieve_chunks(retrieval_query, client, conn)

        if not retrieved:
            return {
                "answer": "I don't have enough information in my knowledge base.",
                "citations": [],
                "confidence": 0.0,
                "metrics": metrics_context,
                "flags": flags,
                "changes": changes,
            }

        prompt = utils.build_prompt(
            question=message,
            retrieved_chunks=retrieved,
            metrics_context=metrics_context,
            flags=flags,
            changes=changes,
        )

        answer = utils.generate_answer(client, prompt)

        similarities, citations = [], []
        for r in retrieved:
            title = r[3]
            url = r[4]
            sim = float(r[5])
            similarities.append(sim)
            citations.append({"title": title, "url": url, "similarity": sim})

        confidence = round(sum(similarities) / len(similarities), 3)

        return {
            "answer": answer,
            "citations": citations,
            "confidence": confidence,
            "metrics": metrics_context,
            "flags": flags,
            "changes": changes,
        }

    finally:
        conn.close()