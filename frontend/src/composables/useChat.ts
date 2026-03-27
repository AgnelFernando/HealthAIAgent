import { ref, watch } from 'vue'
import { API_BASE_URL } from '../config'
import type { ChatMessage, AssistantPayload } from '../types/chat'

function createId() {
  return crypto.randomUUID()
}

export function useChat(selectedUserId: { value: string }) {
  const messages = ref<ChatMessage[]>([
    {
      id: createId(),
      role: 'system',
      text: 'Ask a personalized question about sleep, activity, or recovery.',
      createdAt: new Date().toISOString(),
    },
  ])

  const isLoading = ref(false)
  const error = ref('')

  function resetChat() {
    messages.value = [
      {
        id: createId(),
        role: 'system',
        text: 'Ask a personalized question about sleep, activity, or recovery.',
        createdAt: new Date().toISOString(),
      },
    ]
    error.value = ''
  }

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
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: selectedUserId.value,
          message: trimmed,
          days: 7,
          baseline_days: 30,
          current_day: "2025-12-10",
        }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data: AssistantPayload = await response.json()

      messages.value.push({
        id: createId(),
        role: 'assistant',
        text: data.summary || 'No response generated.',
        summary: data.summary,
        whatChanged: data.what_changed ?? [],
        guidance: data.guidance ?? [],
        citations: data.citations ?? [],
        confidence: data.confidence,
        createdAt: new Date().toISOString(),
      })
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Something went wrong.'

      messages.value.push({
        id: createId(),
        role: 'assistant',
        text: 'Sorry, I could not get a personalized response from the server.',
        createdAt: new Date().toISOString(),
      })
    } finally {
      isLoading.value = false
    }
  }

  watch(
    () => selectedUserId.value,
    () => {
      resetChat()
    }
  )

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    resetChat,
  }
}
