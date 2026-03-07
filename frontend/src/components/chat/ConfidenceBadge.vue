<script setup lang="ts">
const props = defineProps<{
  confidence?: number
}>()

function formatConfidence(value?: number) {
  if (value === undefined || value === null) return 'N/A'
  return `${Math.round(value * 100)}%`
}
</script>

<template>
  <span class="badge">Confidence: {{ formatConfidence(props.confidence) }}</span>
</template>

<style scoped>
.badge {
  display: inline-block;
  margin-top: 8px;
  padding: 6px 10px;
  font-size: 12px;
  border-radius: 999px;
  background: #181818;
  color: #fff;
}
</style>
