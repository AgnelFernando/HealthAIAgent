import { ref, computed, onMounted } from 'vue'
import { API_BASE_URL } from '../config'
import type { DailyMetricPoint, DailyMetricsResponse, MetricCardData } from '../types/metrics'

function average(values: number[]) {
  if (!values.length) return 0
  return values.reduce((sum, value) => sum + value, 0) / values.length
}

function trendDirection(values: number[]): 'up' | 'down' | 'neutral' {
  if (values.length < 2) return 'neutral'
  const first_value: number = values[0] ?? 0
  const last_value: number = values[values.length - 1] ?? 0

  if (last_value > first_value) return 'up'
  if (last_value < first_value) return 'down'
  return 'neutral'
}

function percentChange(values: number[]) {
  if (values.length < 2) return 0

  const firstHalf = values.slice(0, Math.floor(values.length / 2))
  const secondHalf = values.slice(Math.floor(values.length / 2))

  const avg1 = average(firstHalf)
  const avg2 = average(secondHalf)

  if (avg1 === 0) return 0
  return ((avg2 - avg1) / avg1) * 100
}

function formatSleep(minutes: number) {
  const hours = minutes / 60
  return `${hours.toFixed(1)} hrs`
}

function formatNumber(value: number) {
  return Math.round(value).toString()
}

export function useMetrics(userId = "557975cf-2b37-4f1f-8d7e-0b80921d2db7") {
  const data = ref<DailyMetricPoint[]>([])
  const isLoading = ref(false)
  const error = ref('')

  async function fetchMetrics() {
    isLoading.value = true
    error.value = ''

    try {
      const end = new Date("2025-12-07") 
      const start = new Date("2025-12-01")

      const startStr = start.toISOString().slice(0, 10)
      const endStr = end.toISOString().slice(0, 10)

      const response = await fetch(
        `${API_BASE_URL}/metrics/daily?user_id=${userId}&start_date=${startStr}&end_date=${endStr}`
      )

      if (!response.ok) {
        throw new Error(`Failed to fetch metrics: ${response.status}`)
      }

      const json: DailyMetricsResponse = await response.json()
      data.value = json.data ?? []
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch metrics.'
    } finally {
      isLoading.value = false
    }
  }

  const sleepCard = computed<MetricCardData>(() => {
    const points = data.value.map((d) => d.sleep_minutes)
    return {
      title: 'Sleep Duration',
      value: formatSleep(average(points)),
      trendLabel: 'Last 7 days',
      trendDirection: trendDirection(points),
      trendChange: percentChange(points),
      points,
    }
  })

  const hrCard = computed<MetricCardData>(() => {
    const points = data.value.map((d) => d.resting_hr)
    return {
      title: 'Resting HR',
      value: `${formatNumber(average(points))} bpm`,
      trendLabel: 'Last 7 days',
      trendDirection: trendDirection(points),
      trendChange: percentChange(points),
      points,
    }
  })

  const hrvCard = computed<MetricCardData>(() => {
    const points = data.value.map((d) => d.hrv)
    return {
      title: 'HRV',
      value: `${formatNumber(average(points))} ms`,
      trendLabel: 'Last 7 days',
      trendDirection: trendDirection(points),
      trendChange: percentChange(points),
      points,
    }
  })

  const stepsCard = computed<MetricCardData>(() => {
    const points = data.value.map((d) => d.steps)
    return {
      title: 'Steps',
      value: formatNumber(average(points)),
      trendLabel: 'Last 7 days',
      trendDirection: trendDirection(points),
      trendChange: percentChange(points),
      points,
    }
  })

  const cards = computed(() => [
    sleepCard.value,
    hrCard.value,
    hrvCard.value,
    stepsCard.value,
  ])

  onMounted(fetchMetrics)

  return {
    data,
    cards,
    isLoading,
    error,
    fetchMetrics,
  }
}