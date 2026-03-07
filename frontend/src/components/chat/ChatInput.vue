<script setup lang="ts">
import { ref } from 'vue'

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
      placeholder="Ask about sleep, activity, or health guidance..."
      rows="3"
      @keydown.enter.exact.prevent="handleSubmit"
    />
    <button @click="handleSubmit">Send</button>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

textarea {
  width: 100%;
  padding: 12px;
  resize: vertical;
  font: inherit;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  align-self: flex-end;
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
