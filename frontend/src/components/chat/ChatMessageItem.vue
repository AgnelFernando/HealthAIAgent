<script setup lang="ts">
import type { ChatMessage } from '../../types/chat'
import CitationList from './CitationList.vue'
import ConfidenceBadge from './ConfidenceBadge.vue'

defineProps<{
  message: ChatMessage
}>()
</script>

<template>
  <div class="message" :class="message.role">
    <div class="meta">
      <strong>{{ message.role }}</strong>
    </div>

    <p>{{ message.text }}</p>

    <CitationList
      v-if="message.role === 'assistant' && message.citations?.length"
      :citations="message.citations"
    />

    <ConfidenceBadge v-if="message.role === 'assistant'" :confidence="message.confidence" />
  </div>
</template>

<style scoped>
.message {
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 12px;
}

.user {
  background: #2a73c6;
}

.assistant {
  background: #333f2c;
}

.system {
  background: #686868;
}

.meta {
  margin-bottom: 8px;
  text-transform: capitalize;
}
</style>
