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
  getPrompts,
  type NovelProjectDetail,
  type Chapter,
  type Prompt,
} from '../api/novel'
import ChapterTree from '../components/ChapterTree.vue'

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

// AI 对话
const chatMessages = ref<Array<{ role: string; content: string }>>([])
const chatInput = ref('')
const chatLoading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

// ---- 关联章节 ----
const selectedChapterIds = ref<Set<string>>(new Set())
const showChapterPicker = ref(false)

// 折叠状态（弹窗内文件夹展开/折叠）
const pickerExpanded = ref<Set<string>>(new Set())

// 构建树节点
interface PickerTreeNode { chapter: Chapter; children: PickerTreeNode[]; depth: number }

// 树状结构数据（包含所有节点：文件夹 + 章节）
const chapterTreeForPicker = computed<PickerTreeNode[]>(() => {
  const map = new Map<string, PickerTreeNode>()
  const roots: PickerTreeNode[] = []
  for (const ch of chapters.value) {
    map.set(ch.id, { chapter: ch, children: [], depth: 0 })
  }
  for (const ch of chapters.value) {
    const node = map.get(ch.id)!
    if (ch.parent_id && map.has(ch.parent_id)) {
      map.get(ch.parent_id)!.children.push(node)
    } else {
      roots.push(node)
    }
  }
  // 排序
  const sort = (nodes: PickerTreeNode[]) => {
    nodes.sort((a, b) => a.chapter.sort_order - b.chapter.sort_order || a.chapter.chapter_number - b.chapter.chapter_number)
    for (const n of nodes) sort(n.children)
  }
  sort(roots)
  // 设置 depth
  const setDepth = (nodes: PickerTreeNode[], depth: number) => {
    for (const n of nodes) {
      n.depth = depth
      setDepth(n.children, depth + 1)
    }
  }
  setDepth(roots, 0)
  return roots
})

// 展开/折叠文件夹
const togglePickerExpand = (chapterId: string) => {
  if (pickerExpanded.value.has(chapterId)) {
    pickerExpanded.value.delete(chapterId)
  } else {
    pickerExpanded.value.add(chapterId)
  }
  pickerExpanded.value = new Set(pickerExpanded.value)
}

// 判断是否展开
const isPickerExpanded = (ch: Chapter): boolean => {
  return pickerExpanded.value.has(ch.id) || ch.is_expanded !== false
}

// 切换章节选择（只对章节节点有效）
const toggleChapterSelection = (chapterId: string) => {
  if (selectedChapterIds.value.has(chapterId)) {
    selectedChapterIds.value.delete(chapterId)
  } else {
    selectedChapterIds.value.add(chapterId)
  }
  selectedChapterIds.value = new Set(selectedChapterIds.value)
}

// 清空已选章节
const clearSelectedChapters = () => {
  selectedChapterIds.value = new Set()
}

// 已选章节的详情
const selectedChapters = computed(() => {
  return chapters.value.filter((ch) => selectedChapterIds.value.has(ch.id))
})

// 选中文件夹下所有子章节
const selectAllInFolder = (node: PickerTreeNode) => {
  const collect = (n: PickerTreeNode) => {
    if (n.chapter.node_type === 'chapter') {
      selectedChapterIds.value.add(n.chapter.id)
    }
    for (const child of n.children) collect(child)
  }
  collect(node)
  selectedChapterIds.value = new Set(selectedChapterIds.value)
}

// ---- 选择提示词 ----
const promptList = ref<Prompt[]>([])
const promptLoading = ref(false)
const showPromptPicker = ref(false)
const selectedPrompt = ref<Prompt | null>(null)

// 加载提示词列表
const loadPromptList = async () => {
  promptLoading.value = true
  try {
    const data = await getPrompts(1, 50)
    promptList.value = data.items
  } catch (e) {
    console.error('加载提示词失败:', e)
  } finally {
    promptLoading.value = false
  }
}

// 选择提示词
const selectPrompt = (prompt: Prompt) => {
  selectedPrompt.value = prompt
  showPromptPicker.value = false
}

// 清除选中的提示词
const clearSelectedPrompt = () => {
  selectedPrompt.value = null
}

// 计算属性：章节列表（按 sort_order 排序）
const chapters = computed(() => {
  if (!project.value) return []
  return [...project.value.chapters].sort((a, b) => a.sort_order - b.sort_order || a.chapter_number - b.chapter_number)
})

