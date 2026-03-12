
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