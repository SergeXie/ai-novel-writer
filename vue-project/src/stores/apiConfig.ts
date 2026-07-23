/**
 * API 全局配置 Store
 * 支持多模型配置，通过后端保存，前端缓存
 */
import { reactive, ref, computed } from 'vue'
import {
  getApiConfigs,
  createApiConfig,
  updateApiConfig,
  deleteApiConfig,
  testApiConfig,
  type ApiModelConfig,
} from '../api/apiConfig'

export type { ApiModelConfig }

const ACTIVE_KEY = 'ai-api-active-id'

// 全局配置列表
const configs = reactive<ApiModelConfig[]>([])

// 当前激活的配置 ID
const activeId = ref<string | null>(localStorage.getItem(ACTIVE_KEY))

// 设置弹窗的显示状态
const showSettings = ref(false)

// 加载状态
const isLoading = ref(false)

// 当前激活的配置（响应式）
const activeConfig = computed(() => {
  return configs.find(c => c.id === activeId.value) || configs[0] || null
})

// 监听激活 ID 变化
const setActive = (id: string) => {
  activeId.value = id
  localStorage.setItem(ACTIVE_KEY, id)
}

// 从后端加载配置
export async function loadConfigs(): Promise<void> {
  isLoading.value = true
  try {
    const res = await getApiConfigs()
    configs.splice(0, configs.length, ...res.items)

    // 如果激活 ID 无效，设为第一个
    if (!activeId.value || !configs.find(c => c.id === activeId.value)) {
      if (configs.length > 0) {
        setActive(configs[0].id)
      }
    }
  } catch (err) {
    console.error('加载 API 配置失败:', err)
  } finally {
    isLoading.value = false
  }
}

// 创建配置（通过后端）
export async function addConfig(data: {
  name: string
  api_url: string
  api_key: string
  model: string
  temperature?: number
  max_tokens?: number
}): Promise<ApiModelConfig | null> {
  try {
    const newCfg = await createApiConfig(data)
    configs.unshift(newCfg)
    if (!activeId.value) {
      setActive(newCfg.id)
    }
    return newCfg
  } catch (err) {
    console.error('创建 API 配置失败:', err)
    return null
  }
}

// 更新配置（通过后端）
export async function updateConfig(
  id: string,
  data: {
    name?: string
    api_url?: string
    api_key?: string
    model?: string
    temperature?: number
    max_tokens?: number
  }
): Promise<ApiModelConfig | null> {
  try {
    const updated = await updateApiConfig(id, data)
    const index = configs.findIndex(c => c.id === id)
    if (index !== -1) {
      configs[index] = updated
    }
    return updated
  } catch (err) {
    console.error('更新 API 配置失败:', err)
    return null
  }
}

// 删除配置（通过后端）
export async function removeConfig(id: string): Promise<boolean> {
  try {
    await deleteApiConfig(id)
    const index = configs.findIndex(c => c.id === id)
    if (index !== -1) {
      configs.splice(index, 1)
    }
    // 如果删除的是当前激活的，切换到第一个
    if (activeId.value === id) {
      if (configs.length > 0) {
        setActive(configs[0].id)
      } else {
        activeId.value = null
        localStorage.removeItem(ACTIVE_KEY)
      }
    }
    return true
  } catch (err) {
    console.error('删除 API 配置失败:', err)
    return false
  }
}

// 测试配置
export async function testConfig(
  id: string
): Promise<{ success: boolean; message: string }> {
  try {
    return await testApiConfig(id)
  } catch (err: any) {
    return { success: false, message: err.message }
  }
}

// 导出 composable
export function useApiConfig() {
  return {
    configs,
    activeId,
    activeConfig,
    showSettings,
    isLoading,
    loadConfigs,
    addConfig,
    updateConfig,
    removeConfig,
    testConfig,
    setActive,
    /** 预设模型列表 */
    presetModels: [
      { label: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo' },
      { label: 'GPT-4', value: 'gpt-4' },
      { label: 'GPT-4o', value: 'gpt-4o' },
      { label: 'GPT-4o Mini', value: 'gpt-4o-mini' },
      { label: 'Claude 3.5 Sonnet', value: 'claude-3-5-sonnet-20241022' },
      { label: 'DeepSeek Chat', value: 'deepseek-chat' },
      { label: '自定义', value: '' },
    ] as { label: string; value: string }[]
  }
}
