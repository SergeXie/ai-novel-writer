/**
 * 小说项目 API 服务
 * 封装所有与小说项目和章节相关的 API 请求
 */

// API 基础地址
const API_BASE = 'http://localhost:8000/api/v1'

// 获取存储的 token
const getToken = (): string | null => {
  return localStorage.getItem('token')
}

// 通用请求方法
const request = async <T>(
  url: string,
  options: RequestInit = {}
): Promise<T> => {
  const token = getToken()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }

  // 如果有 token 才添加认证头
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(error.detail || '请求失败')
  }

  // 204 No Content
  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}

// ==================== 类型定义 ====================

export interface NovelProject {
  id: string
  title: string
  description: string | null
  genre: string | null
  cover_image: string | null
  status: string
  owner_id: string
  created_at: string
  updated_at: string
}

export interface NovelProjectDetail extends NovelProject {
  chapters: Chapter[]
}

export interface Chapter {
  id: string
  title: string
  content: string | null
  chapter_number: number
  word_count: number
  status: string
  project_id: string
  created_at: string
  updated_at: string
}

export interface ProjectListResponse {
  items: NovelProject[]
  total: number
  page: number
  page_size: number
}

export interface ChapterListResponse {
  items: Chapter[]
  total: number
}

// ==================== 项目 API ====================

/**
 * 获取项目列表
 */
export const getProjects = async (
  page: number = 1,
  pageSize: number = 20
): Promise<ProjectListResponse> => {
  return request<ProjectListResponse>(
    `/projects?page=${page}&page_size=${pageSize}`
  )
}

/**
 * 获取项目详情（包含章节）
 */
export const getProject = async (
  projectId: string
): Promise<NovelProjectDetail> => {
  return request<NovelProjectDetail>(`/projects/${projectId}`)
}

/**
 * 创建项目
 */
export const createProject = async (data: {
  title: string
  description?: string
  genre?: string
}): Promise<NovelProject> => {
  return request<NovelProject>('/projects', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * 更新项目
 */
export const updateProject = async (
  projectId: string,
  data: {
    title?: string
    description?: string
    genre?: string
    cover_image?: string
    status?: string
  }
): Promise<NovelProject> => {
  return request<NovelProject>(`/projects/${projectId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/**
 * 删除项目
 */
export const deleteProject = async (projectId: string): Promise<void> => {
  return request<void>(`/projects/${projectId}`, {
    method: 'DELETE',
  })
}

// ==================== 章节 API ====================

/**
 * 获取项目的所有章节
 */
export const getChapters = async (
  projectId: string
): Promise<ChapterListResponse> => {
  return request<ChapterListResponse>(`/projects/${projectId}/chapters`)
}

/**
 * 获取单个章节
 */
export const getChapter = async (
  projectId: string,
  chapterId: string
): Promise<Chapter> => {
  return request<Chapter>(
    `/projects/${projectId}/chapters/${chapterId}`
  )
}

/**
 * 创建章节
 */
export const createChapter = async (
  projectId: string,
  data: {
    title: string
    content?: string
    chapter_number: number
  }
): Promise<Chapter> => {
  return request<Chapter>(`/projects/${projectId}/chapters`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * 更新章节
 */
export const updateChapter = async (
  projectId: string,
  chapterId: string,
  data: {
    title?: string
    content?: string
    chapter_number?: number
    status?: string
  }
): Promise<Chapter> => {
  return request<Chapter>(
    `/projects/${projectId}/chapters/${chapterId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    }
  )
}

/**
 * 删除章节
 */
export const deleteChapter = async (
  projectId: string,
  chapterId: string
): Promise<void> => {
  return request<void>(
    `/projects/${projectId}/chapters/${chapterId}`,
    {
      method: 'DELETE',
    }
  )
}

// ==================== AI 聊天 API ====================

export interface ChatMessage {
  role: string
  content: string
  timestamp?: string
}

export interface ChatResponse {
  conversation_id: string
  message: ChatMessage
}

/**
 * 发送聊天消息
 */
export const sendChatMessage = async (
  message: string,
  conversationId?: string,
  projectId?: string
): Promise<ChatResponse> => {
  return request<ChatResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      project_id: projectId,
    }),
  })
}

/**
 * 发送流式聊天消息
 */
export const streamChatMessage = async (
  message: string,
  onChunk: (content: string) => void,
  conversationId?: string,
  projectId?: string
): Promise<void> => {
  const token = getToken()
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      project_id: projectId,
    }),
  })

  if (!response.ok) {
    throw new Error('请求失败')
  }

  const reader = response.body?.getReader()
  if (!reader) return

  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    const lines = chunk.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data === '[DONE]') return

        try {
          const parsed = JSON.parse(data)
          if (parsed.content) {
            onChunk(parsed.content)
          }
        } catch {
          // 忽略解析错误
        }
      }
    }
  }
}
