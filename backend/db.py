from models import UpdateUserProfile


def fetch_metrics_summary(conn, user_id: str, days: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("select user_metrics_summary(%s::uuid, %s::int);", (user_id, days))
        row = cur.fetchone()
        if not row:
            return None
        return row[0]  

def fetch_daily_metrics(conn, user_id: str, start_date: str, end_date: str) -> list[dict] | None:
    with conn.cursor() as cur:
        cur.execute("""select date, sleep_minutes, resting_hr, hrv, steps, active_minutes from daily_metrics
                        where user_id = %s::uuid and date BETWEEN %s::date AND %s::date;""", 
                        (user_id, start_date, end_date))
        rows = cur.fetchall()
        return rows
    
def fetch_matcing_chunks(conn, query_embedding, k=5):
    with conn.cursor() as cur:
        cur.execute("select * from match_knowledge_chunks(%s::vector(384), %s)", (query_embedding, k))
        rows = cur.fetchall()
        return rows
    
def fetch_user_profile(conn, user_id: str) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("select * from users where id = %s::uuid;", (user_id,))
        row = cur.fetchone()
        return row
    
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
                    
                  