<script setup lang="ts">
/**
 * ChapterTree.vue - 多级树状章节目录组件（递归渲染）
 * 功能：折叠/展开、右键菜单（重命名/复制/删除/添加子节点）、内联重命名
 * 参考设计：成章 Verse 目录导航
 */
import { ref, computed, nextTick } from 'vue'
import type { Chapter } from '../api/novel'

const props = defineProps<{
  chapters: Chapter[]
  activeChapterId?: string | null
}>()

const emit = defineEmits<{
  (e: 'select', chapter: Chapter): void
  (e: 'delete', chapterId: string): void
  (e: 'create', parentId: string | null, nodeType: 'folder' | 'chapter'): void
  (e: 'rename', chapterId: string, newTitle: string): void
  (e: 'copy', chapterId: string): void
  (e: 'update', chapterId: string, data: Partial<Chapter>): void
}>()

// ---- 本地折叠状态 ----
const localExpanded = ref<Record<string, boolean>>({})
const isExpanded = (ch: Chapter): boolean => {
  if (ch.id in localExpanded.value) return localExpanded.value[ch.id]
  return ch.is_expanded !== false
}
const toggleExpand = (ch: Chapter) => {
  localExpanded.value[ch.id] = !isExpanded(ch)
  emit('update', ch.id, { is_expanded: localExpanded.value[ch.id] })
}

// ---- 内联重命名 ----
const renamingId = ref<string | null>(null)
const renamingValue = ref('')

const startRename = (ch: Chapter) => {
  renamingId.value = ch.id
  renamingValue.value = ch.title
  nextTick(() => {
    const input = document.querySelector('.rename-input') as HTMLInputElement
    if (input) {
      input.focus()
      input.select()
    }
  })
}

const confirmRename = () => {
  if (!renamingId.value) return
  const val = renamingValue.value.trim()
  if (val && val !== props.chapters.find(c => c.id === renamingId.value)?.title) {
    emit('rename', renamingId.value, val)
  }
  renamingId.value = null
  renamingValue.value = ''
}

const cancelRename = () => {
  renamingId.value = null
  renamingValue.value = ''
}

const onRenameKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter') confirmRename()
  else if (e.key === 'Escape') cancelRename()
}

// ---- 悬浮操作按钮 ----
const hoveredId = ref<string | null>(null)

// ---- 构建树 ----
interface TreeNode { chapter: Chapter; children: TreeNode[] }

const treeData = computed<TreeNode[]>(() => {
  const map = new Map<string, TreeNode>()
  const roots: TreeNode[] = []
  for (const ch of props.chapters) {
    map.set(ch.id, { chapter: ch, children: [] })
  }
  for (const ch of props.chapters) {
    const node = map.get(ch.id)!
    if (ch.parent_id && map.has(ch.parent_id)) {
      map.get(ch.parent_id)!.children.push(node)
    } else {
      roots.push(node)
    }
  }
  const sort = (nodes: TreeNode[]) => {
    nodes.sort((a, b) => a.chapter.sort_order - b.chapter.sort_order || a.chapter.chapter_number - b.chapter.chapter_number)
    for (const n of nodes) sort(n.children)
  }
  sort(roots)
  return roots
})

// ---- 右键菜单 ----
const ctxMenu = ref<{ show: boolean; x: number; y: number; chapterId: string | null }>({
  show: false, x: 0, y: 0, chapterId: null,
})
const closeCtxMenu = () => { ctxMenu.value.show = false }

const onContextMenu = (e: MouseEvent, ch: Chapter) => {
  e.preventDefault()
  e.stopPropagation()
  ctxMenu.value = { show: true, x: e.clientX, y: e.clientY, chapterId: ch.id }
}

const handleCtxAction = (action: string) => {
  const id = ctxMenu.value.chapterId
  closeCtxMenu()
  if (!id) return
  const ch = props.chapters.find(c => c.id === id)
  if (!ch) return

  switch (action) {
    case 'rename':
      startRename(ch)
      break
    case 'copy': emit('copy', id); break
    case 'delete': emit('delete', id); break
    case 'add-chapter': emit('create', id, 'chapter'); break
    case 'add-folder': emit('create', id, 'folder'); break
  }
}

// ---- 递归子节点 ----
const getChildren = (chapterId: string): Chapter[] =>
  props.chapters.filter(c => c.parent_id === chapterId)

const countDescendants = (chapterId: string): number => {
  const children = getChildren(chapterId)
  return children.reduce((sum, c) => sum + 1 + countDescendants(c.id), 0)
}
</script>

