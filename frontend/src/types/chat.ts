export interface Citation {
  title: string
  url: string
  similarity?: number
}

export interface AssistantPayload {
  answer: string
  citations: Citation[]
  confidence?: number
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  text: string
  citations?: Citation[]
  confidence?: number
  createdAt: string
}
