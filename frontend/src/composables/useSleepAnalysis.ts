import { ref, watch } from 'vue'
import { API_BASE_URL } from '../config'
import type { SleepTrendsResponse } from '../types/analysis'

export function useSleepAnalysis(selectedUserId: { value: string }) {
  const analysis = ref<SleepTrendsResponse | null>(null)
  const isLoading = ref(false)
  const error = ref('')

  async function fetchSleepAnalysis() {
    isLoading.value = true
    error.value = ''

    try {
      const response = await fetch(
        `${API_BASE_URL}/analysis/sleep-trends?user_id=${selectedUserId.value}&current_day=2025-12-20&days=7`
      )

      if (!response.ok) {
        throw new Error(`Failed to fetch sleep analysis: ${response.status}`)
      }

      analysis.value = await response.json()
    } catch (err) {
      analysis.value = null
      error.value =
        err instanceof Error ? err.message : 'Failed to fetch sleep analysis.'
    } finally {
      isLoading.value = false
    }
  }

  watch(
    () => selectedUserId.value,
    () => {
      fetchSleepAnalysis()
    },
    { immediate: true }
  )

  return {
    analysis,
    isLoading,
    error,
    fetchSleepAnalysis,
  }
}
