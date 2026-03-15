<script setup lang="ts">
import type { SleepTrendsResponse } from '../../types/analysis'

defineProps<{
  analysis: SleepTrendsResponse
}>()

function formatSleep(minutes: number) {
  return `${(minutes / 60).toFixed(1)} hrs`
}

function formatConsistency(score: number) {
  return `${Math.round(score * 100)}%`
}
</script>

<template>
  <section class="sleep-analysis-panel">
    <div class="header">
      <h2>Sleep Analysis</h2>
      <p>Interpretation of recent sleep patterns.</p>
    </div>

    <div class="analysis-grid">
      <div class="analysis-item">
        <span class="label">Average Sleep</span>
        <strong>{{ formatSleep(analysis.avg_sleep_minutes) }}</strong>
      </div>

      <div class="analysis-item">
        <span class="label">Sleep Debt</span>
        <strong>{{ analysis.sleep_debt_hours.toFixed(1) }} hrs</strong>
      </div>

      <div class="analysis-item">
        <span class="label">Consistency</span>
        <strong>{{ formatConsistency(analysis.consistency_score) }}</strong>
      </div>

      <div class="analysis-item">
        <span class="label">Days Below Target</span>
        <strong>{{ analysis.days_below_target }}</strong>
      </div>

      <div class="analysis-item">
        <span class="label">Avg Deep Sleep</span>
        <strong>{{ analysis.avg_deep_pct.toFixed(1) }}%</strong>
      </div>

      <div class="analysis-item">
        <span class="label">Avg REM Sleep</span>
        <strong>{{ analysis.avg_rem_pct.toFixed(1) }}%</strong>
      </div>
    </div>

    <div class="summary-box">
      <span class="label">Summary</span>
      <p>{{ analysis.summary }}</p>
    </div>
  </section>
</template>

<style scoped>
.sleep-analysis-panel {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
  margin-top: 24px;
}

.header {
  margin-bottom: 20px;
  color: #38E4AE;
}

.header h2 {
  margin: 0 0 6px 0;
}

.header p {
  margin: 0;
  color: #666;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.analysis-item {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.analysis-item strong {
    color: #7BD389;
    font-weight: 600;
}

.label {
  font-size: 13px;
  color: #343E3D;
}

.summary-box {
  background: #eef6ff;
  border-radius: 12px;
  padding: 16px;
}

.summary-box p {
  margin: 8px 0 0 0;
  line-height: 1.5;
  color: #7BD389;
}

@media (max-width: 768px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }
}
</style>
