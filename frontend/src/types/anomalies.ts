export interface AnomalyFlag {
  metric: string
  severity: 'medium' | 'high'
  message: string
}

export interface AnomaliesResponse {
  user_id: string
  days: number
  flags: AnomalyFlag[]
}