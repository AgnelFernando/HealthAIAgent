<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler)

const props = defineProps<{
  points: number[]
}>()

const chartData = computed(() => ({
  labels: props.points.map((_, index) => `${index + 1}`),
  datasets: [
    {
      data: props.points,
      borderWidth: 2,
      tension: 0.35,
      pointRadius: 0,
      fill: false,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      enabled: true,
    },
  },
  scales: {
    x: {
      display: false,
    },
    y: {
      display: false,
    },
  },
}
</script>

<template>
  <div class="mini-chart">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.mini-chart {
  height: 90px;
  width: 100%;
}
</style>