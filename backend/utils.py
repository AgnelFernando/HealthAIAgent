import json
from statistics import pstdev

from models import UserProfile

METRIC_TERMS = ("sleep", "hrv", "resting", "heart", "steps", "tired", "recovery", "training", "baseline", "last week", "my ")

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

def pct_drop(current, baseline):
    if current is None or baseline is None or baseline == 0:
        return None
    return ((baseline - current) / baseline) * 100

def severity_from_threshold(value: float, medium_threshold: float, high_threshold: float) -> str:
    if value >= high_threshold:
        return "high"
    if value >= medium_threshold:
        return "medium"
    return "low"

def should_use_metrics(message: str) -> bool:
    m = (message or "").lower()
    return any(t in m for t in METRIC_TERMS)

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

def compute_hr_flags(recent, baseline, days):
    flags = []

    # 1. Resting HR elevated
    hr_change_pct = pct_change(
        recent.get("avg_resting_hr"),
        baseline.get("avg_resting_hr")
    )
    if hr_change_pct is not None and hr_change_pct >= 10:
        severity = "high" if hr_change_pct >= 15 else "medium"
        flags.append({
            "metric": "resting_hr",
            "severity": severity,
            "message": f"Resting HR is {round(hr_change_pct)}% above your {days}-day baseline."
        })

    # 2. HRV suppressed
    hrv_drop_pct = pct_drop(
        recent.get("avg_hrv"),
        baseline.get("avg_hrv")
    )
    if hrv_drop_pct is not None and hrv_drop_pct >= 15:
        severity = "high" if hrv_drop_pct >= 25 else "medium"
        flags.append({
            "metric": "hrv",
            "severity": severity,
            "message": f"HRV is {round(hrv_drop_pct)}% below your {days}-day baseline."
        })

    return flags

def compute_sleep_flags(recent_rows, sleep_target_hours):
    target_sleep_minutes = sleep_target_hours * 60
    flags = []

    # 1. Sleep below target for 3+ days
    days_below_target = 0
    for row in recent_rows:
        sleep_minutes = row[1]
        if sleep_minutes is not None and float(sleep_minutes) < target_sleep_minutes:
            days_below_target += 1

    if days_below_target >= 3:
        severity = "high" if days_below_target >= 5 else "medium"
        flags.append({
            "metric": "sleep_target",
            "severity": severity,
            "message": f"Sleep duration was below the {sleep_target_hours:g}-hour target on {days_below_target} of the last 7 days."
        })

    # 2. Activity spike after poor sleep
    recent_steps = [float(row[4]) for row in recent_rows if row[4] is not None]
    avg_recent_steps = sum(recent_steps) / len(recent_steps) if recent_steps else 0

    activity_spike_detected = False
    for row in recent_rows:
        sleep_minutes = row[1]
        steps = row[4]
        if sleep_minutes is None or steps is None:
            continue

        if float(sleep_minutes) < target_sleep_minutes and float(steps) > avg_recent_steps * 1.2:
            activity_spike_detected = True
            break

    if activity_spike_detected:
        flags.append({
            "metric": "activity_recovery",
            "severity": "medium",
            "message": "Activity volume spiked on a low-sleep day, which may reduce recovery quality."
        })

    return flags


def build_sleep_analysis(current_sleep_metrics: list, profile: UserProfile | None, metrics_summary: dict | None):
    target_sleep_hours = 8.0
    if profile and profile.sleep_target_hours is not None:
        target_sleep_hours = float(profile.sleep_target_hours)

    sleep_values = [float(r[1]) for r in current_sleep_metrics if r[1] is not None]
    deep_values = [float(r[2]) for r in current_sleep_metrics if r[2] is not None]
    rem_values = [float(r[3]) for r in current_sleep_metrics if r[3] is not None]

    if not sleep_values:
        return None

    avg_sleep_minutes = float(metrics_summary.get("avg_sleep") or 0) if metrics_summary else safe_avg(sleep_values)
    sleep_debt_hours = compute_sleep_debt_hours(sleep_values, target_sleep_hours)
    consistency_score = compute_consistency_score(sleep_values)
    avg_deep_pct = round(safe_avg(deep_values), 1)
    avg_rem_pct = round(safe_avg(rem_values), 1)
    days_below_target = compute_days_below_target(sleep_values, target_sleep_hours)

    summary = build_sleep_summary(
        avg_sleep_minutes=avg_sleep_minutes,
        target_sleep_hours=target_sleep_hours,
        days_below_target=days_below_target,
        consistency_score=consistency_score,
    )

    return {
        "avg_sleep_minutes": round(avg_sleep_minutes, 1),
        "sleep_debt_hours": sleep_debt_hours,
        "consistency_score": consistency_score,
        "avg_deep_pct": avg_deep_pct,
        "avg_rem_pct": avg_rem_pct,
        "days_below_target": days_below_target,
        "target_sleep_hours": target_sleep_hours,
        "summary": summary,
    }

