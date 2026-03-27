<script setup lang="ts">
import type { Citation } from '../../types/chat'

defineProps<{
  citations: Citation[]
}>()
</script>

<template>
  <div v-if="citations.length" class="citations">
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

.citations a {
  color: #f0544f;
  text-decoration: none;
}

.citations span {
  color: #d81e5b;
}

ul {
  padding-left: 18px;
  margin: 0;
}

li {
  margin-bottom: 6px;
}
</style>
