export interface Citation {
  title: string
  url: string
  similarity?: number
}

export interface AssistantPayload {
  summary: string
  what_changed: string[]
  guidance: string[]
  citations: Citation[]
  confidence?: number
  metrics?: Record<string, unknown> | null
  flags?: unknown[]
  changes?: Record<string, unknown> | null
  profile?: Record<string, unknown> | null
  sleep_analysis?: Record<string, unknown> | null
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  text: string
  summary?: string
  whatChanged?: string[]
  guidance?: string[]
  citations?: Citation[]
  confidence?: number
  createdAt: string
}