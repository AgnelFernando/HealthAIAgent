export interface SleepTrendsResponse {
  user_id: string
  days: number
  avg_sleep_minutes: number
  sleep_debt_hours: number
  consistency_score: number
  avg_deep_pct: number
  avg_rem_pct: number
  days_below_target: number
  target_sleep_hours: number
  summary: string
}
