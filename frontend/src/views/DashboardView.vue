<script setup lang="ts">
import MetricCard from '../components/dashboard/MetricCard.vue'
import { useMetrics } from '../composables/useMetrics'
import { ref } from 'vue'
import { USER_OPTIONS } from '../constants/users'

const selectedUserId = ref(
  localStorage.getItem('selected_user_id') || USER_OPTIONS[0]?.user_id || "557975cf-2b37-4f1f-8d7e-0b80921d2db7"
)

const { cards, isLoading, error, fetchMetrics } = useMetrics(selectedUserId.value)
</script>

<template>
  <main class="dashboard-page">
    <section class="dashboard-header">
      <div>
        <h1>Health Dashboard</h1>
        <p>Last 7 days overview of sleep, recovery, and activity.</p>
      </div>

      <button @click="fetchMetrics">Refresh</button>
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

.state-box.error {
  background: #504949;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-header {
    flex-direction: column;
  }
}
</style>