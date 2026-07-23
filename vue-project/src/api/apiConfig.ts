/**
 * API 配置 API 服务
 * 管理 AI API 配置，通过后端保存
 */

const API_BASE = 'http://localhost:8000/api/v1'

// 获取存储的 token（可选）
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

  // 如果有 token 才添加认证头（可选）
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

  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}

// ==================== 类型定义 ====================

export interface ApiModelConfig {
  id: string
  owner_id: string
  name: string
  api_url: string
  api_key: string       // 详情接口返回完整 key
  api_key_masked?: string // 列表接口返回脱敏 key
  model: string
  temperature: number
  max_tokens: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ApiConfigListResponse {
  items: ApiModelConfig[]
  total: number
}

// ==================== API 方法 ====================

/**
 * 获取所有 API 配置
 */
export const getApiConfigs = async (): Promise<ApiConfigListResponse> => {
  return request<ApiConfigListResponse>('/api-configs')
}

/**
 * 获取单个 API 配置详情（包含完整 API Key）
 */
export const getApiConfig = async (id: string): Promise<ApiModelConfig> => {
  return request<ApiModelConfig>(`/api-configs/${id}`)
}

/**
 * 创建新的 API 配置
 */
export const createApiConfig = async (data: {
  name: string
  api_url: string
  api_key: string
  model: string
  temperature?: number
  max_tokens?: number
}): Promise<ApiModelConfig> => {
  return request<ApiModelConfig>('/api-configs', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * 更新 API 配置
 */
export const updateApiConfig = async (
  id: string,
  data: {
    name?: string
    api_url?: string
    api_key?: string
    model?: string
    temperature?: number
    max_tokens?: number
    is_active?: boolean
  }
): Promise<ApiModelConfig> => {
  return request<ApiModelConfig>(`/api-configs/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/**
 * 删除 API 配置
 */
export const deleteApiConfig = async (id: string): Promise<void> => {
  return request<void>(`/api-configs/${id}`, {
    method: 'DELETE',
  })
}

/**
 * 测试 API 配置
 */
export const testApiConfig = async (
  id: string
): Promise<{ success: boolean; message: string }> => {
  return request<{ success: boolean; message: string }>(
    `/api-configs/${id}/test`,
    { method: 'POST' }
  )
}

/**
 * 使用指定配置发送聊天消息
 */
export const sendChatWithConfig = async (
  message: string,
  apiConfigId: string,
  conversationId?: string
): Promise<{ conversation_id: string; message: { role: string; content: string } }> => {
  return request('/chat/with-config', {
    method: 'POST',
    body: JSON.stringify({
      message,
      api_config_id: apiConfigId,
      conversation_id: conversationId,
    }),
  })
}
