<script setup lang="ts">
import type { AnomaliesResponse } from '../../types/anomalies'

defineProps<{
  anomalies: AnomaliesResponse
}>()
</script>

<template>
  <section class="risk-flags-panel">
    <div class="header">
      <h2>Risk Flags</h2>
      <p>Recent changes that may be worth monitoring.</p>
    </div>

    <div v-if="anomalies.flags.length === 0" class="empty-state">
      <span class="status-dot green"></span>
      <div>
        <strong>No notable risk flags</strong>
        <p>Recent sleep, recovery, and activity signals look relatively stable.</p>
      </div>
    </div>

    <div v-else class="flags-list">
      <div
        v-for="flag in anomalies.flags"
        :key="`${flag.metric}-${flag.message}`"
        class="flag-card"
        :class="flag.severity"
      >
        <div class="flag-top">
          <span class="severity-badge" :class="flag.severity">
            {{ flag.severity }}
          </span>
          <span class="metric-name">{{ flag.metric }}</span>
        </div>

        <p>{{ flag.message }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.risk-flags-panel {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
  margin-top: 24px;
}

.header {
  margin-bottom: 20px;
  color: hsla(160, 100%, 37%, 1);
}

.header h2 {
  margin: 0 0 6px 0;
}

.header p {
  margin: 0;
  color: #666;
}

.empty-state {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #ecfdf5;
  border-radius: 12px;
  padding: 16px;
}

.empty-state p {
  margin: 6px 0 0 0;
  color: #4b5563;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  margin-top: 4px;
  flex-shrink: 0;
}

.status-dot.green {
  background: #16a34a;
}

.flags-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.flag-card {
  border-radius: 12px;
  padding: 16px;
  border-left: 5px solid transparent;
}

.flag-card.medium {
  background: #fefce8;
  border-left-color: #ca8a04;
  color: #856014;
}

.flag-card.high {
  background: #fef2f2;
  border-left-color: #dc2626;
  color: #FF7B9C;
}

.flag-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.severity-badge {
  font-size: 12px;
  text-transform: capitalize;
  padding: 4px 8px;
  border-radius: 999px;
  font-weight: 600;
}

.severity-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.severity-badge.high {
  background: #fee2e2;
  color: #991b1b;
}

.metric-name {
  font-size: 13px;
  color: #6b7280;
}

.flag-card p {
  margin: 0;
  line-height: 1.5;
}
</style>