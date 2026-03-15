
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

from statistics import pstdev

def safe_avg(values):
    values = [v for v in values if v is not None]
    if not values:
        return 0.0
    return sum(values) / len(values)

def compute_sleep_debt_hours(sleep_values: list[float], target_sleep_hours: float) -> float:
    target_minutes = target_sleep_hours * 60
    total_deficit = sum(max(0, target_minutes - value) for value in sleep_values if value is not None)
    return round(total_deficit / 60, 1)

def compute_days_below_target(sleep_values: list[float], target_sleep_hours: float) -> int:
    target_minutes = target_sleep_hours * 60
    return sum(1 for value in sleep_values if value is not None and value < target_minutes)

def compute_consistency_score(sleep_values: list[float]) -> float:
    values = [v for v in sleep_values if v is not None]
    if len(values) <= 1:
        return 1.0
    std_dev = pstdev(values)
    score = max(0.0, min(1.0, 1 - (std_dev / 120)))
    return round(score, 2)

def build_sleep_summary(avg_sleep_minutes, target_sleep_hours, days_below_target, consistency_score):
    avg_sleep_hours = avg_sleep_minutes / 60 if avg_sleep_minutes else 0

    if days_below_target >= 5:
        return f"Sleep duration was below the {target_sleep_hours:g}-hour target on {days_below_target} of the last 7 days."

    if consistency_score < 0.6:
        return "Sleep duration varied significantly across the last 7 days, suggesting an inconsistent sleep schedule."

    if avg_sleep_hours >= target_sleep_hours:
        return "Sleep duration was generally aligned with the target and remained relatively stable this week."

    return "Sleep was moderately below target this week, but patterns were fairly consistent overall."
