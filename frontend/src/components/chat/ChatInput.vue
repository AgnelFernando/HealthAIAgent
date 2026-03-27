<script setup lang="ts">
import { ref } from 'vue'
import sendIcon from '../../assets/send.svg'

const emit = defineEmits<{
  submit: [value: string]
}>()

const input = ref('')

function handleSubmit() {
  const value = input.value.trim()
  if (!value) return
  emit('submit', value)
  input.value = ''
}
</script>

<template>
  <div class="chat-input">
    <textarea
      v-model="input"
      placeholder="Ask about sleep, fatigue, recovery, or workout intensity..."
      rows="3"
      @keydown.enter.exact.prevent="handleSubmit"
    />
    <button @click="handleSubmit" type="button">
      <img :src="sendIcon" alt="Send" class="send-icon" />
    </button>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  flex-direction: row;
}

textarea {
  width: 100%;
  padding: 12px;
  resize: vertical;
  font: inherit;
  border: 0;
  border-radius: 0;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 18px;
  border: none;
  border-radius: 0 0 8px 0;
  cursor: pointer;
  background: white;
}

.send-icon {
  width: 32px;
  height: 32px;
}
</style>
