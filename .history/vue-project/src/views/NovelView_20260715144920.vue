<script setup lang="ts">
/**
 * NovelView.vue - AI 写小说主界面
 * 模拟类似 Cursor/Claude 的桌面软件布局
 */
import { ref, nextTick } from 'vue'

// 侧边栏折叠状态
const sidebarCollapsed = ref(false)

// 当前选中的项目
const selectedProject = ref('novelAi')

// 当前选中的对话
const selectedConversation = ref<string | null>(null)

// 输入框内容
const inputValue = ref('')

// 请求模式
const requestMode = ref('普通')

// 项目列表数据
const projects = ref([
  {
    name: 'outputs',
    conversations: [
      { id: '1', title: '你是什么模型', time: '6 天' },
      { id: '2', title: '我要实现"小三班下学期成长档...', time: '6 天' },
    ]
  },
  {
    name: 'novelAi',
    conversations: [
      { id: '3', title: '更新项目架构', time: '6 天' },
      { id: '4', title: '帮我更新项目架构', time: '6 天' },
      { id: '5', title: '项目架构是怎么样的', time: '1 周' },
    ]
  },
  {
    name: 'TestNoval',
    conversations: [
      { id: '6', title: '文件有什么', time: '1 周' },
    ]
  }
])

// 独立对话列表
const standaloneConversations = ref([
  { id: '7', title: '你有什么agent', time: '3 天' },
  { id: '8', title: '你能做ppt吗', time: '6 天' },
  { id: '9', title: '我想要一个skills，你先找找有没有...', time: '6 天' },
])

// 上下文列表（输入框下方的标签）
const contextItems = ref([
  { type: 'folder', name: 'outputs' },
  { type: 'folder', name: 'novelAi' },
])

// 聊天消息
const messages = ref<Array<{role: string, content: string}>>([])

// 发送消息
const sendMessage = () => {
  if (!inputValue.value.trim()) return
  
  messages.value.push({
    role: 'user',
    content: inputValue.value
  })
  
  const userMessage = inputValue.value
  inputValue.value = ''
  
  // 模拟 AI 回复
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: `收到您的消息："${userMessage}"。我正在分析您的需求，请稍候...`
    })
  }, 1000)
}

// 新建对话
const newConversation = () => {
  selectedConversation.value = null
  messages.value = []
  inputValue.value = ''
}

// 选择对话
const selectConversation = (id: string) => {
  selectedConversation.value = id
}

// 切换侧边栏
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// 添加上下文
const addContext = () => {
  // 模拟添加上下文功能
}

// 切换请求模式
const toggleRequestMode = () => {
  const modes = ['普通', '高', '极速']
  const currentIndex = modes.indexOf(requestMode.value)
  requestMode.value = modes[(currentIndex + 1) % modes.length]
}

// 快捷键处理
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}


</script>

