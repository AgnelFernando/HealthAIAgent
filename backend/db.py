from models import UpdateUserProfile, UserProfile


def fetch_sleep_metrics(conn, user_id: str, current_day: str, days: int):
    with conn.cursor() as cur:
        cur.execute("""
            select date, sleep_minutes, deep_sleep_pct, rem_sleep_pct
            from daily_metrics
            where user_id = %s::uuid
              and date between %s::date - (%s - 1) * interval '1 day'
                          and %s::date
            order by date asc;
        """, (user_id, current_day, days, current_day))
        rows = cur.fetchall()
        return rows

def fetch_metrics_summary(conn, user_id: str, current_day: str, days: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("select * from user_metrics_summary(%s::uuid, %s::date, %s::int);", 
                    (user_id, current_day, days))
        row = cur.fetchone()
        if not row:
            return None
        return {
                "avg_sleep": row[0],
                "avg_resting_hr": row[1],
                "avg_hrv": row[2],
                "total_steps": row[3],
                "sleep_variability": row[4] }  

def fetch_daily_metrics(conn, user_id: str, start_date: str, end_date: str) -> list[dict] | None:
    with conn.cursor() as cur:
        cur.execute("""select date, sleep_minutes, resting_hr, hrv, steps, active_minutes from daily_metrics
                        where user_id = %s::uuid and date BETWEEN %s::date AND %s::date;""", 
                        (user_id, start_date, end_date))
        rows = cur.fetchall()
        if rows:
            return [{"date": r[0].isoformat(), "sleep_minutes": r[1], "resting_hr": r[2], "hrv": r[3], "steps": r[4], "active_minutes": r[5]} for r in rows]
        return None
    
def fetch_recent_metrics(conn, user_id: str, current_day: str, days: int):
    with conn.cursor() as cur:
        cur.execute("""
            select date, sleep_minutes, resting_hr, hrv, steps, active_minutes
            from daily_metrics
            where user_id = %s::uuid
              and date between %s::date - (%s - 1) * interval '1 day'
                          and %s::date
            order by date asc;
        """, (user_id, current_day, days, current_day))
        return cur.fetchall()

def fetch_matcing_chunks(conn, query_embedding, k=5):
    with conn.cursor() as cur:
        cur.execute("select * from match_knowledge_chunks(%s::vector(384), %s)", (query_embedding, k))
        rows = cur.fetchall()
        return rows
    
def fetch_user_profile(conn, user_id: str) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("select * from users where id = %s::uuid;", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return UserProfile(
            user_id=row[0], 
            name=row[1], 
            dob=row[2], 
            gender=row[3], 
            weight_lb=row[4], 
            height_cm=row[5], 
            goal=row[6], 
            preferred_workout_intensity=row[8], 
            sleep_target_hours=row[9], 
            notes=row[10])
    
def update_user_profile(conn, user_id: str, profile_data: UpdateUserProfile) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            update users set name = %s, dob = %s, gender = %s, 
                    weight_lb = %s, height_cm = %s, goal = %s, 
                    preferred_workout_intensity = %s, sleep_target_hours = %s, notes = %s
            where id = %s::uuid
                    returning id, name, dob, gender, weight_lb, height_cm, 
                    goal, preferred_workout_intensity, sleep_target_hours, notes;
        """, (profile_data.name, profile_data.dob, profile_data.gender, 
              profile_data.weight_lb, profile_data.height_cm, profile_data.goal, 
              profile_data.preferred_workout_intensity, profile_data.sleep_target_hours, 
              profile_data.notes, user_id))
        updated_row = cur.fetchone()
        conn.commit()
        return updated_row
                    
                  