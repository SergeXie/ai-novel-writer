<script setup lang="ts">
/**
 * NovelEditorView.vue - 小说编辑页面
 * 三栏布局：左侧章节结构、中间文本编辑、右侧AI对话
 */
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getProject,
  getChapter,
  createChapter,
  updateChapter,
  deleteChapter,
  sendChatMessage,
  type NovelProjectDetail,
  type Chapter,
} from '../api/novel'

const route = useRoute()
const router = useRouter()

// 项目ID
const projectId = computed(() => route.params.id as string)

// 项目数据
const project = ref<NovelProjectDetail | null>(null)
const loading = ref(true)

// 当前选中的章节
const currentChapter = ref<Chapter | null>(null)

// 编辑器内容
const editorContent = ref('')
const editorTitle = ref('')
const saving = ref(false)
const lastSaved = ref<Date | null>(null)

// 左侧面板宽度（可拖拽调整）
const leftPanelWidth = ref(280)
const rightPanelWidth = ref(350)
const isDraggingLeft = ref(false)
const isDraggingRight = ref(false)

// 章节操作
const showNewChapterDialog = ref(false)
const newChapterTitle = ref('')
const newChapterNumber = ref(1)

// AI 对话
const chatMessages = ref<Array<{ role: string; content: string }>>([])
const chatInput = ref('')
const chatLoading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

// 计算属性：章节列表（按章节号排序）
const chapters = computed(() => {
  if (!project.value) return []
  return [...project.value.chapters].sort((a, b) => a.chapter_number - b.chapter_number)
})

// 计算属性：总字数
const totalWordCount = computed(() => {
  return chapters.value.reduce((sum, ch) => sum + ch.word_count, 0)
})

// 加载项目数据
const loadProject = async () => {
  loading.value = true
  try {
    project.value = await getProject(projectId.value)
    // 如果有章节，默认选中第一个
    if (project.value.chapters.length > 0) {
      await selectChapter(project.value.chapters[0])
    }
  } catch (error) {
    console.error('加载项目失败:', error)
  } finally {
    loading.value = false
  }
}

// 选择章节
const selectChapter = async (chapter: Chapter) => {
  // 如果当前有未保存的内容，先保存
  if (currentChapter.value && editorContent.value !== currentChapter.value.content) {
    await saveCurrentChapter()
  }

  currentChapter.value = chapter
  editorContent.value = chapter.content || ''
  editorTitle.value = chapter.title
}

