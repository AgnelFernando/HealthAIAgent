<script setup lang="ts">
import { ref, watch } from 'vue'
import MetricCard from '../components/dashboard/MetricCard.vue'
import SleepAnalysisPanel from '../components/dashboard/SleepAnalysisPanel.vue'
import { useMetrics } from '../composables/useMetrics'
import { useSleepAnalysis } from '../composables/useSleepAnalysis'
import { USER_OPTIONS } from '../constants/users'

const selectedUserId = ref(
  localStorage.getItem('selected_user_id') ||
    USER_OPTIONS[0]?.user_id ||
    '557975cf-2b37-4f1f-8d7e-0b80921d2db7'
)

const { cards, isLoading, error, fetchMetrics } = useMetrics(selectedUserId.value)
const {
  analysis,
  isLoading: isAnalysisLoading,
  error: analysisError,
  fetchSleepAnalysis,
} = useSleepAnalysis(selectedUserId)

function refreshAll() {
  fetchMetrics()
  fetchSleepAnalysis()
}
</script>

<template>
  <main class="dashboard-page">
    <section class="dashboard-header">
      <div>
        <h1>Health Dashboard</h1>
        <p>Last 7 days overview of sleep, recovery, and activity.</p>
      </div>

      <div class="header-actions">

        <button @click="refreshAll">Refresh</button>
      </div>
    </section>

    <section v-if="isLoading" class="state-box">
      Loading metrics...
    </section>

    <section v-else-if="error" class="state-box error">
      {{ error }}
    </section>

    <section v-else class="metrics-grid">
      <MetricCard
        v-for="card in cards"
        :key="card.title"
        :card="card"
      />
    </section>

    <section v-if="isAnalysisLoading" class="state-box analysis-state">
      Loading sleep analysis...
    </section>

    <section v-else-if="analysisError" class="state-box error analysis-state">
      {{ analysisError }}
    </section>

    <SleepAnalysisPanel
      v-else-if="analysis"
      :analysis="analysis"
    />
  </main>
</template>

<style scoped>
.dashboard-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 12px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 12px;
}

.dashboard-header h1 {
  margin: 0 0 8px 0;
}

.dashboard-header p {
  margin: 0;
  color: #666;
}

.header-actions {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.user-picker {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.user-picker span {
  font-size: 13px;
  color: #666;
}

.user-picker select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
  background: white;
}

button {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  cursor: pointer;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.state-box {
  padding: 18px;
  border-radius: 12px;
  background: #f8fafc;
}

.analysis-state {
  margin-top: 24px;
}

.state-box.error {
  background: #504949;
  color: white;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
