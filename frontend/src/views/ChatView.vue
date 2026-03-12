<script setup lang="ts">
import ChatInput from '../components/chat/ChatInput.vue'
import ChatMessageList from '../components/chat/ChatMessageList.vue'
import { useChat } from '../composables/useChat'

const { messages, isLoading, error, sendMessage } = useChat()
</script>

<template>
  <main class="chat-page">
    <section class="hero">
      <h1>Health AI Chat</h1>
      <p>Ask evidence-grounded questions about sleep, activity, and general health guidance.</p>
    </section>

    <section v-if="error" class="error">
      {{ error }}
    </section>

    <ChatMessageList :messages="messages" />

    <section class="loading" v-if="isLoading">Thinking...</section>

    <ChatInput @submit="sendMessage" />
  </main>
</template>

<style scoped>
.chat-page {
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  flex-direction: column;
}

.hero {
  margin-bottom: 10px;
}

.error {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
  background: #f87c7c;
}

.loading {
  margin: 12px 0;
  font-size: 14px;
}
</style>
