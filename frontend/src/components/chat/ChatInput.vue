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
      placeholder="Ask about sleep, activity, or health guidance..."
      rows="3"
      @keydown.enter.exact.prevent="handleSubmit"
    />
    <button @click="handleSubmit">
      <img :src="sendIcon" alt="Send" class="send-icon"/>
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
  border: 0px solid #ccc;
  border-radius: 0;
}

button {
  align-self: flex-end;
  padding: 10px 18px;
  border: none;
  border-radius: 0 0 8px 0;
  cursor: pointer;
  height: stretch;
  background: white;
}
.send-icon {
  width: 40px;
  height: 40px;
}
</style>
