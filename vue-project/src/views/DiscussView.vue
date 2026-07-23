<script setup lang="ts">
/**
 * DiscussView.vue - 思路交流 / AI 对话页面
 * 与 AI 进行创作思路对话，使用全局 API 配置
 */
import { ref, nextTick, computed } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'
import { useApiConfig } from '../stores/apiConfig'
import { sendChatWithConfig } from '../api/apiConfig'

const { configs, activeId, activeConfig, showSettings, presetModels } = useApiConfig()
const showNoApiKeyHint = ref(false)

// 当前模型显示名
const currentModelLabel = computed(() => {
  if (!activeConfig.value) return ''
  const found = presetModels.find(m => m.value === activeConfig.value!.model)
  return found ? found.label : activeConfig.value.model
})

// 是否已配置 API（后端返回 api_key_masked，如果为空说明未配置）
const isConfigured = computed(() => {
  if (!activeConfig.value) return false
  // 如果有完整的 api_key 说明已配置（详情接口返回）
  // 如果 api_key_masked 不为空也说明已配置（列表接口返回）
  return !!activeConfig.value.api_key || (!!activeConfig.value.api_key_masked && activeConfig.value.api_key_masked !== '')
})

// ========== 对话状态 ==========
interface Message {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
  loading?: boolean
  error?: boolean
}

const messages = ref<Message[]>([
  {
    id: 1,
    role: 'assistant',
    content: '你好！我是你的创作灵感助手\n\n你可以跟我聊聊：\n- 你正在构思的故事设定\n- 遇到的创作瓶颈\n- 想要探讨的情节走向\n- 人物塑造的困惑\n\n请先在顶部导航栏 API 设置中配置你的 API，然后我们就可以开始对话了！',
    timestamp: Date.now()
  }
])

const userInput = ref('')
const chatContainer = ref<HTMLDivElement | null>(null)
const isGenerating = ref(false)

// ========== 发送消息 ==========
let messageIdCounter = 2

const sendMessage = async () => {
  const text = userInput.value.trim()
  if (!text || isGenerating.value) return
  if (!activeConfig.value) {
    showNoApiKeyHint.value = true
    return
  }

  const cfg = activeConfig.value

  // 添加用户消息
  const userMsg: Message = {
    id: messageIdCounter++,
    role: 'user',
    content: text,
    timestamp: Date.now()
  }
  messages.value.push(userMsg)
  userInput.value = ''
  await scrollToBottom()

  // 添加助手占位消息
  const assistantMsg: Message = {
    id: messageIdCounter++,
    role: 'assistant',
    content: '',
    timestamp: Date.now(),
    loading: true
  }
  messages.value.push(assistantMsg)
  await scrollToBottom()

  isGenerating.value = true

  try {
    // 通过后端 API 调用用户配置的 AI
    const data = await sendChatWithConfig(text, cfg.id)
    const reply = data.message?.content || '抱歉，我没有收到回复内容。'

    assistantMsg.content = reply
    assistantMsg.loading = false
  } catch (err: any) {
    assistantMsg.content = `请求出错：${err.message}\n\n请检查顶部 API 设置是否正确。`
    assistantMsg.error = true
    assistantMsg.loading = false
  } finally {
    isGenerating.value = false
    await scrollToBottom()
  }
}

// ========== 工具函数 ==========
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const clearChat = () => {
  messages.value = [{
    id: messageIdCounter++,
    role: 'assistant',
    content: '对话已清空。有什么创作问题想聊的吗？',
    timestamp: Date.now()
  }]
}

