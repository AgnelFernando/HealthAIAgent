

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