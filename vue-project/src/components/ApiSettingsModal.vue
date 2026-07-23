<script setup lang="ts">
/**
 * ApiSettingsModal.vue - 全局 API 设置弹窗（多模型，后端存储）
 */
import { ref, watch } from 'vue'
import { useApiConfig, type ApiModelConfig } from '../stores/apiConfig'

const {
  configs, activeId, showSettings, isLoading,
  addConfig, updateConfig, removeConfig, testConfig, setActive, loadConfigs,
  presetModels
} = useApiConfig()

const settingsTab = ref<'list' | 'edit'>('list')
const editingConfig = ref<Partial<ApiModelConfig> & { id?: string } | null>(null)
const isNewConfig = ref(false)
const apiStatus = ref<'idle' | 'testing' | 'success' | 'error'>('idle')
const apiStatusMsg = ref('')
const deleteConfirmId = ref<string | null>(null)
const saving = ref(false)

// 模型选择相关
const currentModel = ref('')
const customModel = ref('')
const showCustomModel = ref(false)

// 打开时加载配置
watch(showSettings, (val) => {
  if (val) {
    loadConfigs()
  }
})

// 开始编辑
const startEdit = (config: ApiModelConfig, isNew = false) => {
  editingConfig.value = { ...config }
  isNewConfig.value = isNew
  currentModel.value = config.model
  showCustomModel.value = !presetModels.find(m => m.value === config.model)
  if (showCustomModel.value) customModel.value = config.model
  apiStatus.value = 'idle'
  apiStatusMsg.value = ''
  settingsTab.value = 'edit'
}

// 添加新配置
const handleAddConfig = () => {
  startEdit({
    id: '',
    name: `模型 ${configs.length + 1}`,
    api_url: 'https://api.openai.com/v1/chat/completions',
    api_key: '',
    api_key_masked: '',
    model: 'gpt-3.5-turbo',
    temperature: 0.7,
    max_tokens: 2048,
    is_active: true,
    owner_id: '',
    created_at: '',
    updated_at: '',
  }, true)
}

// 保存配置
const handleSave = async () => {
  if (!editingConfig.value) return
  saving.value = true

  try {
    if (isNewConfig.value) {
      const newCfg = await addConfig({
        name: editingConfig.value.name || '新配置',
        api_url: editingConfig.value.api_url || '',
        api_key: editingConfig.value.api_key || '',
        model: editingConfig.value.model || 'gpt-3.5-turbo',
        temperature: editingConfig.value.temperature,
        max_tokens: editingConfig.value.max_tokens,
      })
      if (newCfg) {
        settingsTab.value = 'list'
      }
    } else if (editingConfig.value.id) {
      await updateConfig(editingConfig.value.id, {
        name: editingConfig.value.name,
        api_url: editingConfig.value.api_url,
        api_key: editingConfig.value.api_key,
        model: editingConfig.value.model,
        temperature: editingConfig.value.temperature,
        max_tokens: editingConfig.value.max_tokens,
      })
      settingsTab.value = 'list'
    }
  } finally {
    saving.value = false
  }
}

// 返回列表
const backToList = () => {
  settingsTab.value = 'list'
  editingConfig.value = null
}

const onModelChange = () => {
  if (!editingConfig.value) return
  if (currentModel.value === '') {
    showCustomModel.value = true
  } else {
    showCustomModel.value = false
    editingConfig.value.model = currentModel.value
  }
}

const applyCustomModel = () => {
  if (!editingConfig.value) return
  if (customModel.value.trim()) {
    editingConfig.value.model = customModel.value.trim()
    currentModel.value = ''
  }
}

// 测试 API
const handleTest = async () => {
  if (!editingConfig.value?.id) return
  apiStatus.value = 'testing'
  apiStatusMsg.value = '测试中...'

  const result = await testConfig(editingConfig.value.id)
  apiStatus.value = result.success ? 'success' : 'error'
  apiStatusMsg.value = result.success ? '✓ 连接成功！' : `✕ ${result.message}`
}

// 删除确认
const confirmDelete = (id: string) => { deleteConfirmId.value = id }

const doDelete = async (id: string) => {
  await removeConfig(id)
  deleteConfirmId.value = null
  if (editingConfig.value?.id === id) {
    backToList()
  }
}

const handleSetActive = (id: string) => { setActive(id) }

const close = () => {
  showSettings.value = false
  settingsTab.value = 'list'
  editingConfig.value = null
}

const getModelLabel = (model: string) => {
  const found = presetModels.find(m => m.value === model)
  return found ? found.label : model
}
</script>

