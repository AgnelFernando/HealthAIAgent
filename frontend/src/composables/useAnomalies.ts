import { ref, watch } from 'vue'
import { API_BASE_URL } from '../config'
import type { AnomaliesResponse } from '../types/anomalies.ts'

export function useAnomalies(selectedUserId: { value: string }) {
  const anomalies = ref<AnomaliesResponse | null>(null)
  const isLoading = ref(false)
  const error = ref('')

  async function fetchAnomalies() {
    isLoading.value = true
    error.value = ''

    try {
      const response = await fetch(
        `${API_BASE_URL}/analysis/anomalies?user_id=${selectedUserId.value}&current_day=2025-12-20&days=7`
      )

      if (!response.ok) {
        throw new Error(`Failed to fetch anomalies: ${response.status}`)
      }

      anomalies.value = await response.json()
    } catch (err) {
      anomalies.value = null
      error.value =
        err instanceof Error ? err.message : 'Failed to fetch anomalies.'
    } finally {
      isLoading.value = false
    }
  }

  watch(
    () => selectedUserId.value,
    () => {
      fetchAnomalies()
    },
    { immediate: true }
  )

  return {
    anomalies,
    isLoading,
    error,
    fetchAnomalies,
  }
}