from models import UpdateUserProfile, UserProfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import psycopg2
import os

import utils
import llm
import db

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
        question_embedding = llm.create_embeddings(client, question)
        retrieved = db.fetch_matcing_chunks(conn, question_embedding)
        if not retrieved:
            return {"answer": "I don't have enough information in my knowledge base.", "citations": [], "confidence": 0.0}

        prompt = utils.build_prompt(question, retrieved)
        answer = llm.generate_answer(client, prompt)

    
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
        summary = db.fetch_metrics_summary(conn, user_id, days)
        if not summary:
            raise HTTPException(status_code=404, detail="No metrics found for this user/range")
        return {"user_id": user_id, "days": days, "summary": summary}
    finally:
        conn.close()

@app.get("/metrics/daily")
def metrics_daily(user_id: str, start_date: str, end_date: str):
    conn = get_db_conn()
    try:
        daily = db.fetch_daily_metrics(conn, user_id, start_date, end_date)
        if not daily:
            raise HTTPException(status_code=404, detail="No metrics found for this user/range")
        data = [{"date": r[0].isoformat(), "sleep_minutes": r[1], "resting_hr": r[2], "hrv": r[3], "steps": r[4], "active_minutes": r[5]} for r in daily]
        return {"user_id": user_id, "data": data}
    finally:
        conn.close()

@app.get("/metrics/compare")
def metrics_compare(user_id: str, days: int = 7, baseline_days: int = 30):
    conn = get_db_conn()
    try:
        s7 = db.fetch_metrics_summary(conn, user_id, days)
        s30 = db.fetch_metrics_summary(conn, user_id, baseline_days)
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
            s_curr = db.fetch_metrics_summary(conn, user_id, days)
            s_base = db.fetch_metrics_summary(conn, user_id, baseline_days)

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
        retrieval_query_embedding = llm.create_embeddings(client, retrieval_query)
        retrieved = db.fetch_matcing_chunks(retrieval_query_embedding, conn)

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

        answer = llm.generate_answer(client, prompt)

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

@app.get("/user/profile/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: str):
    conn = get_db_conn()
    try:
        profile = db.fetch_user_profile(conn, user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        return profile
    finally:
        conn.close()


@app.put("/user/profile/{user_id}", response_model=UserProfile)
def update_profile(user_id: str, payload: UpdateUserProfile):
    conn = get_db_conn()
    try:
        updated_row = db.update_user_profile(conn, user_id, payload)
        if not updated_row:
            raise HTTPException(status_code=404, detail="Profile not found")
        updated_profile = UserProfile(user_id=updated_row[0], name=updated_row[1], dob=updated_row[2], 
                              gender=updated_row[3], weight_lb=updated_row[4], 
                              height_cm=updated_row[5], goal=updated_row[6], 
                              preferred_workout_intensity=updated_row[7], 
                              sleep_target_hours=updated_row[8], notes=updated_row[9])
        return updated_profile
    finally:        
        conn.close()

@app.get("/analysis/sleep-trends")
def sleep_trends(user_id: str, current_day: str, days: int = 7):
    conn = get_db_conn()
    try:
        summary = db.fetch_metrics_summary(conn, user_id, current_day, days)
        if not summary:
            raise HTTPException(status_code=404, detail="No metrics found for this user/range")

        profile: UserProfile = db.fetch_user_profile(conn, user_id)
        target_sleep_hours = 8.0
        if profile and profile.sleep_target_hours is not None:
            target_sleep_hours = float(profile.sleep_target_hours)

        rows = db.fetch_sleep_metrics(conn, user_id, current_day, days)
        if not rows:
            raise HTTPException(status_code=404, detail="No sleep metrics found for this user/range")

        sleep_values = [float(row[1]) for row in rows if row[1] is not None]
        deep_values = [float(row[2]) for row in rows if row[2] is not None]
        rem_values = [float(row[3]) for row in rows if row[3] is not None]

        avg_sleep_minutes = float(summary.get("avg_sleep") or 0)
        sleep_debt_hours = utils.compute_sleep_debt_hours(sleep_values, target_sleep_hours)
        days_below_target = utils.compute_days_below_target(sleep_values, target_sleep_hours)
        consistency_score = utils.compute_consistency_score(sleep_values)

        avg_deep_pct = round(utils.safe_avg(deep_values), 1)
        avg_rem_pct = round(utils.safe_avg(rem_values), 1)

        summary_text = utils.build_sleep_summary(
            avg_sleep_minutes=avg_sleep_minutes,
            target_sleep_hours=target_sleep_hours,
            days_below_target=days_below_target,
            consistency_score=consistency_score,
        )

        return {
            "user_id": user_id,
            "days": days,
            "avg_sleep_minutes": round(avg_sleep_minutes, 1),
            "sleep_debt_hours": sleep_debt_hours,
            "consistency_score": consistency_score,
            "avg_deep_pct": avg_deep_pct,
            "avg_rem_pct": avg_rem_pct,
            "days_below_target": days_below_target,
            "target_sleep_hours": target_sleep_hours,
            "summary": summary_text,
        }
    finally:
        conn.close()
