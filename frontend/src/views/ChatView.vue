<script setup lang="ts">
import { ref, watch } from 'vue'
import ChatInput from '../components/chat/ChatInput.vue'
import ChatMessageList from '../components/chat/ChatMessageList.vue'
import { useChat } from '../composables/useChat'
import { USER_OPTIONS } from '../constants/users'

const selectedUserId = ref(
  localStorage.getItem('selected_user_id') ||
    USER_OPTIONS[0]?.user_id ||
    '557975cf-2b37-4f1f-8d7e-0b80921d2db7'
)

watch(selectedUserId, (value) => {
  localStorage.setItem('selected_user_id', value)
})

const { messages, isLoading, error, sendMessage } = useChat(selectedUserId)
</script>

<template>
  <main class="chat-page">
    <section class="hero">
      <div>
        <h1>Health AI Chat</h1>
        <p>
          Ask personalized questions about sleep, recovery, and activity using
          your profile and recent health data.
        </p>
      </div>

      <label class="user-picker">
        <span>User</span>
        <select v-model="selectedUserId">
          <option
            v-for="user in USER_OPTIONS"
            :key="user.user_id"
            :value="user.user_id"
          >
            {{ user.name }}
          </option>
        </select>
      </label>
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
  height: 100%;
}

.hero {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.user-picker {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 220px;
}

.user-picker span {
  font-size: 13px;
  color: #666;
}

.user-picker select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font: inherit;
  background: white;
}

.error {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
  background: #f87c7c;
  color: white;
}

.loading {
  margin: 12px 0;
  font-size: 14px;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }

  .user-picker {
    width: 100%;
  }
}
</style>
