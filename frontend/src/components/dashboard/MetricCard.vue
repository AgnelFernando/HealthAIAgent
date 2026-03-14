<script setup lang="ts">
import MiniLineChart from './MiniLineChart.vue'
import type { MetricCardData } from '../../types/metrics'
import up from '../../assets/up.svg'
import down from '../../assets/down.svg'

defineProps<{
  card: MetricCardData
}>()
</script>

<template>
  <div class="metric-card">
    <div class="metric-header">
      <h3>{{ card.title }}</h3>
      <span class="trend" :class="card.trendDirection">
        <img v-if="card.trendDirection === 'up'" :src="up" alt="Up"/>
        <img v-else-if="card.trendDirection === 'down'" :src="down" alt="Down"/>
        {{ Math.abs(card.trendChange).toFixed(1) }} %
      </span>
    </div>

    <div class="metric-value">
      {{ card.value }}
    </div>

    <div class="metric-label">
      {{ card.trendLabel }}
    </div>

    <MiniLineChart :points="card.points" />
  </div>
</template>

<style scoped>
.metric-card {
  background: #E8E9ED;
  color: #FF7B9C;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
  display: flex;
  flex-direction: column;
  font-weight: 600;
  gap: 6px;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-header h3 {
  margin: 0;
  font-size: 16px;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
}

.metric-label {
  font-size: 14px;
  color: #666;
}

.trend {
  text-transform: capitalize;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 999px;
  background: #f3f4f6;
  display: flex;
}

.trend.up {
  background: #0f766e;
  color: #ffffff;
}

.trend.down {
  background: #b91c1c;
  color: #E8E9ED;
}

.trend.neutral {
  color: #6b7280;
}
</style>