<template>
  <Teleport to="body">
    <div v-if="showSettings" class="modal-overlay" @click.self="close">
      <div class="modal">
        <div class="modal-header">
          <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="vertical-align: -3px"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> API 设置</h2>
          <button class="modal-close" @click="close">✕</button>
        </div>

        <div class="modal-body">
          <!-- 加载中 -->
          <div v-if="isLoading" class="loading-state">
            <p>加载配置中...</p>
          </div>

          <!-- ====== 配置列表视图 ====== -->
          <div v-if="settingsTab === 'list'" class="config-list-view">
            <div class="list-header">
              <span class="list-count">已配置 {{ configs.length }} 个模型</span>
              <button class="btn-add" @click="handleAddConfig">＋ 添加模型</button>
            </div>

            <div v-if="configs.length === 0" class="empty-state">
              <p>暂无模型配置</p>
              <p>点击上方按钮添加你的第一个 API 配置</p>
            </div>

            <div
              v-for="cfg in configs"
              :key="cfg.id"
              class="config-card"
              :class="{ active: cfg.id === activeId }"
            >
              <div class="card-main" @click="handleSetActive(cfg.id)">
                <div class="card-radio">
                  <div class="radio-dot" :class="{ checked: cfg.id === activeId }"></div>
                </div>
                <div class="card-info">
                  <div class="card-name">{{ cfg.name }}</div>
                  <div class="card-meta">
                    <span class="meta-model">{{ getModelLabel(cfg.model) }}</span>
                    <span class="meta-dot">·</span>
                    <span class="meta-key">{{ cfg.api_key_masked || '未配置' }}</span>
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-btn" @click.stop="startEdit(cfg)" title="编辑"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>
                <button
                  v-if="configs.length > 1"
                  class="action-btn danger"
                  @click.stop="confirmDelete(cfg.id)"
                  title="删除"
                ><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
              </div>

              <div v-if="deleteConfirmId === cfg.id" class="delete-confirm">
                <span>确认删除「{{ cfg.name }}」？</span>
                <button class="del-yes" @click="doDelete(cfg.id)">删除</button>
                <button class="del-no" @click="deleteConfirmId = null">取消</button>
              </div>
            </div>
          </div>

          <!-- ====== 编辑视图 ====== -->
          <div v-if="settingsTab === 'edit' && editingConfig" class="config-edit-view">
            <div class="edit-back" @click="backToList">← 返回列表</div>

            <div class="form-group">
              <label>配置名称</label>
              <input v-model="editingConfig.name" type="text" placeholder="如：我的 GPT-4" class="form-input" />
            </div>

            <div class="form-group">
              <label>API 地址</label>
              <input v-model="editingConfig.api_url" type="text" placeholder="https://api.openai.com/v1/chat/completions" class="form-input" />
              <span class="form-hint">OpenAI 兼容接口地址</span>
            </div>

            <div class="form-group">
              <label>API Key</label>
              <input v-model="editingConfig.api_key" type="password" placeholder="sk-..." class="form-input" />
              <span v-if="!isNewConfig && editingConfig.id" class="form-hint">留空则保持原有 Key 不变</span>
            </div>

            <div class="form-group">
              <label>模型</label>
              <select v-model="currentModel" @change="onModelChange" class="form-input">
                <option v-for="m in presetModels" :key="m.value" :value="m.value">{{ m.label }}</option>
              </select>
              <div v-if="showCustomModel" class="custom-model">
                <input v-model="customModel" @blur="applyCustomModel" placeholder="输入模型名称，如 gpt-4-turbo" class="form-input" />
              </div>
            </div>

            <div class="form-group">
              <label>Temperature（创造性）: {{ editingConfig.temperature }}</label>
              <input v-model.number="editingConfig.temperature" type="range" min="0" max="2" step="0.1" class="form-range" />
              <div class="range-labels"><span>精确 0</span><span>平衡 1</span><span>发散 2</span></div>
            </div>

            <div class="form-group">
              <label>Max Tokens（最大回复长度）: {{ editingConfig.max_tokens }}</label>
              <input v-model.number="editingConfig.max_tokens" type="range" min="256" max="8192" step="256" class="form-range" />
              <div class="range-labels"><span>256</span><span>4096</span><span>8192</span></div>
            </div>

            <div class="edit-actions">
              <button
                v-if="editingConfig.id"
                class="test-btn"
                @click="handleTest"
                :disabled="!editingConfig.api_key || apiStatus === 'testing'"
              >
                {{ apiStatus === 'testing' ? '测试中...' : '测试连接' }}
              </button>
              <span v-if="apiStatusMsg" class="test-status" :class="apiStatus">{{ apiStatusMsg }}</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="footer-left">
            <span v-if="settingsTab === 'list'" class="footer-hint">选中的模型将用于 AI 对话</span>
            <span v-else class="footer-hint"></span>
          </div>
          <div class="footer-right">
            <button v-if="settingsTab === 'edit'" class="btn-save" @click="handleSave" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
            <button class="btn-done" @click="close">完成</button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(2px); }