<template>
  <div class="chapter-tree" @click="closeCtxMenu">
    <!-- 工具栏 -->
    <div class="tree-toolbar">
      <button class="toolbar-btn" @click.stop="emit('create', null, 'folder')" title="新建文件夹">
        <svg class="toolbar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>
        文件夹
      </button>
      <button class="toolbar-btn" @click.stop="emit('create', null, 'chapter')" title="新建章节">
        <svg class="toolbar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
        章节
      </button>
    </div>

    <div class="tree-content">
      <!-- 递归渲染 -->
      <template v-if="treeData.length > 0">
        <div v-for="node in treeData" :key="node.chapter.id">
          <!-- 顶层节点 -->
          <div
            class="tree-row"
            :class="{ 'is-active': activeChapterId === node.chapter.id, 'is-folder': node.chapter.node_type === 'folder' }"
            :style="{ paddingLeft: '12px' }"
            @click.stop="emit('select', node.chapter)"
            @contextmenu="onContextMenu($event, node.chapter)"
            @mouseenter="hoveredId = node.chapter.id"
            @mouseleave="hoveredId = null"
          >
            <!-- 展开/折叠箭头 -->
            <span v-if="node.chapter.node_type === 'folder'" class="tree-arrow" :class="{ opened: isExpanded(node.chapter) }" @click.stop="toggleExpand(node.chapter)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </span>
            <span v-else class="tree-arrow-placeholder"></span>
            <!-- 图标 -->
            <span class="tree-icon">
              <svg v-if="node.chapter.node_type === 'folder'" class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
              <svg v-else class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
            </span>
            <!-- 标题 / 重命名输入框 -->
            <template v-if="renamingId === node.chapter.id">
              <input
                v-model="renamingValue"
                class="rename-input"
                @blur="confirmRename"
                @keydown="onRenameKeydown"
                @click.stop
              />
            </template>
            <template v-else>
              <span class="tree-label">{{ node.chapter.title || '未命名' }}</span>
            </template>
            <!-- 悬浮操作按钮 -->
            <div v-if="hoveredId === node.chapter.id && renamingId !== node.chapter.id" class="row-actions" @click.stop>
              <button class="row-action-btn" title="添加子章节" @click="emit('create', node.chapter.id, 'chapter')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              </button>
              <button class="row-action-btn" title="重命名" @click="startRename(node.chapter)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button class="row-action-btn danger" title="删除" @click="emit('delete', node.chapter.id)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
              </button>
            </div>
          </div>

          <!-- 子节点（递归一层） -->
          <template v-if="node.chapter.node_type === 'folder' && isExpanded(node.chapter)">
            <div v-for="child in node.children" :key="child.chapter.id">
              <div
                class="tree-row"
                :class="{ 'is-active': activeChapterId === child.chapter.id, 'is-folder': child.chapter.node_type === 'folder' }"
                :style="{ paddingLeft: '36px' }"
                @click.stop="emit('select', child.chapter)"
                @contextmenu="onContextMenu($event, child.chapter)"
                @mouseenter="hoveredId = child.chapter.id"
                @mouseleave="hoveredId = null"
              >
                <span v-if="child.chapter.node_type === 'folder'" class="tree-arrow" :class="{ opened: isExpanded(child.chapter) }" @click.stop="toggleExpand(child.chapter)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                </span>
                <span v-else class="tree-arrow-placeholder"></span>
                <span class="tree-icon">
                  <svg v-if="child.chapter.node_type === 'folder'" class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                  <svg v-else class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                </span>
                <template v-if="renamingId === child.chapter.id">
                  <input
                    v-model="renamingValue"
                    class="rename-input"
                    @blur="confirmRename"
                    @keydown="onRenameKeydown"
                    @click.stop
                  />
                </template>
                <template v-else>
                  <span class="tree-label">{{ child.chapter.title || '未命名' }}</span>
                </template>
                <div v-if="hoveredId === child.chapter.id && renamingId !== child.chapter.id" class="row-actions" @click.stop>
                  <button class="row-action-btn" title="添加子章节" @click="emit('create', child.chapter.id, 'chapter')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  </button>
                  <button class="row-action-btn" title="重命名" @click="startRename(child.chapter)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  </button>
                  <button class="row-action-btn danger" title="删除" @click="emit('delete', child.chapter.id)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                  </button>
                </div>
              </div>

              <!-- 第三层 -->
              <template v-if="child.chapter.node_type === 'folder' && isExpanded(child.chapter)">
                <div v-for="gc in getChildren(child.chapter.id)" :key="gc.id">
                  <div
                    class="tree-row"
                    :class="{ 'is-active': activeChapterId === gc.id, 'is-folder': gc.node_type === 'folder' }"
                    :style="{ paddingLeft: '60px' }"
                    @click.stop="emit('select', gc)"
                    @contextmenu="onContextMenu($event, gc)"
                    @mouseenter="hoveredId = gc.id"
                    @mouseleave="hoveredId = null"
                  >
                    <span v-if="gc.node_type === 'folder'" class="tree-arrow" :class="{ opened: isExpanded(gc) }" @click.stop="toggleExpand(gc)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                    </span>
                    <span v-else class="tree-arrow-placeholder"></span>
                    <span class="tree-icon">
                      <svg v-if="gc.node_type === 'folder'" class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                      <svg v-else class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                    </span>
                    <template v-if="renamingId === gc.id">
                      <input
                        v-model="renamingValue"
                        class="rename-input"
                        @blur="confirmRename"
                        @keydown="onRenameKeydown"
                        @click.stop
                      />
                    </template>
                    <template v-else>
                      <span class="tree-label">{{ gc.title || '未命名' }}</span>
                    </template>
                    <div v-if="hoveredId === gc.id && renamingId !== gc.id" class="row-actions" @click.stop>
                      <button class="row-action-btn" title="添加子章节" @click="emit('create', gc.id, 'chapter')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                      </button>
                      <button class="row-action-btn" title="重命名" @click="startRename(gc)">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                      </button>
                      <button class="row-action-btn danger" title="删除" @click="emit('delete', gc.id)">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                      </button>
                    </div>
                  </div>

                  <!-- 第四层 -->
                  <template v-if="gc.node_type === 'folder' && isExpanded(gc)">
                    <div v-for="ggc in getChildren(gc.id)" :key="ggc.id">
                      <div
                        class="tree-row"
                        :class="{ 'is-active': activeChapterId === ggc.id, 'is-folder': ggc.node_type === 'folder' }"
                        :style="{ paddingLeft: '84px' }"
                        @click.stop="emit('select', ggc)"
                        @contextmenu="onContextMenu($event, ggc)"
                        @mouseenter="hoveredId = ggc.id"
                        @mouseleave="hoveredId = null"
                      >
                        <span v-if="ggc.node_type === 'folder'" class="tree-arrow" :class="{ opened: isExpanded(ggc) }" @click.stop="toggleExpand(ggc)">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                        </span>
                        <span v-else class="tree-arrow-placeholder"></span>
                        <span class="tree-icon">
                          <svg v-if="ggc.node_type === 'folder'" class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                          <svg v-else class="icon-svg" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>
                        </span>
                        <template v-if="renamingId === ggc.id">
                          <input
                            v-model="renamingValue"
                            class="rename-input"
                            @blur="confirmRename"
                            @keydown="onRenameKeydown"
                            @click.stop
                          />
                        </template>
                        <template v-else>
                          <span class="tree-label">{{ ggc.title || '未命名' }}</span>
                        </template>
                        <div v-if="hoveredId === ggc.id && renamingId !== ggc.id" class="row-actions" @click.stop>
                          <button class="row-action-btn" title="添加子章节" @click="emit('create', ggc.id, 'chapter')">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                          </button>
                          <button class="row-action-btn" title="重命名" @click="startRename(ggc)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                          </button>
                          <button class="row-action-btn danger" title="删除" @click="emit('delete', ggc.id)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>
              </template>
            </div>
          </template>
        </div>
      </template>

      <!-- 空状态 -->
      <div v-else class="empty-tree">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
        </div>
        <p>暂无内容，开始创建吧</p>
        <button class="empty-add-btn" @click.stop="emit('create', null, 'folder')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>
          创建文件夹
        </button>
        <button class="empty-add-btn secondary" @click.stop="emit('create', null, 'chapter')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          创建章节
        </button>
      </div>
    </div>

    <!-- 右键菜单 -->
    <Teleport to="body">
      <div v-if="ctxMenu.show" class="ctx-overlay" @click="closeCtxMenu" @contextmenu.prevent="closeCtxMenu">
        <div class="ctx-menu" :style="{ left: ctxMenu.x + 'px', top: ctxMenu.y + 'px' }" @click.stop>
          <button class="ctx-item" @click="handleCtxAction('rename')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ctx-icon"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            重命名
          </button>
          <button class="ctx-item" @click="handleCtxAction('copy')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ctx-icon"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            复制
          </button>
          <div class="ctx-divider"></div>
          <button class="ctx-item" @click="handleCtxAction('add-chapter')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ctx-icon"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
            添加子章节
          </button>
          <button class="ctx-item" @click="handleCtxAction('add-folder')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ctx-icon"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>
            添加子文件夹
          </button>
          <div class="ctx-divider"></div>
          <button class="ctx-item danger" @click="handleCtxAction('delete')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ctx-icon"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
            删除
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.chapter-tree {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

/* ---- 工具栏 ---- */
.tree-toolbar {
  display: flex;
  gap: 6px;
  padding: 10px 12px;
  border-bottom: 1px solid #e8eaed;
  flex-shrink: 0;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  border: 1px solid #dadce0;
  border-radius: 6px;
  background: #fff;
  font-size: 12px;
  color: #5f6368;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
}

.toolbar-btn:hover {
  background: #f1f3f4;
  border-color: #bdc1c6;
  color: #202124;
}

.toolbar-icon {
  width: 14px;
  height: 14px;
}

/* ---- 树内容 ---- */
.tree-content {
  flex: 1;
  overflow-y: auto;
  padding: 4px 0;
}

/* ---- 树行 ---- */
.tree-row {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 32px;
  padding-right: 8px;
  cursor: pointer;
  transition: background 0.1s;
  user-select: none;
  position: relative;
}

.tree-row:hover {
  background: #f1f3f4;
}

.tree-row.is-active {
  background: #e8f0fe;
}

.tree-row.is-active .tree-label {
  color: #1967d2;
  font-weight: 500;
}

/* ---- 箭头 ---- */
.tree-arrow {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9aa0a6;
  flex-shrink: 0;
  transition: transform 0.15s;
  cursor: pointer;
  border-radius: 4px;
}

.tree-arrow:hover {
  background: #e8eaed;
  color: #5f6368;
}

.tree-arrow svg {
  width: 12px;
  height: 12px;
}

.tree-arrow.opened {
  transform: rotate(90deg);
}

.tree-arrow-placeholder {
  width: 18px;
  flex-shrink: 0;
}

/* ---- 图标 ---- */
.tree-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-svg {
  width: 16px;
  height: 16px;
}

/* ---- 标签 ---- */
.tree-label {
  flex: 1;
  font-size: 13px;
  color: #3c4043;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

/* ---- 悬浮操作按钮 ---- */
.row-actions {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-left: auto;
  flex-shrink: 0;
}

.row-action-btn {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #9aa0a6;
  cursor: pointer;
  border-radius: 4px;
  padding: 0;
  transition: all 0.12s;
}

.row-action-btn:hover {
  background: #e8eaed;
  color: #3c4043;
}

.row-action-btn.danger:hover {
  background: #fce8e6;
  color: #d93025;
}

.row-action-btn svg {
  width: 14px;
  height: 14px;
}

/* ---- 内联重命名输入框 ---- */
.rename-input {
  flex: 1;
  height: 22px;
  padding: 0 6px;
  border: 1px solid #1a73e8;
  border-radius: 4px;
  font-size: 13px;
  color: #202124;
  background: #fff;
  outline: none;
  font-family: inherit;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
}

/* ---- 空状态 ---- */
.empty-tree {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 20px;
  text-align: center;
}

.empty-icon {
  margin-bottom: 12px;
  color: #dadce0;
}

.empty-tree p {
  font-size: 13px;
  color: #9aa0a6;
  margin: 0 0 18px;
}

.empty-add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  border: 1px dashed #dadce0;
  border-radius: 6px;
  background: transparent;
  color: #5f6368;
  font-size: 13px;
  cursor: pointer;
  margin-bottom: 8px;
  width: 160px;
  justify-content: center;
  transition: all 0.15s;
  font-family: inherit;
}

.empty-add-btn:hover {
  background: #f1f3f4;
  border-color: #bdc1c6;
  color: #3c4043;
}

/* ---- 右键菜单 ---- */
.ctx-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
}

.ctx-menu {
  position: fixed;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
  padding: 4px;
  min-width: 180px;
  z-index: 10000;
}

.ctx-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 14px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 13px;
  color: #3c4043;
  cursor: pointer;
  text-align: left;
  transition: background 0.1s;
  font-family: inherit;
}

.ctx-item:hover {
  background: #f1f3f4;
}

.ctx-item.danger {
  color: #d93025;
}

.ctx-item.danger:hover {
  background: #fce8e6;
}

.ctx-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.ctx-divider {
  height: 1px;
  background: #e8eaed;
  margin: 4px 0;
}
</style>