// 计算属性：总字数（只统计实际章节）
const totalWordCount = computed(() => {
  return chapters.value
    .filter((ch) => ch.node_type === 'chapter')
    .reduce((sum, ch) => sum + ch.word_count, 0)
})

// ---- 章节树操作 ----

// 新建弹窗
const showNewDialog = ref(false)
const newNodeTitle = ref('')
const newNodeType = ref<'folder' | 'chapter'>('chapter')
const newNodeParentId = ref<string | null>(null)

// 在指定父节点下创建
const handleTreeCreate = (parentId: string | null, nodeType: 'folder' | 'chapter') => {
  newNodeTitle.value = ''
  newNodeType.value = nodeType
  newNodeParentId.value = parentId
  showNewDialog.value = true
}

// 提交创建
const handleCreateNode = async () => {
  if (!newNodeTitle.value.trim()) return

  try {
    // 计算 sort_order（同级最大 +1）
    const siblings = chapters.value.filter(
      (ch) => ch.parent_id === newNodeParentId.value
    )
    const maxSort = siblings.reduce((max, ch) => Math.max(max, ch.sort_order), 0)

    const requestData = {
      title: newNodeTitle.value.trim(),
      node_type: newNodeType.value,
      parent_id: newNodeParentId.value || undefined,
      sort_order: maxSort + 1,
      chapter_number: newNodeType.value === 'chapter' ? chapters.value.filter(c => c.node_type === 'chapter').length + 1 : 0,
    }

    console.log('创建请求:', JSON.stringify(requestData))
    const node = await createChapter(projectId.value, requestData)

    if (project.value) {
      project.value.chapters.push(node)
    }

    // 如果是章节，自动选中
    if (newNodeType.value === 'chapter') {
      await selectChapter(node)
    }

    showNewDialog.value = false
    newNodeTitle.value = ''
  } catch (error) {
    console.error('创建失败:', error)
  }
}

