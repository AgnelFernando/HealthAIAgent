<script setup lang="ts">
import { nextTick, onUpdated, ref } from 'vue'
import type { ChatMessage } from '../../types/chat'
import ChatMessageItem from './ChatMessageItem.vue'

defineProps<{
  messages: ChatMessage[]
}>()

const containerRef = ref<HTMLElement | null>(null)

onUpdated(async () => {
  await nextTick()
  if (containerRef.value) {
    containerRef.value.scrollTop = containerRef.value.scrollHeight
  }
})
</script>

<template>
  <div ref="containerRef" class="message-list">
    <ChatMessageItem v-for="message in messages" :key="message.id" :message="message" />
  </div>
</template>

<style scoped>
.message-list {
  height: 60vh;
  overflow-y: auto;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 12px 12px 0 0;
  background: white;
}
</style>