def detect_anomalies(
    days: int,
    baseline_days: int,
    recent_rows: list,
    profile: UserProfile | None,
    current_summary: dict | None,
    baseline_summary: dict | None,
):
    flags = []

    if not current_summary or not baseline_summary:
        return flags

    target_sleep_hours = 8.0
    if profile and profile.sleep_target_hours is not None:
        target_sleep_hours = float(profile.sleep_target_hours)

    # 1. resting HR elevated
    hr_change_pct = pct_change(
        current_summary.get("avg_resting_hr"),
        baseline_summary.get("avg_resting_hr"),
    )
    if hr_change_pct is not None and hr_change_pct >= 10:
        flags.append({
            "metric": "resting_hr",
            "severity": "high" if hr_change_pct >= 15 else "medium",
            "message": f"Resting HR is {round(hr_change_pct)}% above your {baseline_days}-day baseline."
        })

    # 2. HRV suppressed
    hrv_drop_pct = pct_drop(
        current_summary.get("avg_hrv"),
        baseline_summary.get("avg_hrv"),
    )
    if hrv_drop_pct is not None and hrv_drop_pct >= 15:
        flags.append({
            "metric": "hrv",
            "severity": "high" if hrv_drop_pct >= 25 else "medium",
            "message": f"HRV is {round(hrv_drop_pct)}% below your {baseline_days}-day baseline."
        })

    # 3. sleep below target 3+ days
    target_sleep_minutes = target_sleep_hours * 60
    days_below_target = 0

    for row in recent_rows:
        sleep_minutes = row[1]
        if sleep_minutes is not None and float(sleep_minutes) < target_sleep_minutes:
            days_below_target += 1

    if days_below_target >= 3:
        flags.append({
            "metric": "sleep_target",
            "severity": "high" if days_below_target >= 5 else "medium",
            "message": f"Sleep duration was below the {target_sleep_hours:g}-hour target on {days_below_target} of the last {days} days."
        })

    # 4. activity spike after poor sleep
    recent_steps = [float(r[4]) for r in recent_rows if r[4] is not None]
    avg_recent_steps = sum(recent_steps) / len(recent_steps) if recent_steps else 0

    for row in recent_rows:
        sleep_minutes = row[1]
        steps = row[4]
        if sleep_minutes is None or steps is None:
            continue

        if float(sleep_minutes) < target_sleep_minutes and float(steps) > avg_recent_steps * 1.2:
            flags.append({
                "metric": "activity_recovery",
                "severity": "medium",
                "message": "Activity volume spiked on a low-sleep day, which may reduce recovery quality."
            })
            break

    return flags

def build_personalized_chat_prompt(
    question,
    retrieved_chunks,
    profile=None,
    metrics_context=None,
    flags=None,
    anomaly_flags=None,
    changes=None,
    sleep_analysis=None,
):
    profile = profile if isinstance(profile, UserProfile) else None
    metrics_context = metrics_context or {}
    flags = flags or []
    anomaly_flags = anomaly_flags or []
    changes = changes or {}
    sleep_analysis = sleep_analysis or {}

    chunk_text = []
    for r in retrieved_chunks:
        title = r[3]
        content = r[2]
        chunk_text.append(f"[Source: {title}]\n{content}")

    flags_text = "\n".join([f"- {f}" for f in flags]) if flags else "None"
    anomaly_text = "\n".join([f"- ({f['severity']}) {f['message']}" for f in anomaly_flags]) if anomaly_flags else "None"

    return f"""
You are a health intelligence assistant.

Your job is to answer the user's question using:
1. their profile and goals
2. recent wearable metrics
3. sleep analysis
4. anomaly flags
5. retrieved health guidance

Do not diagnose disease.
Do not invent facts.
Be grounded in the provided data and sources.
Keep the tone supportive and practical.

Return valid JSON only in this format:
{{
  "summary": "short personalized answer",
  "what_changed": ["bullet 1", "bullet 2"],
  "guidance": ["bullet 1", "bullet 2"]
}}

User question:
{question}

User profile:
- goal: {profile.goal if profile else None}
- preferred_workout_intensity: {profile.preferred_workout_intensity if profile else None}
- sleep_target_hours: {profile.sleep_target_hours if profile else None}
- notes: {profile.notes if profile else None}

Metrics context:
{metrics_context}

Changes vs baseline:
{changes}

Simple health flags:
{flags_text}

Sleep analysis:
{sleep_analysis}

Anomaly flags:
{anomaly_text}

Relevant guidance:
{chr(10).join(chunk_text)}
"""

def compute_chat_confidence(similarities, sleep_analysis=None, anomaly_flags=None):
    retrieval_score = sum(similarities) / len(similarities) if similarities else 0.0
    data_bonus = 0.15 if sleep_analysis else 0.0
    anomaly_bonus = 0.10 if anomaly_flags is not None else 0.0

    confidence = retrieval_score + data_bonus + anomaly_bonus
    confidence = max(0.0, min(1.0, confidence))
    return round(confidence, 3)

def parse_chat_json_response(raw_answer: str) -> dict:
    try:
        parsed = json.loads(raw_answer)
        return {
            "summary": parsed.get("summary", ""),
            "what_changed": parsed.get("what_changed", []),
            "guidance": parsed.get("guidance", []),
        }
    except Exception:
        return {
            "summary": raw_answer,
            "what_changed": [],
            "guidance": [],
        }