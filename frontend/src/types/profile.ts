export interface UserProfile {
  user_id: string
  name: string
  dob: string
  gender: string
  goal: string
  weight_lb: number
  height_cm: number
  preferred_workout_intensity: string | null
  sleep_target_hours: number | null
  notes: string | null
}