<template>
  <div class="novel-app">
    <!-- 左侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- 顶部菜单 -->
      <div class="sidebar-menu">
        <button class="menu-btn" @click="newConversation">
          <span class="icon">✏️</span>
          <span class="text" v-if="!sidebarCollapsed">新对话</span>
        </button>
        <button class="menu-btn">
          <span class="icon">🔍</span>
          <span class="text" v-if="!sidebarCollapsed">搜索</span>
        </button>
        <button class="menu-btn">
          <span class="icon">📅</span>
          <span class="text" v-if="!sidebarCollapsed">已安排</span>
        </button>
        <button class="menu-btn">
          <span class="icon">🧩</span>
          <span class="text" v-if="!sidebarCollapsed">插件</span>
        </button>
      </div>

      <!-- 项目列表 -->
      <div class="sidebar-section" v-if="!sidebarCollapsed">
        <div class="section-title">项目</div>
        <div v-for="project in projects" :key="project.name" class="project-group">
          <div class="project-name">
            <span class="icon">📁</span>
            {{ project.name }}
          </div>
          <div 
            v-for="conv in project.conversations" 
            :key="conv.id"
            class="conversation-item"
            :class="{ active: selectedConversation === conv.id }"
            @click="selectConversation(conv.id)"
          >
            <span class="conv-title">{{ conv.title }}</span>
            <span class="conv-time">{{ conv.time }}</span>
          </div>
        </div>
      </div>

      <!-- 独立对话 -->
      <div class="sidebar-section" v-if="!sidebarCollapsed">
        <div class="section-title">对话</div>
        <div 
          v-for="conv in standaloneConversations" 
          :key="conv.id"
          class="conversation-item"
          :class="{ active: selectedConversation === conv.id }"
          @click="selectConversation(conv.id)"
        >
          <span class="conv-title">{{ conv.title }}</span>
          <span class="conv-time">{{ conv.time }}</span>
        </div>
      </div>

      <!-- 底部设置 -->
      <div class="sidebar-footer">
        <div class="settings-btn">
          <span class="avatar">⚙️</span>
          <div class="settings-info" v-if="!sidebarCollapsed">
            <div class="settings-title">设置</div>
            <div class="settings-sub">账户</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-area">
      <!-- 顶部标题栏 -->
      <header class="top-bar">
        <button class="toggle-btn" @click="toggleSidebar">
          {{ sidebarCollapsed ? '☰' : '✕' }}
        </button>
        <h1 class="app-title">AI 小说创作助手</h1>
        <div class="top-actions">
          <button class="action-btn">📊</button>
          <button class="action-btn">⚙️</button>
        </div>
      </header>

      <!-- 消息区域 -->
      <div class="messages-area">
        <!-- 欢迎界面 -->
        <div v-if="messages.length === 0" class="welcome-screen">
          <div class="welcome-content">
            <h2 class="welcome-title">我们可以帮您创作什么？</h2>
            <p class="welcome-subtitle">告诉我您的想法，我来帮您实现</p>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="message-list">
          <div 
            v-for="(msg, index) in messages" 
            :key="index"
            class="message"
            :class="msg.role"
          >
            <div class="message-avatar">
              {{ msg.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              {{ msg.content }}
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <!-- 上下文标签 -->
        <div class="context-tags" v-if="contextItems.length > 0">
          <div 
            v-for="(item, index) in contextItems" 
            :key="index"
            class="context-tag"
          >
            <span class="tag-icon">📁</span>
            {{ item.name }}
            <button class="tag-remove" @click="contextItems.splice(index, 1)">×</button>
          </div>
        </div>

        <!-- 输入框容器 -->
        <div class="input-container">
          <div class="input-wrapper">
            <textarea 
              v-model="inputValue"
              placeholder="描述您想创作的内容..."
              class="message-input"
              @keydown="handleKeydown"
              rows="1"
            ></textarea>
          </div>
          
          <!-- 输入框底部工具栏 -->
          <div class="input-toolbar">
            <div class="toolbar-left">
              <button class="toolbar-btn" @click="addContext" title="添加上下文">
                <span>+</span>
              </button>
              <button class="toolbar-btn" title="请求批准">
                <span>🔑</span>
                <span class="btn-text">请求批准</span>
                <span class="dropdown-arrow">▼</span>
              </button>
            </div>
            <div class="toolbar-right">
              <button class="toolbar-btn mode-btn" @click="toggleRequestMode">
                自定义 <span class="mode-badge">{{ requestMode }}</span> ▼
              </button>
              <button 
                class="send-btn" 
                @click="sendMessage"
                :disabled="!inputValue.trim()"
              >
                <span class="send-icon">⬆</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 整体布局 */
.novel-app {
  display: flex;
  height: 100%;
  background: #f8f9fa;
  overflow: hidden;
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 60px;
}

/* 侧边栏菜单 */
.sidebar-menu {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.menu-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
  transition: background 0.2s;
}

.menu-btn:hover {
  background: #f3f4f6;
}

.menu-btn .icon {
  font-size: 16px;
}

/* 项目列表区域 */
.sidebar-section {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  margin-bottom: 8px;
  padding: 0 8px;
}

.project-group {
  margin-bottom: 16px;
}

.project-name {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.project-name .icon {
  font-size: 14px;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px 8px 32px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.conversation-item:hover {
  background: #f3f4f6;
}

.conversation-item.active {
  background: #e5e7eb;
}

.conv-title {
  font-size: 13px;
  color: #4b5563;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.conv-time {
  font-size: 11px;
  color: #9ca3af;
  flex-shrink: 0;
}

/* 底部设置 */
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid #e5e7eb;
}

.settings-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.settings-btn:hover {
  background: #f3f4f6;
}

.settings-btn .avatar {
  font-size: 20px;
}

.settings-info .settings-title {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.settings-info .settings-sub {
  font-size: 12px;
  color: #9ca3af;
}

/* ===== 主内容区 ===== */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部标题栏 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  color: #6b7280;
}

.toggle-btn:hover {
  background: #f3f4f6;
}

.app-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.top-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 18px;
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
}

.action-btn:hover {
  background: #f3f4f6;
}

/* 消息区域 */
.messages-area {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 20px;
  position: relative;
  z-index: 0;
}

/* 欢迎界面 */
.welcome-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
}

.welcome-content {
  text-align: center;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 16px;
  color: #6b7280;
}

/* 消息列表 */
.message-list {
  max-width: 800px;
  margin: 0 auto;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #dbeafe;
}

.message.assistant .message-avatar {
  background: #d1fae5;
}

.message-content {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
}

.message.user .message-content {
  background: #3b82f6;
  color: white;
  border-bottom-left-radius: 4px;
}

.message.assistant .message-content {
  background: #f3f4f6;
  color: #374151;
  border-bottom-left-radius: 4px;
}

/* ===== 输入区域 ===== */
.input-area {
  padding: 16px 20px 20px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
}

/* 上下文标签 */
.context-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.context-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f3f4f6;
  border-radius: 20px;
  font-size: 13px;
  color: #4b5563;
}

.tag-icon {
  font-size: 12px;
}

.tag-remove {
  background: none;
  border: none;
  font-size: 14px;
  cursor: pointer;
  color: #9ca3af;
  padding: 0;
  line-height: 1;
}

.tag-remove:hover {
  color: #ef4444;
}

/* 输入框容器 */
.input-container {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
  overflow: hidden;
  transition: border-color 0.2s;
}

.input-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-wrapper {
  padding: 12px 16px;
}

.message-input {
  width: 100%;
  border: none;
  background: transparent;
  resize: none;
  font-size: 14px;
  line-height: 1.6;
  color: #111827;
  outline: none;
  font-family: inherit;
}

.message-input::placeholder {
  color: #9ca3af;
}

/* 输入框底部工具栏 */
.input-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-top: 1px solid #e5e7eb;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.mode-btn {
  font-size: 12px;
}

.mode-badge {
  font-weight: 600;
  color: #111827;
}

.dropdown-arrow {
  font-size: 10px;
  margin-left: 2px;
}

/* 发送按钮 */
.send-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #111827;
  border: none;
  color: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: #374151;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.send-icon {
  display: block;
  margin-top: -1px;
}

/* 滚动条样式 */
.sidebar-section::-webkit-scrollbar,
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.sidebar-section::-webkit-scrollbar-track,
.messages-area::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-section::-webkit-scrollbar-thumb,
.messages-area::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.sidebar-section::-webkit-scrollbar-thumb:hover,
.messages-area::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}


</style>
