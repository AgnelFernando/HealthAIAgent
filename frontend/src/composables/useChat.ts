import { ref } from 'vue'
import { API_BASE_URL } from '../config'
import type { ChatMessage, AssistantPayload } from '../types/chat'

function createId() {
  return crypto.randomUUID()
}

export function useChat() {
  const messages = ref<ChatMessage[]>([
    {
      id: createId(),
      role: 'system',
      text: 'Ask a question about sleep, activity, or health guidance.',
      createdAt: new Date().toISOString(),
    },
  ])

  const isLoading = ref(false)
  const error = ref('')

  async function sendMessage(question: string) {
    const trimmed = question.trim()
    if (!trimmed) return

    error.value = ''

    messages.value.push({
      id: createId(),
      role: 'user',
      text: trimmed,
      createdAt: new Date().toISOString(),
    })

    isLoading.value = true

    try {
      const response = await fetch(`${API_BASE_URL}/rag/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: trimmed }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data: AssistantPayload = await response.json()

      messages.value.push({
        id: createId(),
        role: 'assistant',
        text: data.answer,
        citations: data.citations ?? [],
        confidence: data.confidence,
        createdAt: new Date().toISOString(),
      })
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Something went wrong.'

      messages.value.push({
        id: createId(),
        role: 'assistant',
        text: 'Sorry, I could not get a response from the server.',
        createdAt: new Date().toISOString(),
      })
    } finally {
      isLoading.value = false
    }
  }

  return {
    messages,
    isLoading,
    error,
    sendMessage,
  }
}
