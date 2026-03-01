
def retrieve_chunks(question, client, conn, k=5):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=question,
        dimensions=384,  
    )
    query_embedding = resp.data[0].embedding

    cur = conn.cursor()
    cur.execute("select * from match_knowledge_chunks(%s::vector(384), %s)", (query_embedding, k))

    rows = cur.fetchall()
    cur.close()
    return rows

def build_prompt(question, retrieved_chunks, metrics_context=None, flags=None, changes=None):
    sources_text = "\n\n".join(
        [f"[Source: {r[3]}]\n{r[2]}" for r in retrieved_chunks]
    )

    metrics_text = "None"
    if metrics_context:
        metrics_text = (
            f"Range: last {metrics_context.get('days')} days\n"
            f"Summary: {metrics_context.get('summary')}\n"
            f"Baseline ({metrics_context.get('baseline_days')} days): {metrics_context.get('baseline')}"
        )

    flags_text = "None"
    if flags:
        flags_text = "\n".join([f"- {f}" for f in flags]) if isinstance(flags, list) else str(flags)

    changes_text = "None"
    if changes:
        changes_text = str(changes)

    return f"""
You are a health information assistant.

Rules:
- Use the SOURCES below for all general medical/health claims and guidelines.
- You MAY use the user's METRICS (numbers) to personalize the response (e.g., trends, averages, baseline changes).
- If the SOURCES do not contain the needed guideline/fact, say: "I do not have enough information from the provided sources."
- Do NOT diagnose. Do NOT claim a disease/condition. Use cautious language like "may", "can be associated with".
- Always cite sources by title in parentheses for guideline/medical statements.

Response format:
1) Answer (2-6 sentences)
2) Personalized insights (bullets, only if METRICS are present)
3) What to do next (bullets, practical + safe)
4) Sources (list the titles you used)

USER METRICS (if available):
{metrics_text}

FLAGS (if available):
{flags_text}

BASELINE CHANGES (if available):
{changes_text}

SOURCES:
{sources_text}

QUESTION:
{question}
"""


def generate_answer(client, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content

def compute_health_flags(summary):
    flags = []

    if summary["avg_sleep"] < 420:
        flags.append("sleep_deprivation_risk")

    if summary["avg_resting_hr"] > 75:
        flags.append("elevated_resting_hr")

    if summary["avg_hrv"] < 35:
        flags.append("low_hrv_stress_signal")

    if summary["sleep_variability"] > 90:
        flags.append("irregular_sleep_schedule")

    return flags

from datetime import datetime

def fetch_metrics_summary(conn, user_id: str, days: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("select user_metrics_summary(%s::uuid, %s::int);", (user_id, days))
        row = cur.fetchone()
        if not row:
            return None
        return row[0]  

def safe_float(x):
    try:
        return float(x) if x is not None else None
    except Exception:
        return None

def pct_change(curr, base):
    curr = safe_float(curr)
    base = safe_float(base)
    if curr is None or base is None or base == 0:
        return None
    return round(((curr - base) / base) * 100.0, 1)

METRIC_TERMS = ("sleep", "hrv", "resting", "heart", "steps", "tired", "recovery", "training", "baseline", "last week", "my ")

def should_use_metrics(message: str) -> bool:
    m = (message or "").lower()
    return any(t in m for t in METRIC_TERMS)