// 树节点删除
const handleTreeDelete = async (chapterId: string) => {
  try {
    await deleteChapter(projectId.value, chapterId)

    // 更新本地数据（后端级联删除子节点）
    if (project.value) {
      // 递归收集要删除的ID
      const idsToRemove = new Set<string>()
      const collectIds = (parentId: string) => {
        idsToRemove.add(parentId)
        chapters.value
          .filter((c) => c.parent_id === parentId)
          .forEach((c) => collectIds(c.id))
      }
      collectIds(chapterId)

      project.value.chapters = project.value.chapters.filter(
        (c) => !idsToRemove.has(c.id)
      )
    }

    // 如果删除的是当前选中的章节，清空编辑器
    if (currentChapter.value?.id === chapterId) {
      currentChapter.value = null
      editorContent.value = ''
      editorTitle.value = ''

      // 尝试选中第一个可用章节
      const firstChapter = chapters.value.find((c) => c.node_type === 'chapter' && c.id !== chapterId)
      if (firstChapter) {
        await selectChapter(firstChapter)
      }
    }
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 树节点更新（折叠/展开等）
const handleTreeUpdate = async (chapterId: string, data: Partial<Chapter>) => {
  try {
    await updateChapter(projectId.value, chapterId, data)
    if (project.value) {
      const index = project.value.chapters.findIndex((c) => c.id === chapterId)
      if (index !== -1) {
        project.value.chapters[index] = { ...project.value.chapters[index], ...data }
      }
    }
  } catch (error) {
    console.error('更新失败:', error)
  }
}

// 树节点重命名
const handleTreeRename = async (chapterId: string, newTitle: string) => {
  try {
    await updateChapter(projectId.value, chapterId, { title: newTitle })
    if (project.value) {
      const index = project.value.chapters.findIndex((c) => c.id === chapterId)
      if (index !== -1) {
        project.value.chapters[index].title = newTitle
      }
    }
    // 如果是当前选中章节，同步编辑器
    if (currentChapter.value?.id === chapterId) {
      currentChapter.value.title = newTitle
      editorTitle.value = newTitle
    }
  } catch (error) {
    console.error('重命名失败:', error)
  }
}

// 树节点复制（递归复制子节点）
const handleTreeCopy = async (chapterId: string) => {
  const source = chapters.value.find((c) => c.id === chapterId)
  if (!source) return

  try {
    // 递归复制节点
    const copyNode = async (srcId: string, parentId: string | null): Promise<Chapter | null> => {
      const src = chapters.value.find((c) => c.id === srcId)
      if (!src) return null

      const siblings = chapters.value.filter((c) => c.parent_id === parentId)
      const maxSort = siblings.reduce((max, c) => Math.max(max, c.sort_order), 0)

      const newNode = await createChapter(projectId.value, {
        title: src.title + ' (副本)',
        content: src.content || undefined,
        node_type: src.node_type,
        parent_id: parentId,
        sort_order: maxSort + 1,
        chapter_number: src.node_type === 'chapter' ? chapters.value.length + 1 : 0,
      })

      if (project.value) {
        project.value.chapters.push(newNode)
      }

      // 递归复制子节点
      const children = chapters.value.filter((c) => c.parent_id === srcId)
      for (const child of children) {
        await copyNode(child.id, newNode.id)
      }

      return newNode
    }

    await copyNode(chapterId, source.parent_id)
  } catch (error) {
    console.error('复制失败:', error)
  }
}

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

// 选择章节（文件夹不可编辑）
const selectChapter = async (chapter: Chapter) => {
  if (chapter.node_type === 'folder') return

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

// 发送 AI 消息
const sendChatMessage_ = async () => {
  if (!chatInput.value.trim() || chatLoading.value) return

  const userMessage = chatInput.value

  // 构建用户消息的显示文本（包含提示词标记）
  let displayMessage = userMessage
  if (selectedPrompt.value) {
    displayMessage = `📎 ${selectedPrompt.value.title}\n${userMessage}`
  }
  if (selectedChapters.value.length > 0) {
    displayMessage += `\n🔗 关联了 ${selectedChapters.value.length} 个章节`
  }

  chatMessages.value.push({ role: 'user', content: displayMessage })
  chatInput.value = ''
  chatLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    // 构建上下文列表
    const contextList: string[] = []

    // 1. 当前编辑章节（自动包含）
    if (currentChapter.value && editorContent.value) {
      contextList.push(`[当前编辑章节] ${currentChapter.value.title}\n${editorContent.value}`)
    }

    // 2. 用户手动关联的章节
    for (const ch of selectedChapters.value) {
      // 避免重复添加当前章节
      if (ch.id === currentChapter.value?.id) continue
      if (ch.content) {
        contextList.push(`[关联章节] ${ch.title}\n${ch.content}`)
      }
    }

    // 3. 选中的提示词
    if (selectedPrompt.value) {
      contextList.push(`[提示词] ${selectedPrompt.value.title}\n${selectedPrompt.value.content}`)
    }

    const response = await sendChatMessage(
      userMessage,
      undefined,
      projectId.value,
      contextList.length > 0 ? contextList : undefined
    )
    chatMessages.value.push({
      role: 'assistant',
      content: response.message.content,
    })

    // 发送后清除选择（提示词自动清除，章节保留以便复用）
    selectedPrompt.value = null
  } catch (error: any) {
    const errorMsg = error?.message || '抱歉，发生了错误，请稍后重试。'
    chatMessages.value.push({ role: 'assistant', content: errorMsg })
    console.error('AI 对话失败:', error)
  } finally {
    chatLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

// 返回列表
const goBack = () => {
  router.push('/novel')
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
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
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" style="vertical-align: -2px"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg> 保存
          </button>
        </div>
      </header>

      <!-- 三栏布局 -->
      <div class="editor-body">
        <!-- 左侧：章节树 -->
        <aside class="left-panel" :style="{ width: leftPanelWidth + 'px' }">
          <div class="panel-header">
            <h3>目录结构</h3>
          </div>

          <ChapterTree
            :chapters="chapters"
            :active-chapter-id="currentChapter?.id || null"
            @select="selectChapter"
            @delete="handleTreeDelete"
            @create="handleTreeCreate"
            @update="handleTreeUpdate"
            @rename="handleTreeRename"
            @copy="handleTreeCopy"
          />
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
            <div class="prompt-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="32" height="32"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></div>
            <h3>选择一个章节开始编辑</h3>
            <p>从左侧章节列表中选择一个章节，或创建一个新章节</p>
            <button class="create-chapter-btn" @click="handleTreeCreate(null, 'chapter')">
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
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>

          <!-- 对话消息 -->
          <div class="chat-messages" ref="chatContainer">
            <!-- 欢迎消息 -->
            <div v-if="chatMessages.length === 0" class="chat-welcome">
              <div class="welcome-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg></div>
              <h4>AI 写作助手</h4>
              <p>我可以帮你：</p>
              <ul>
                <li>续写故事情节</li>
                <li>优化文字表达</li>
                <li>生成角色对话</li>
                <li>提供创作建议</li>
              </ul>
              <p class="tip">💡 使用下方「关联章节」和「提示词」功能，让 AI 更好地理解你的创作意图</p>
            </div>

            <!-- 消息列表 -->
            <div
              v-for="(msg, index) in chatMessages"
              :key="index"
              class="chat-message"
              :class="msg.role"
            >
              <div class="message-avatar">
                {{ msg.role === 'user' ? 'U' : 'AI' }}
              </div>
              <div class="message-content">
                {{ msg.content }}
              </div>
            </div>

            <!-- 加载中 -->
            <div v-if="chatLoading" class="chat-message assistant loading">
              <div class="message-avatar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg></div>
              <div class="message-content">
                <span class="typing-indicator">思考中...</span>
              </div>
            </div>
          </div>

          <!-- 已选标签区域 -->
          <div v-if="selectedChapters.length > 0 || selectedPrompt" class="selected-tags">
            <!-- 已选提示词标签 -->
            <div v-if="selectedPrompt" class="tag-item prompt-tag" @click="clearSelectedPrompt">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="12" height="12"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              <span>{{ selectedPrompt.title }}</span>
              <span class="tag-remove">×</span>
            </div>
            <!-- 已选章节标签 -->
            <div v-for="ch in selectedChapters" :key="ch.id" class="tag-item chapter-tag" @click="toggleChapterSelection(ch.id)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="12" height="12"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              <span>{{ ch.title }}</span>
              <span class="tag-remove">×</span>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <!-- 工具栏：关联章节 / 选择提示词 -->
            <div class="chat-toolbar">
              <button class="toolbar-btn" @click="showChapterPicker = true" :class="{ active: selectedChapters.length > 0 }" title="关联章节">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                关联章节
                <span v-if="selectedChapters.length > 0" class="badge">{{ selectedChapters.length }}</span>
              </button>
              <button class="toolbar-btn" @click="showPromptPicker = true; loadPromptList()" :class="{ active: !!selectedPrompt }" title="选择提示词">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                提示词
              </button>
              <div class="toolbar-spacer"></div>
              <span v-if="currentChapter" class="current-chapter-hint" :title="currentChapter.title">
                📝 {{ currentChapter.title }}
              </span>
            </div>

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
      <div class="error-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg></div>
      <h3>项目不存在</h3>
      <p>该项目可能已被删除或您没有访问权限</p>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>

    <!-- 新建弹窗 -->
    <Teleport to="body">
      <div v-if="showNewDialog" class="dialog-overlay" @click.self="showNewDialog = false">
        <div class="dialog">
          <div class="dialog-header">
            <h2>{{ newNodeType === 'folder' ? '新建文件夹' : '新建章节' }}</h2>
            <button class="close-btn" @click="showNewDialog = false">×</button>
          </div>

          <div class="dialog-body">
            <div class="form-group">
              <label>名称 <span class="required">*</span></label>
              <input
                v-model="newNodeTitle"
                type="text"
                :placeholder="newNodeType === 'folder' ? '请输入文件夹名称' : '请输入章节标题'"
                class="form-input"
                @keyup.enter="handleCreateNode"
                ref="newNodeInputRef"
              />
            </div>

            <div class="form-group">
              <label>类型</label>
              <div class="type-switcher">
                <button
                  class="type-btn"
                  :class="{ active: newNodeType === 'chapter' }"
                  @click="newNodeType = 'chapter'"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" style="vertical-align: -2px"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg> 章节
                </button>
                <button
                  class="type-btn"
                  :class="{ active: newNodeType === 'folder' }"
                  @click="newNodeType = 'folder'"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" style="vertical-align: -2px"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg> 文件夹
                </button>
              </div>
            </div>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="showNewDialog = false">取消</button>
            <button
              class="submit-btn"
              @click="handleCreateNode"
              :disabled="!newNodeTitle.trim()"
            >
              创建
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 关联章节弹窗 -->
    <Teleport to="body">
      <div v-if="showChapterPicker" class="dialog-overlay" @click.self="showChapterPicker = false">
        <div class="dialog chapter-picker-dialog">
          <div class="dialog-header">
            <h2>关联章节</h2>
            <button class="close-btn" @click="showChapterPicker = false">×</button>
          </div>

          <div class="dialog-body chapter-picker-body">
            <div v-if="chapters.length === 0" class="picker-empty">暂无可关联的章节</div>
            <!-- 树状递归渲染 -->
            <template v-for="node in chapterTreeForPicker" :key="node.chapter.id">
              <div class="tree-node" :style="{ paddingLeft: node.depth * 20 + 'px' }">
                <!-- 文件夹行 -->
                <div
                  v-if="node.chapter.node_type === 'folder'"
                  class="tree-row tree-folder"
                >
                  <span class="tree-arrow" :class="{ opened: isPickerExpanded(node.chapter) }" @click="togglePickerExpand(node.chapter.id)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><polyline points="9 18 15 12 9 6"/></svg>
                  </span>
                  <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" width="16" height="16"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                  <span class="tree-label">{{ node.chapter.title }}</span>
                  <button class="tree-folder-select-btn" title="选中该文件夹下所有章节" @click="selectAllInFolder(node)">全选</button>
                </div>
                <!-- 章节行 -->
                <label
                  v-else
                  class="tree-row tree-chapter"
                  :class="{ selected: selectedChapterIds.has(node.chapter.id), current: node.chapter.id === currentChapter?.id }"
                >
                  <span class="tree-arrow-placeholder"></span>
                  <input
                    type="checkbox"
                    :checked="selectedChapterIds.has(node.chapter.id)"
                    @change="toggleChapterSelection(node.chapter.id)"
                  />
                  <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" width="16" height="16"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                  <span class="tree-label">{{ node.chapter.title }}</span>
                  <span v-if="node.chapter.id === currentChapter?.id" class="picker-item-badge">当前</span>
                  <span class="tree-count">{{ node.chapter.word_count }}字</span>
                </label>
              </div>
              <!-- 递归子节点 -->
              <template v-if="node.chapter.node_type !== 'folder' || isPickerExpanded(node.chapter)">
                <template v-for="child1 in node.children" :key="child1.chapter.id">
                  <div class="tree-node" :style="{ paddingLeft: child1.depth * 20 + 'px' }">
                    <div
                      v-if="child1.chapter.node_type === 'folder'"
                      class="tree-row tree-folder"
                    >
                      <span class="tree-arrow" :class="{ opened: isPickerExpanded(child1.chapter) }" @click="togglePickerExpand(child1.chapter.id)">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><polyline points="9 18 15 12 9 6"/></svg>
                      </span>
                      <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" width="16" height="16"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                      <span class="tree-label">{{ child1.chapter.title }}</span>
                      <button class="tree-folder-select-btn" title="选中该文件夹下所有章节" @click="selectAllInFolder(child1)">全选</button>
                    </div>
                    <label
                      v-else
                      class="tree-row tree-chapter"
                      :class="{ selected: selectedChapterIds.has(child1.chapter.id), current: child1.chapter.id === currentChapter?.id }"
                    >
                      <span class="tree-arrow-placeholder"></span>
                      <input
                        type="checkbox"
                        :checked="selectedChapterIds.has(child1.chapter.id)"
                        @change="toggleChapterSelection(child1.chapter.id)"
                      />
                      <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" width="16" height="16"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                      <span class="tree-label">{{ child1.chapter.title }}</span>
                      <span v-if="child1.chapter.id === currentChapter?.id" class="picker-item-badge">当前</span>
                      <span class="tree-count">{{ child1.chapter.word_count }}字</span>
                    </label>
                  </div>
                  <!-- 第三层 -->
                  <template v-if="child1.chapter.node_type !== 'folder' || isPickerExpanded(child1.chapter)">
                    <template v-for="child2 in child1.children" :key="child2.chapter.id">
                      <div class="tree-node" :style="{ paddingLeft: child2.depth * 20 + 'px' }">
                        <div
                          v-if="child2.chapter.node_type === 'folder'"
                          class="tree-row tree-folder"
                        >
                          <span class="tree-arrow" :class="{ opened: isPickerExpanded(child2.chapter) }" @click="togglePickerExpand(child2.chapter.id)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><polyline points="9 18 15 12 9 6"/></svg>
                          </span>
                          <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" width="16" height="16"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                          <span class="tree-label">{{ child2.chapter.title }}</span>
                          <button class="tree-folder-select-btn" title="选中该文件夹下所有章节" @click="selectAllInFolder(child2)">全选</button>
                        </div>
                        <label
                          v-else
                          class="tree-row tree-chapter"
                          :class="{ selected: selectedChapterIds.has(child2.chapter.id), current: child2.chapter.id === currentChapter?.id }"
                        >
                          <span class="tree-arrow-placeholder"></span>
                          <input
                            type="checkbox"
                            :checked="selectedChapterIds.has(child2.chapter.id)"
                            @change="toggleChapterSelection(child2.chapter.id)"
                          />
                          <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" width="16" height="16"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                          <span class="tree-label">{{ child2.chapter.title }}</span>
                          <span v-if="child2.chapter.id === currentChapter?.id" class="picker-item-badge">当前</span>
                          <span class="tree-count">{{ child2.chapter.word_count }}字</span>
                        </label>
                      </div>
                      <!-- 第四层（最深） -->
                      <template v-if="child2.chapter.node_type !== 'folder' || isPickerExpanded(child2.chapter)">
                        <template v-for="child3 in child2.children" :key="child3.chapter.id">
                          <div class="tree-node" :style="{ paddingLeft: child3.depth * 20 + 'px' }">
                            <label
                              class="tree-row tree-chapter"
                              :class="{ selected: selectedChapterIds.has(child3.chapter.id), current: child3.chapter.id === currentChapter?.id }"
                            >
                              <span class="tree-arrow-placeholder"></span>
                              <input
                                type="checkbox"
                                :checked="selectedChapterIds.has(child3.chapter.id)"
                                @change="toggleChapterSelection(child3.chapter.id)"
                              />
                              <svg class="tree-icon" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" width="16" height="16"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                              <span class="tree-label">{{ child3.chapter.title }}</span>
                              <span v-if="child3.chapter.id === currentChapter?.id" class="picker-item-badge">当前</span>
                              <span class="tree-count">{{ child3.chapter.word_count }}字</span>
                            </label>
                          </div>
                        </template>
                      </template>
                    </template>
                  </template>
                </template>
              </template>
            </template>
          </div>

          <div class="dialog-footer">
            <button v-if="selectedChapters.length > 0" class="clear-btn" @click="clearSelectedChapters">清空选择</button>
            <div class="footer-spacer"></div>
            <span class="selected-count">已选 {{ selectedChapters.length }} 个章节</span>
            <button class="submit-btn" @click="showChapterPicker = false">确定</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 选择提示词弹窗 -->
    <Teleport to="body">
      <div v-if="showPromptPicker" class="dialog-overlay" @click.self="showPromptPicker = false">
        <div class="dialog prompt-picker-dialog">
          <div class="dialog-header">
            <h2>选择提示词</h2>
            <button class="close-btn" @click="showPromptPicker = false">×</button>
          </div>

          <div class="dialog-body prompt-picker-body">
            <div v-if="promptLoading" class="picker-empty">加载中...</div>
            <div v-else-if="promptList.length === 0" class="picker-empty">暂无提示词，去提示词广场创建吧</div>
            <div
              v-for="p in promptList"
              :key="p.id"
              class="picker-item prompt-item"
              :class="{ selected: selectedPrompt?.id === p.id }"
              @click="selectPrompt(p)"
            >
              <div class="prompt-item-title">{{ p.title }}</div>
              <div class="prompt-item-desc">{{ p.description || p.content.slice(0, 60) + '...' }}</div>
              <div class="prompt-item-meta">
                <span class="prompt-category">{{ p.category }}</span>
                <span>使用 {{ p.usage_count }} 次</span>
              </div>
            </div>
          </div>

          <div class="dialog-footer">
            <button v-if="selectedPrompt" class="clear-btn" @click="clearSelectedPrompt">取消选择</button>
            <div class="footer-spacer"></div>
            <span v-if="selectedPrompt" class="selected-count">已选：{{ selectedPrompt.title }}</span>
            <button class="submit-btn" @click="showPromptPicker = false">确定</button>
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
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.panel-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
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

.chat-welcome .tip {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 12px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px dashed #e2e8f0;
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

/* 已选标签区域 */
.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 16px 0;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  max-width: 160px;
}

.tag-item span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tag-remove {
  font-size: 14px;
  line-height: 1;
  opacity: 0.6;
  margin-left: 2px;
}

.tag-item:hover .tag-remove {
  opacity: 1;
}

.chapter-tag {
  background: #ede9fe;
  color: #5b21b6;
  border: 1px solid #c4b5fd;
}

.chapter-tag:hover {
  background: #ddd6fe;
}

.prompt-tag {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.prompt-tag:hover {
  background: #fde68a;
}

/* 聊天工具栏 */
.chat-toolbar {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
}

.toolbar-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #64748b;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
}

.toolbar-btn:hover {
  background: #f1f5f9;
  color: #334155;
  border-color: #cbd5e1;
}

.toolbar-btn.active {
  background: #eef2ff;
  color: #4f46e5;
  border-color: #a5b4fc;
}

.toolbar-btn .badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  font-size: 10px;
  font-weight: 600;
  line-height: 1;
}

.toolbar-spacer {
  flex: 1;
}

.current-chapter-hint {
  font-size: 11px;
  color: #94a3b8;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 弹窗选择器通用样式 */
.chapter-picker-dialog {
  max-width: 680px;
  min-width: 520px;
}

.prompt-picker-dialog {
  max-width: 520px;
}

.chapter-picker-body,
.prompt-picker-body {
  max-height: 500px;
  overflow-y: auto;
  padding: 8px 12px;
}

/* 树状结构样式 */
.tree-node {
  /* 每个节点由 paddingLeft 控制缩进 */
}

.tree-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.1s;
  user-select: none;
}

.tree-row:hover {
  background: #f1f5f9;
}

.tree-folder {
  cursor: default;
  font-weight: 500;
  color: #1e40af;
}

.tree-folder:hover {
  background: #eff6ff;
}

.tree-chapter {
  color: #334155;
}

.tree-chapter.selected {
  background: #eef2ff;
  color: #4338ca;
}

.tree-chapter.current {
  opacity: 0.7;
}

.tree-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.15s;
  color: #94a3b8;
}

.tree-arrow.opened {
  transform: rotate(90deg);
}

.tree-arrow-placeholder {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.tree-icon {
  flex-shrink: 0;
}

.tree-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tree-folder-select-btn {
  font-size: 11px;
  padding: 2px 8px;
  border: 1px solid #dbeafe;
  border-radius: 4px;
  background: #eff6ff;
  color: #3b82f6;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.15s;
  flex-shrink: 0;
}

.tree-folder:hover .tree-folder-select-btn {
  opacity: 1;
}

.tree-folder-select-btn:hover {
  background: #dbeafe;
  border-color: #93c5fd;
}

.tree-chapter input[type="checkbox"] {
  accent-color: #6366f1;
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.tree-count {
  font-size: 11px;
  color: #94a3b8;
  flex-shrink: 0;
}

.picker-empty {
  padding: 32px 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

.clear-btn {
  background: none;
  border: none;
  color: #6366f1;
  font-size: 13px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
}

.clear-btn:hover {
  background: #eef2ff;
  color: #4338ca;
}

.footer-spacer {
  flex: 1;
}

.selected-count {
  font-size: 13px;
  color: #64748b;
}

.picker-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  font-size: 14px;
  color: #334155;
  cursor: pointer;
  transition: background 0.1s;
  border-radius: 8px;
  margin-bottom: 2px;
}

.picker-item:hover {
  background: #f8fafc;
}

.picker-item.selected {
  background: #eef2ff;
  color: #4338ca;
}

.picker-item.current {
  opacity: 0.6;
}

.picker-item input[type="checkbox"] {
  accent-color: #6366f1;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.picker-item-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.picker-item-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  background: #e2e8f0;
  color: #64748b;
}

.picker-item-count {
  font-size: 12px;
  color: #94a3b8;
  flex-shrink: 0;
}

/* 提示词选择弹窗专用样式 */
.prompt-item {
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 12px 14px;
  cursor: pointer;
  border: 1px solid #f1f5f9;
}

.prompt-item:hover {
  border-color: #e2e8f0;
}

.prompt-item.selected {
  border-color: #c7d2fe;
}

.prompt-item-title {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.prompt-item-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prompt-item-meta {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.prompt-category {
  padding: 2px 8px;
  background: #f1f5f9;
  border-radius: 4px;
  color: #6366f1;
}

.prompt-item.selected .prompt-item-title {
  color: #4338ca;
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

/* 类型切换器 */
.type-switcher {
  display: flex;
  gap: 8px;
}

.type-btn {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: center;
}

.type-btn:hover {
  background: #f8fafc;
}

.type-btn.active {
  background: #eef2ff;
  border-color: #6366f1;
  color: #4f46e5;
  font-weight: 500;
}
</style>
