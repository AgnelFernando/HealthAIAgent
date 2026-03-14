export interface DailyMetricPoint {
  date: string
  sleep_minutes: number
  resting_hr: number
  hrv: number
  steps: number
  activity_minutes: number
}

export interface DailyMetricsResponse {
  user_id: string
  data: DailyMetricPoint[]
}

export interface MetricCardData {
  title: string
  value: string
  trendLabel: string
  trendDirection: 'up' | 'down' | 'neutral'
  trendChange: number
  points: number[]
}