const formatTime = (ts: number) => {
  const d = new Date(ts)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 简单的 markdown 转 HTML
const formatMessage = (text: string): string => {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <!-- 顶栏 -->
      <header class="page-header">
        <div class="header-left">
          <span class="header-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>
          <h1 class="page-title">思路交流</h1>
          <span class="header-sub">AI 创作对话</span>
        </div>
        <div class="header-right">
          <!-- 当前 API 信息显示 -->
          <div v-if="activeConfig" class="api-badge" :class="{ configured: isConfigured }" @click="showSettings = true" title="点击修改 API 设置">
            <span class="api-badge-dot"></span>
            <span class="api-badge-name">{{ activeConfig.name }}</span>
            <span class="api-badge-model">{{ currentModelLabel }}</span>
          </div>
          <button class="header-btn" @click="clearChat" title="清空对话"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
        </div>
      </header>

      <!-- 对话区域 -->
      <div class="chat-area" ref="chatContainer">
        <div v-for="msg in messages" :key="msg.id" class="message" :class="[msg.role, { error: msg.error, loading: msg.loading }]">
          <div class="msg-avatar">
            {{ msg.role === 'user' ? 'U' : 'AI' }}
          </div>
          <div class="msg-body">
            <div class="msg-content" v-if="!msg.loading">
              <div class="msg-text" v-html="formatMessage(msg.content)"></div>
            </div>
            <div v-else class="msg-loading">
              <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            </div>
            <div class="msg-time">{{ formatTime(msg.timestamp) }}</div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <!-- 未配置 API Key 的醒目提示 -->
        <div v-if="showNoApiKeyHint" class="no-api-dialog">
          <div class="no-api-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="32" height="32"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div>
          <div class="no-api-text">
            <strong>尚未配置 API Key</strong>
            <p>请先配置 API 才能与 AI 助手对话。点击下方按钮前往设置。</p>
          </div>
          <div class="no-api-actions">
            <button class="no-api-btn-primary" @click="showSettings = true; showNoApiKeyHint = false">前往设置</button>
            <button class="no-api-btn-secondary" @click="showNoApiKeyHint = false">关闭</button>
          </div>
        </div>

        <div v-if="!isConfigured && !showNoApiKeyHint" class="input-hint">
          尚未配置 API，点击发送时将提示你前往设置
        </div>
        <div class="input-row">
          <textarea
            v-model="userInput"
            @keydown="handleKeydown"
            :disabled="isGenerating"
            placeholder="聊聊你的创作灵感... (Enter 发送，Shift+Enter 换行)"
            rows="1"
            class="chat-input"
          />
          <button
            class="send-btn"
            @click="sendMessage"
            :disabled="!userInput.trim() || isGenerating"
          >
            <span v-if="isGenerating" class="btn-loading">⏳</span>
            <span v-else>发送</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-layout { display: flex; width: calc(100% + 4rem); margin-left: -2rem; margin-top: -2rem; height: calc(100vh - 50px); background: #f5f7fa; overflow: hidden; }
.content-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }

/* Header */
.page-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; background: white; border-bottom: 1px solid #e5e7eb; flex-shrink: 0; }
.header-left { display: flex; align-items: center; gap: 10px; }
.header-icon { font-size: 22px; }
.page-title { font-size: 20px; font-weight: 700; color: #1e293b; margin: 0; }
.header-sub { font-size: 13px; color: #94a3b8; margin-left: 4px; }
.header-actions { display: flex; gap: 8px; }
.header-right { display: flex; align-items: center; gap: 8px; }
.header-btn { width: 36px; height: 36px; border: 1px solid #e5e7eb; border-radius: 8px; background: white; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
.header-btn:hover { background: #f1f5f9; border-color: #cbd5e1; }

/* API Badge */
.api-badge { display: flex; align-items: center; gap: 6px; padding: 6px 12px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; transition: all 0.15s; font-size: 12px; }
.api-badge:hover { background: #e2e8f0; }
.api-badge.configured { background: #ecfdf5; border-color: #a7f3d0; }
.api-badge-dot { width: 7px; height: 7px; border-radius: 50%; background: #ef4444; flex-shrink: 0; }
.api-badge.configured .api-badge-dot { background: #10b981; }
.api-badge-name { font-weight: 600; color: #334155; }
.api-badge-model { color: #6c63ff; }

/* Chat Area */
.chat-area { flex: 1; overflow-y: auto; padding: 24px 32px; display: flex; flex-direction: column; gap: 16px; }

.message { display: flex; gap: 12px; max-width: 85%; }
.message.user { align-self: flex-end; flex-direction: row-reverse; }
.message.assistant { align-self: flex-start; }

.msg-avatar { width: 36px; height: 36px; border-radius: 50%; background: #f1f5f9; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.message.user .msg-avatar { background: #ede9fe; }

.msg-body { display: flex; flex-direction: column; gap: 4px; }
.message.user .msg-body { align-items: flex-end; }

.msg-content { padding: 12px 16px; border-radius: 16px; font-size: 14px; line-height: 1.7; word-break: break-word; }
.message.user .msg-content { background: #6c63ff; color: white; border-bottom-right-radius: 4px; }
.message.assistant .msg-content { background: white; color: #334155; border: 1px solid #e5e7eb; border-bottom-left-radius: 4px; }
.message.error .msg-content { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.msg-text :deep(code) { background: rgba(0,0,0,0.06); padding: 1px 4px; border-radius: 3px; font-size: 13px; }
.message.user .msg-text :deep(code) { background: rgba(255,255,255,0.2); }

.msg-time { font-size: 11px; color: #94a3b8; padding: 0 4px; }

/* Loading dots */
.msg-loading { display: flex; gap: 4px; padding: 16px 20px; background: white; border: 1px solid #e5e7eb; border-radius: 16px; border-bottom-left-radius: 4px; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1; animation: bounce 1.4s infinite ease-in-out; }
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

/* Input Area */
.input-area { padding: 16px 32px 20px; background: white; border-top: 1px solid #e5e7eb; flex-shrink: 0; }
.input-hint { text-align: center; font-size: 13px; color: #f59e0b; margin-bottom: 8px; }

/* No API Key Dialog */
.no-api-dialog { display: flex; align-items: center; gap: 16px; padding: 16px 20px; background: #fef3c7; border: 2px solid #fbbf24; border-radius: 12px; margin-bottom: 12px; }
.no-api-icon { font-size: 28px; flex-shrink: 0; }
.no-api-text { flex: 1; }
.no-api-text strong { color: #92400e; font-size: 15px; }
.no-api-text p { margin: 4px 0 0; color: #a16207; font-size: 13px; }
.no-api-actions { display: flex; gap: 8px; flex-shrink: 0; }
.no-api-btn-primary { padding: 8px 16px; background: #6c63ff; color: white; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; white-space: nowrap; }
.no-api-btn-primary:hover { background: #5b54e6; }
.no-api-btn-secondary { padding: 8px 14px; background: white; color: #92400e; border: 1px solid #fbbf24; border-radius: 8px; font-size: 13px; cursor: pointer; }
.no-api-btn-secondary:hover { background: #fef9e3; }
.input-row { display: flex; gap: 10px; align-items: flex-end; }
.chat-input { flex: 1; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 14px; line-height: 1.5; resize: none; font-family: inherit; transition: border-color 0.2s; min-height: 44px; max-height: 120px; }
.chat-input:focus { outline: none; border-color: #6c63ff; }
.chat-input:disabled { background: #f9fafb; }
.send-btn { padding: 12px 24px; background: #6c63ff; color: white; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s; white-space: nowrap; height: 44px; }
.send-btn:hover:not(:disabled) { background: #5b54e6; }
.send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-loading { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>
