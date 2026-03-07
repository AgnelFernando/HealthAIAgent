<script setup lang="ts">
import type { Citation } from '../../types/chat'

defineProps<{
  citations: Citation[]
}>()
</script>

<template>
  <div v-if="citations.length" class="citations">
    <h4>Sources</h4>
    <ul>
      <li v-for="(citation, index) in citations" :key="index">
        <a :href="citation.url" target="_blank" rel="noopener noreferrer">
          {{ citation.title }}
        </a>
        <span v-if="citation.similarity !== undefined">
          — similarity: {{ citation.similarity.toFixed(2) }}
        </span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.citations {
  margin-top: 12px;
}

ul {
  padding-left: 18px;
}

li {
  margin-bottom: 6px;
}
</style>