.modal { background: white; border-radius: 16px; width: 560px; max-width: 92vw; max-height: 85vh; display: flex; flex-direction: column; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px 16px; }
.modal-header h2 { margin: 0; font-size: 18px; color: #1e293b; }
.modal-close { width: 32px; height: 32px; border: none; background: #f1f5f9; border-radius: 8px; cursor: pointer; font-size: 16px; color: #64748b; display: flex; align-items: center; justify-content: center; }
.modal-close:hover { background: #e2e8f0; }
.modal-body { padding: 0 24px; overflow-y: auto; flex: 1; }

.login-hint, .loading-state { text-align: center; padding: 40px 0; color: #64748b; }

/* 列表视图 */
.list-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.list-count { font-size: 13px; color: #94a3b8; }
.btn-add { padding: 6px 14px; background: #6c63ff; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-add:hover { background: #5b54e6; }

.empty-state { text-align: center; padding: 40px 0; color: #94a3b8; }
.empty-state p { margin: 4px 0; }
.empty-state p:first-child { font-size: 16px; }

.config-card { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border: 2px solid #e5e7eb; border-radius: 10px; margin-bottom: 8px; transition: all 0.15s; position: relative; }
.config-card:hover { border-color: #c7d2fe; }
.config-card.active { border-color: #6c63ff; background: #f5f3ff; }

.card-main { display: flex; align-items: center; gap: 12px; cursor: pointer; flex: 1; min-width: 0; }
.card-radio { flex-shrink: 0; }
.radio-dot { width: 18px; height: 18px; border: 2px solid #d1d5db; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
.radio-dot.checked { border-color: #6c63ff; }
.radio-dot.checked::after { content: ''; width: 10px; height: 10px; border-radius: 50%; background: #6c63ff; }

.card-info { min-width: 0; }
.card-name { font-size: 14px; font-weight: 600; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-meta { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #94a3b8; margin-top: 2px; }
.meta-model { color: #6c63ff; font-weight: 500; }
.meta-dot { color: #d1d5db; }

.card-actions { display: flex; gap: 4px; flex-shrink: 0; margin-left: 8px; }
.action-btn { width: 30px; height: 30px; border: 1px solid #e5e7eb; border-radius: 6px; background: white; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; }
.action-btn:hover { background: #f1f5f9; }
.action-btn.danger:hover { background: #fef2f2; border-color: #fecaca; }

.delete-confirm { position: absolute; inset: 0; background: rgba(254,242,242,0.95); border-radius: 10px; display: flex; align-items: center; gap: 10px; padding: 0 14px; font-size: 13px; color: #991b1b; z-index: 1; }
.del-yes { padding: 4px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: 600; }
.del-no { padding: 4px 12px; background: white; color: #64748b; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 12px; cursor: pointer; }

/* 编辑视图 */
.edit-back { font-size: 13px; color: #6c63ff; cursor: pointer; margin-bottom: 16px; font-weight: 500; }
.edit-back:hover { text-decoration: underline; }

.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.form-group label { font-size: 13px; font-weight: 600; color: #374151; }
.form-input { padding: 10px 14px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 14px; transition: border-color 0.2s; font-family: inherit; }
.form-input:focus { outline: none; border-color: #6c63ff; }
.form-hint { font-size: 12px; color: #94a3b8; }
select.form-input { cursor: pointer; }
.custom-model { margin-top: 6px; }
.form-range { width: 100%; accent-color: #6c63ff; cursor: pointer; }
.range-labels { display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; }

.edit-actions { display: flex; align-items: center; gap: 12px; padding-top: 4px; }
.test-btn { padding: 8px 16px; border: 2px solid #6c63ff; background: white; color: #6c63ff; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; }
.test-btn:hover:not(:disabled) { background: #f5f3ff; }
.test-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.test-status { font-size: 13px; }
.test-status.success { color: #10b981; }
.test-status.error { color: #ef4444; }
.test-status.testing { color: #6c63ff; }

/* 底部 */
.modal-footer { display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; border-top: 1px solid #e5e7eb; }
.footer-hint { font-size: 12px; color: #94a3b8; }
.footer-right { display: flex; gap: 8px; }
.btn-save { padding: 8px 16px; background: #10b981; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-save:hover:not(:disabled) { background: #059669; }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-done { padding: 8px 20px; background: #6c63ff; color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-done:hover { background: #5b54e6; }
</style>
