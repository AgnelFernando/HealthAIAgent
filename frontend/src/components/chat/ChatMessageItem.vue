<script setup lang="ts">
import type { ChatMessage } from '../../types/chat'
import CitationList from './CitationList.vue'
import ConfidenceBadge from './ConfidenceBadge.vue'

const props = defineProps<{
  message: ChatMessage
}>()

const isUser = props.message.role === 'user'
const isAssistant = props.message.role === 'assistant'

function getLabel() {
  if (isUser) return 'You'
  if (isAssistant) return 'AI Agent'
  return 'System'
}
</script>

<template>
  <div
    class="message-row"
    :class="{
      'message-row-user': isUser,
      'message-row-assistant': isAssistant,
      'message-row-system': message.role === 'system',
    }"
  >
    <div
      class="message-bubble"
      :class="{
        'message-bubble-user': isUser,
        'message-bubble-assistant': isAssistant,
        'message-bubble-system': message.role === 'system',
      }"
    >
      <div class="meta">
        <strong>{{ getLabel() }}</strong>
      </div>

      <p class="message-text">{{ message.text }}</p>

      <CitationList
        v-if="isAssistant && message.citations?.length"
        :citations="message.citations"
      />

      <ConfidenceBadge
        v-if="isAssistant"
        :confidence="message.confidence"
      />
    </div>
  </div>
</template>

<style scoped>
.message-row {
  display: flex;
  margin-bottom: 12px;
}

.message-row-user {
  justify-content: flex-end;
}

.message-row-assistant {
  justify-content: flex-start;
}

.message-row-system {
  justify-content: center;
}

.message-bubble {
  width: min(80%, 820px);
  padding: 16px;
  border-radius: 16px;
  box-sizing: border-box;
}

.message-bubble-user {
  background: #FDF0D5;
  color: #D81E5B;
}

.message-bubble-assistant {
  background: #C6D8D3;
  color: #3A3335;
}

.message-bubble-system {
  background: #686868;
  color: white;
}

.meta {
  margin-bottom: 8px;
  font-size: 14px;
}

.meta strong {
  font-weight: 600;
}

.message-text {
  margin: 0;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>