// 保存当前章节
const saveCurrentChapter = async () => {
  if (!currentChapter.value) return

  saving.value = true
  try {
    const updated = await updateChapter(
      projectId.value,
      currentChapter.value.id,
      {
        title: editorTitle.value,
        content: editorContent.value,
      }
    )

    // 更新本地数据
    currentChapter.value = updated
    lastSaved.value = new Date()

    // 更新项目中的章节
    if (project.value) {
      const index = project.value.chapters.findIndex((c) => c.id === updated.id)
      if (index !== -1) {
        project.value.chapters[index] = updated
      }
    }
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

// 创建新章节
const handleCreateChapter = async () => {
  if (!newChapterTitle.value.trim()) return

  try {
    const chapter = await createChapter(projectId.value, {
      title: newChapterTitle.value,
      chapter_number: newChapterNumber.value,
    })

    // 更新项目数据
    if (project.value) {
      project.value.chapters.push(chapter)
    }

    // 选中新创建的章节
    await selectChapter(chapter)

    // 关闭弹窗
    showNewChapterDialog.value = false
    newChapterTitle.value = ''
    newChapterNumber.value = chapters.value.length + 1
  } catch (error) {
    console.error('创建章节失败:', error)
  }
}

// 删除章节
const handleDeleteChapter = async (chapterId: string) => {
  if (!confirm('确定要删除这个章节吗？此操作不可恢复。')) return

  try {
    await deleteChapter(projectId.value, chapterId)

    // 更新本地数据
    if (project.value) {
      project.value.chapters = project.value.chapters.filter((c) => c.id !== chapterId)
    }

    // 如果删除的是当前章节，清空编辑器
    if (currentChapter.value?.id === chapterId) {
      currentChapter.value = null
      editorContent.value = ''
      editorTitle.value = ''

      // 如果还有其他章节，选中第一个
      if (project.value && project.value.chapters.length > 0) {
        await selectChapter(project.value.chapters[0])
      }
    }
  } catch (error) {
    console.error('删除章节失败:', error)
  }
}

// 发送 AI 消息
const sendChatMessage_ = async () => {
  if (!chatInput.value.trim() || chatLoading.value) return

  const userMessage = chatInput.value
  chatMessages.value.push({ role: 'user', content: userMessage })
  chatInput.value = ''
  chatLoading.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  try {
    // 构建上下文
    let context = userMessage
    if (currentChapter.value) {
      context = `当前章节：${currentChapter.value.title}\n章节内容：\n${editorContent.value}\n\n用户问题：${userMessage}`
    }

    const response = await sendChatMessage(context, undefined, projectId.value)
    chatMessages.value.push({
      role: 'assistant',
      content: response.message.content,
    })
  } catch (error) {
    chatMessages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。',
    })
    console.error('AI 对话失败:', error)
  } finally {
    chatLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 返回列表
const goBack = () => {
  router.push('/novel')
}

// 打开新建章节弹窗
const openNewChapterDialog = () => {
  newChapterNumber.value = chapters.value.length + 1
  newChapterTitle.value = `第${newChapterNumber.value}章 `
  showNewChapterDialog.value = true
}

// 左侧拖拽调整宽度
const startDragLeft = (e: MouseEvent) => {
  isDraggingLeft.value = true
  const startX = e.clientX
  const startWidth = leftPanelWidth.value

  const onMouseMove = (e: MouseEvent) => {
    const diff = e.clientX - startX
    leftPanelWidth.value = Math.max(200, Math.min(400, startWidth + diff))
  }

  const onMouseUp = () => {
    isDraggingLeft.value = false
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
  }

  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

// 右侧拖拽调整宽度
const startDragRight = (e: MouseEvent) => {
  isDraggingRight.value = true
  const startX = e.clientX
  const startWidth = rightPanelWidth.value

  const onMouseMove = (e: MouseEvent) => {
    const diff = startX - e.clientX
    rightPanelWidth.value = Math.max(280, Math.min(500, startWidth + diff))
  }

  const onMouseUp = () => {
    isDraggingRight.value = false
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
  }

  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

// 处理键盘快捷键
const handleEditorKeydown = (e: KeyboardEvent) => {
  // Ctrl+S 保存
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    saveCurrentChapter()
  }
}

// 自动保存（防抖）
let autoSaveTimer: ReturnType<typeof setTimeout> | null = null
watch(editorContent, () => {
  if (autoSaveTimer) {
    clearTimeout(autoSaveTimer)
  }
  autoSaveTimer = setTimeout(() => {
    if (currentChapter.value) {
      saveCurrentChapter()
    }
  }, 3000) // 3秒后自动保存
})

// 组件挂载时加载数据
onMounted(() => {
  loadProject()
})
</script>

<template>
  <div class="editor-container" @keydown="handleEditorKeydown">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>

    <template v-else-if="project">
      <!-- 顶部工具栏 -->
      <header class="editor-header">
        <div class="header-left">
          <button class="back-btn" @click="goBack" title="返回列表">
            ← 返回
          </button>
          <div class="project-info">
            <h1 class="project-title">{{ project.title }}</h1>
            <span class="project-meta">
              {{ project.genre || '未分类' }} · {{ chapters.length }} 章 · {{ totalWordCount }} 字
            </span>
          </div>
        </div>

        <div class="header-right">
          <span v-if="lastSaved" class="save-status">
            {{ saving ? '保存中...' : `已保存 ${lastSaved.toLocaleTimeString()}` }}
          </span>
          <button class="save-btn" @click="saveCurrentChapter" :disabled="saving || !currentChapter">
            💾 保存
          </button>
        </div>
      </header>

      <!-- 三栏布局 -->
      <div class="editor-body">
        <!-- 左侧：章节结构 -->
        <aside class="left-panel" :style="{ width: leftPanelWidth + 'px' }">
          <div class="panel-header">
            <h3>章节结构</h3>
            <button class="add-chapter-btn" @click="openNewChapterDialog" title="添加章节">
              +
            </button>
          </div>

          <div class="chapter-list">
            <div
              v-for="chapter in chapters"
              :key="chapter.id"
              class="chapter-item"
              :class="{ active: currentChapter?.id === chapter.id }"
              @click="selectChapter(chapter)"
            >
              <div class="chapter-info">
                <span class="chapter-number">{{ chapter.chapter_number }}</span>
                <div class="chapter-details">
                  <span class="chapter-title">{{ chapter.title }}</span>
                  <span class="chapter-words">{{ chapter.word_count }} 字</span>
                </div>
              </div>
              <button
                class="delete-chapter-btn"
                @click.stop="handleDeleteChapter(chapter.id)"
                title="删除章节"
              >
                ×
              </button>
            </div>

            <!-- 空状态 -->
            <div v-if="chapters.length === 0" class="empty-chapters">
              <p>暂无章节</p>
              <button class="add-chapter-btn-text" @click="openNewChapterDialog">
                + 创建第一章
              </button>
            </div>
          </div>
        </aside>

        <!-- 左侧拖拽条 -->
        <div
          class="drag-handle left-drag"
          @mousedown="startDragLeft"
          :class="{ dragging: isDraggingLeft }"
        ></div>

        <!-- 中间：文本编辑区 -->
        <main class="center-panel">
          <template v-if="currentChapter">
            <div class="editor-toolbar">
              <input
                v-model="editorTitle"
                class="chapter-title-input"
                placeholder="章节标题"
              />
              <div class="toolbar-actions">
                <span class="word-count">{{ editorContent.length }} 字</span>
              </div>
            </div>

            <div class="editor-wrapper">
              <textarea
                v-model="editorContent"
                class="content-editor"
                placeholder="开始创作你的故事..."
                spellcheck="false"
              ></textarea>
            </div>
          </template>

          <!-- 未选择章节时的提示 -->
          <div v-else class="no-chapter-selected">
            <div class="prompt-icon">📝</div>
            <h3>选择一个章节开始编辑</h3>
            <p>从左侧章节列表中选择一个章节，或创建一个新章节</p>
            <button class="create-chapter-btn" @click="openNewChapterDialog">
              + 创建新章节
            </button>
          </div>
        </main>

        <!-- 右侧拖拽条 -->
        <div
          class="drag-handle right-drag"
          @mousedown="startDragRight"
          :class="{ dragging: isDraggingRight }"
        ></div>

        <!-- 右侧：AI 对话 -->
        <aside class="right-panel" :style="{ width: rightPanelWidth + 'px' }">
          <div class="panel-header">
            <h3>AI 助手</h3>
            <button class="clear-chat-btn" @click="chatMessages = []" title="清空对话">
              🗑️
            </button>
          </div>

          <!-- 对话消息 -->
          <div class="chat-messages" ref="chatContainer">
            <!-- 欢迎消息 -->
            <div v-if="chatMessages.length === 0" class="chat-welcome">
              <div class="welcome-icon">🤖</div>
              <h4>AI 写作助手</h4>
              <p>我可以帮你：</p>
              <ul>
                <li>续写故事情节</li>
                <li>优化文字表达</li>
                <li>生成角色对话</li>
                <li>提供创作建议</li>
              </ul>
            </div>

            <!-- 消息列表 -->
            <div
              v-for="(msg, index) in chatMessages"
              :key="index"
              class="chat-message"
              :class="msg.role"
            >
              <div class="message-avatar">
                {{ msg.role === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="message-content">
                {{ msg.content }}
              </div>
            </div>

            <!-- 加载中 -->
            <div v-if="chatLoading" class="chat-message assistant loading">
              <div class="message-avatar">🤖</div>
              <div class="message-content">
                <span class="typing-indicator">思考中...</span>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <textarea
              v-model="chatInput"
              class="chat-input"
              placeholder="输入你的问题..."
              @keydown.enter.exact.prevent="sendChatMessage_"
              rows="3"
            ></textarea>
            <button
              class="send-btn"
              @click="sendChatMessage_"
              :disabled="!chatInput.trim() || chatLoading"
            >
              发送
            </button>
          </div>
        </aside>
      </div>
    </template>

    <!-- 项目不存在 -->
    <div v-else class="error-state">
      <div class="error-icon">😕</div>
      <h3>项目不存在</h3>
      <p>该项目可能已被删除或您没有访问权限</p>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>

    <!-- 新建章节弹窗 -->
    <Teleport to="body">
      <div v-if="showNewChapterDialog" class="dialog-overlay" @click.self="showNewChapterDialog = false">
        <div class="dialog">
          <div class="dialog-header">
            <h2>创建新章节</h2>
            <button class="close-btn" @click="showNewChapterDialog = false">×</button>
          </div>

          <div class="dialog-body">
            <div class="form-group">
              <label>章节编号 <span class="required">*</span></label>
              <input
                v-model.number="newChapterNumber"
                type="number"
                min="1"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label>章节标题 <span class="required">*</span></label>
              <input
                v-model="newChapterTitle"
                type="text"
                placeholder="请输入章节标题"
                class="form-input"
                @keyup.enter="handleCreateChapter"
              />
            </div>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="showNewChapterDialog = false">取消</button>
            <button
              class="submit-btn"
              @click="handleCreateChapter"
              :disabled="!newChapterTitle.trim()"
            >
              创建
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
/* 整体容器 */
.editor-container {
  width: calc(100% + 4rem);
  margin-left: -2rem;
  margin-top: -2rem;
  height: calc(100vh - 50px);
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  overflow: hidden;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 顶部工具栏 */
.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.project-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.project-meta {
  font-size: 13px;
  color: #94a3b8;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.save-status {
  font-size: 13px;
  color: #64748b;
}

.save-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 三栏布局 */
.editor-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧面板 */
.left-panel {
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.panel-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.add-chapter-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #6366f1;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.add-chapter-btn:hover {
  background: #f5f3ff;
  border-color: #6366f1;
}

/* 章节列表 */
.chapter-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chapter-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.chapter-item:hover {
  background: #f1f5f9;
}

.chapter-item.active {
  background: #eef2ff;
  border: 1px solid #c7d2fe;
}

.chapter-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.chapter-number {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #6366f1;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chapter-item.active .chapter-number {
  background: #6366f1;
  color: white;
}

.chapter-details {
  flex: 1;
  min-width: 0;
}

.chapter-title {
  display: block;
  font-size: 14px;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chapter-words {
  font-size: 12px;
  color: #94a3b8;
}

.delete-chapter-btn {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 16px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
}

.chapter-item:hover .delete-chapter-btn {
  opacity: 1;
}

.delete-chapter-btn:hover {
  background: #fee2e2;
  color: #ef4444;
}

/* 空章节状态 */
.empty-chapters {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-chapters p {
  font-size: 14px;
  color: #94a3b8;
  margin: 0 0 16px;
}

.add-chapter-btn-text {
  padding: 8px 16px;
  border: 1px dashed #6366f1;
  border-radius: 8px;
  background: transparent;
  color: #6366f1;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-chapter-btn-text:hover {
  background: #f5f3ff;
}

/* 拖拽条 */
.drag-handle {
  width: 4px;
  cursor: col-resize;
  background: #e5e7eb;
  transition: background 0.2s ease;
  flex-shrink: 0;
}

.drag-handle:hover,
.drag-handle.dragging {
  background: #6366f1;
}

/* 中间编辑区 */
.center-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  min-width: 0;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.chapter-title-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid transparent;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  background: transparent;
  transition: all 0.2s ease;
}

.chapter-title-input:focus {
  outline: none;
  border-color: #e5e7eb;
  background: #f9fafb;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.word-count {
  font-size: 13px;
  color: #94a3b8;
}

/* 编辑器包装器 */
.editor-wrapper {
  flex: 1;
  overflow: hidden;
}

.content-editor {
  width: 100%;
  height: 100%;
  padding: 24px;
  border: none;
  font-size: 16px;
  line-height: 1.8;
  color: #1e293b;
  background: white;
  resize: none;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
}

.content-editor:focus {
  outline: none;
}

.content-editor::placeholder {
  color: #cbd5e1;
}

/* 未选择章节提示 */
.no-chapter-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
}

.prompt-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.no-chapter-selected h3 {
  font-size: 20px;
  color: #1e293b;
  margin: 0 0 8px;
}

.no-chapter-selected p {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 24px;
}

.create-chapter-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  background: #6366f1;
  color: white;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-chapter-btn:hover {
  background: #4f46e5;
}

/* 右侧 AI 对话面板 */
.right-panel {
  background: white;
  border-left: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.clear-chat-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-chat-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
}

/* 聊天消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 欢迎消息 */
.chat-welcome {
  text-align: center;
  padding: 20px;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.chat-welcome h4 {
  font-size: 16px;
  color: #1e293b;
  margin: 0 0 8px;
}

.chat-welcome p {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 12px;
}

.chat-welcome ul {
  text-align: left;
  font-size: 14px;
  color: #64748b;
  margin: 0;
  padding-left: 20px;
}

.chat-welcome li {
  margin-bottom: 4px;
}

/* 聊天消息 */
.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.chat-message.user .message-avatar {
  background: #6366f1;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: #1e293b;
  background: #f1f5f9;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-message.user .message-content {
  background: #6366f1;
  color: white;
}

.chat-message.assistant .message-content {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

/* 打字指示器 */
.typing-indicator {
  display: inline-block;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 聊天输入区域 */
.chat-input-area {
  padding: 16px;
  border-top: 1px solid #e5e7eb;
}

.chat-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.chat-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.send-btn {
  width: 100%;
  padding: 10px;
  margin-top: 8px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 错误状态 */
.error-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.error-state h3 {
  font-size: 20px;
  color: #1e293b;
  margin: 0 0 8px;
}

.error-state p {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 24px;
}

/* 弹窗样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 20px 0;
}

.dialog-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  font-size: 18px;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #e2e8f0;
}

.dialog-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
}

.required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  background: #f9fafb;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 20px 20px;
}

.cancel-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f9fafb;
}

.submit-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
