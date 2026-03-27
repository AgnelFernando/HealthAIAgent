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

      <template v-if="!isAssistant">
        <p class="message-text">{{ message.text }}</p>
      </template>

      <template v-else>
        <section class="assistant-section">
          <h4>Summary</h4>
          <p class="message-text">{{ message.summary || message.text }}</p>
        </section>

        <section
          v-if="message.whatChanged && message.whatChanged.length"
          class="assistant-section"
        >
          <h4>What changed in your data</h4>
          <ul class="section-list">
            <li v-for="item in message.whatChanged" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section
          v-if="message.guidance && message.guidance.length"
          class="assistant-section"
        >
          <h4>Relevant guidance</h4>
          <ul class="section-list">
            <li v-for="item in message.guidance" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section
          v-if="message.citations && message.citations.length"
          class="assistant-section"
        >
          <h4>Sources</h4>
          <CitationList :citations="message.citations" />
        </section>

        <ConfidenceBadge
          v-if="message.confidence !== undefined"
          :confidence="message.confidence"
        />
      </template>
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
  background: #fdf0d5;
  color: #d81e5b;
}

.message-bubble-assistant {
  background: #c6d8d3;
  color: #3a3335;
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

.assistant-section + .assistant-section {
  margin-top: 16px;
}

.assistant-section h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
}

.section-list {
  margin: 0;
  padding-left: 18px;
}

.section-list li + li {
  margin-top: 6px;
}
</style>
