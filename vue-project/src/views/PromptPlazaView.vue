<script setup lang="ts">
/**
 * PromptPlazaView.vue - 提示词广场（后端版）
 * 连接后端API，支持增删改查
 */
import { ref, onMounted } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'
import {
  getPrompts, createPrompt, updatePrompt, deletePrompt,
  usePrompt, likePrompt, type Prompt
} from '../api/novel'

// 数据
const prompts = ref<Prompt[]>([])
const loading = ref(false)
const total = ref(0)

// 分类
const activeCategory = ref('')
const categories = [
  { id: '', label: '全部', icon: 'clipboard' },
  { id: '角色塑造', label: '角色塑造', icon: 'user' },
  { id: '情节构思', label: '情节构思', icon: 'book' },
  { id: '世界观', label: '世界观', icon: 'globe' },
  { id: '对话润色', label: '对话润色', icon: 'message' },
  { id: '改写优化', label: '改写优化', icon: 'edit' },
  { id: '大纲生成', label: '大纲生成', icon: 'list' },
  { id: '其他', label: '其他', icon: 'folder' },
]

// 弹窗状态
const showDialog = ref(false)
const isEdit = ref(false)
const editingId = ref('')
const formData = ref({
  title: '',
  description: '',
  content: '',
  category: '其他',
  is_public: true,
})

// 加载数据
const loadPrompts = async () => {
  loading.value = true
  try {
    const data = await getPrompts(1, 50, activeCategory.value || undefined)
    prompts.value = data.items
    total.value = data.total
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    loading.value = false
  }
}

const filterByCategory = (cat: string) => {
  activeCategory.value = cat
  loadPrompts()
}

// 新建
const openCreate = () => {
  isEdit.value = false
  editingId.value = ''
  formData.value = { title: '', description: '', content: '', category: '其他', is_public: true }
  showDialog.value = true
}

// 编辑
const openEdit = (p: Prompt, e: Event) => {
  e.stopPropagation()
  isEdit.value = true
  editingId.value = p.id
  formData.value = {
    title: p.title,
    description: p.description || '',
    content: p.content,
    category: p.category,
    is_public: p.is_public,
  }
  showDialog.value = true
}

// 保存
const handleSave = async () => {
  if (!formData.value.title.trim() || !formData.value.content.trim()) return
  try {
    if (isEdit.value) {
      await updatePrompt(editingId.value, formData.value)
    } else {
      await createPrompt(formData.value)
    }
    showDialog.value = false
    await loadPrompts()
  } catch (e) {
    console.error('保存失败:', e)
  }
}

// 删除
const handleDelete = async (id: string, e: Event) => {
  e.stopPropagation()
  if (!confirm('确定删除这个提示词吗？')) return
  try {
    await deletePrompt(id)
    await loadPrompts()
  } catch (e) {
    console.error('删除失败:', e)
  }
}

// 使用
const showUseDialog = ref(false)
const selectedPrompt = ref<Prompt | null>(null)
const useContent = ref('')

const openUseDialog = async (p: Prompt) => {
  selectedPrompt.value = p
  useContent.value = p.content
  showUseDialog.value = true
  // 增加使用次数
  try { await usePrompt(p.id) } catch {}
  // 更新本地数据
  p.usage_count++
}

const copyContent = () => {
  navigator.clipboard.writeText(useContent.value)
}

// 点赞
const handleLike = async (p: Prompt, e: Event) => {
  e.stopPropagation()
  try {
    const res = await likePrompt(p.id)
    p.like_count = res.like_count
  } catch {}
}

// 复制
const copiedId = ref('')
const copyPrompt = (p: Prompt, e: Event) => {
  e.stopPropagation()
  navigator.clipboard.writeText(p.content)
  copiedId.value = p.id
  setTimeout(() => copiedId.value = '', 2000)
}

onMounted(() => loadPrompts())
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <div class="header-left">
          <h1 class="page-title">提示词广场</h1>
          <span class="count-badge">{{ total }}</span>
        </div>
        <button class="create-btn" @click="openCreate">
          <span>+</span> 创建提示词
        </button>
      </header>

      <!-- 分类栏 -->
      <div class="category-bar">
        <button
          v-for="cat in categories"
          :key="cat.id"
          class="cat-btn"
          :class="{ active: activeCategory === cat.id }"
          @click="filterByCategory(cat.id)"
        >
          <span>{{ cat.icon }}</span>
          <span>{{ cat.label }}</span>
        </button>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="loading-state"><div class="spinner"></div></div>

      <!-- 空状态 -->
      <div v-else-if="prompts.length === 0" class="empty-state">
        <div class="empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
        <h3>暂无提示词</h3>
        <p>点击「创建提示词」添加你的第一个提示词模板</p>
      </div>

      <!-- 提示词列表 -->
      <div v-else class="prompt-grid">
        <div
          v-for="p in prompts"
          :key="p.id"
          class="prompt-card"
          @click="openUseDialog(p)"
        >
          <div class="card-header">
            <h3 class="card-title">{{ p.title }}</h3>
            <span class="cat-tag">{{ p.category }}</span>
          </div>
          <p class="card-desc">{{ p.description || p.content.substring(0, 80) }}</p>
          <div class="card-preview">{{ p.content }}</div>
          <div class="card-footer">
            <div class="card-stats">
              <span class="stat-item" @click="handleLike(p, $event)">
                ♥ {{ p.like_count }}
              </span>
              <span class="stat-item">▸ {{ p.usage_count }}</span>
            </div>
            <div class="card-actions">
              <button
                class="action-btn copy-btn"
                :class="{ copied: copiedId === p.id }"
                @click="copyPrompt(p, $event)"
              >
                {{ copiedId === p.id ? '✓' : '⧉' }}
              </button>
              <button class="action-btn edit-btn" @click="openEdit(p, $event)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>
              <button class="action-btn delete-btn" @click="handleDelete(p.id, $event)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
            </div>
          </div>
        </div>
      </div>

      <!-- 编辑/新建弹窗 -->
      <Teleport to="body">
        <div v-if="showDialog" class="dialog-overlay" @click.self="showDialog = false">
          <div class="dialog">
            <div class="dialog-header">
              <h2>{{ isEdit ? '编辑提示词' : '创建提示词' }}</h2>
              <button class="close-btn" @click="showDialog = false">×</button>
            </div>
            <div class="dialog-body">
              <div class="form-row">
                <div class="form-group flex-1">
                  <label>标题 <span class="req">*</span></label>
                  <input v-model="formData.title" class="form-input" placeholder="输入提示词标题" />
                </div>
                <div class="form-group" style="width: 140px">
                  <label>分类</label>
                  <select v-model="formData.category" class="form-select">
                    <option v-for="c in categories.filter(c => c.id)" :key="c.id" :value="c.id">{{ c.label }}</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>描述</label>
                <input v-model="formData.description" class="form-input" placeholder="简要描述提示词用途（选填）" />
              </div>
              <div class="form-group">
                <label>提示词内容 <span class="req">*</span></label>
                <textarea v-model="formData.content" class="form-textarea" rows="10" placeholder="输入提示词内容，使用 [方括号] 标记需要用户填写的部分"></textarea>
              </div>
              <div class="form-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="formData.is_public" />
                  <span>公开此提示词（其他用户可见）</span>
                </label>
              </div>
            </div>
            <div class="dialog-footer">
              <button class="cancel-btn" @click="showDialog = false">取消</button>
              <button
                class="submit-btn"
                @click="handleSave"
                :disabled="!formData.title.trim() || !formData.content.trim()"
              >
                {{ isEdit ? '保存' : '创建' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 使用弹窗 -->
        <div v-if="showUseDialog" class="dialog-overlay" @click.self="showUseDialog = false">
          <div class="dialog">
            <div class="dialog-header">
              <h2>{{ selectedPrompt?.title }}</h2>
              <button class="close-btn" @click="showUseDialog = false">×</button>
            </div>
            <div class="dialog-body">
              <p class="dialog-desc">{{ selectedPrompt?.description }}</p>
              <label class="dialog-label">提示词内容（可编辑后复制）</label>
              <textarea v-model="useContent" class="form-textarea" rows="12"></textarea>
              <p class="dialog-hint">修改 [方括号] 中的内容为你的具体内容，然后复制使用</p>
            </div>
            <div class="dialog-footer">
              <button class="cancel-btn" @click="showUseDialog = false">关闭</button>
              <button class="submit-btn" @click="copyContent">复制提示词</button>
            </div>
          </div>
        </div>
      </Teleport>
    </main>
  </div>
</template>

<style scoped>
.page-layout {
  display: flex;
  width: calc(100% + 4rem);
  margin-left: -2rem;
  margin-top: -2rem;
  height: calc(100vh - 50px);
  background: #f5f7fa;
  overflow: hidden;
}
.content-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
.page-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 32px; background: white; border-bottom: 1px solid #e5e7eb; flex-shrink: 0; }
.header-left { display: flex; align-items: center; gap: 12px; }
.page-title { font-size: 22px; font-weight: 700; color: #1e293b; margin: 0; }
.count-badge { font-size: 13px; color: #94a3b8; background: #f1f5f9; padding: 2px 10px; border-radius: 12px; }
.create-btn { display: flex; align-items: center; gap: 6px; padding: 10px 20px; background: #1d4ed8; color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
.create-btn:hover { background: #1e40af; }

/* 分类 */
.category-bar { display: flex; gap: 8px; padding: 16px 32px; background: white; border-bottom: 1px solid #e5e7eb; overflow-x: auto; flex-shrink: 0; }
.cat-btn { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border: 1px solid #e5e7eb; border-radius: 20px; background: white; color: #475569; font-size: 14px; cursor: pointer; white-space: nowrap; transition: all 0.2s; }
.cat-btn:hover { border-color: #1d4ed8; color: #1d4ed8; }
.cat-btn.active { background: #1d4ed8; border-color: #1d4ed8; color: white; }

/* 加载和空状态 */
.loading-state { display: flex; align-items: center; justify-content: center; padding: 120px 0; }
.spinner { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #1d4ed8; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { display: flex; flex-direction: column; align-items: center; padding: 120px 0; }
.empty-icon { font-size: 56px; margin-bottom: 20px; }
.empty-state h3 { font-size: 18px; color: #1e293b; margin: 0 0 8px; }
.empty-state p { font-size: 14px; color: #94a3b8; margin: 0; }

/* 网格 */
.prompt-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; padding: 24px 32px; overflow-y: auto; align-content: start; }

/* 卡片 */
.prompt-card { background: white; border-radius: 12px; border: 1px solid #f0f0f0; cursor: pointer; transition: all 0.25s; }
.prompt-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.08); transform: translateY(-2px); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; padding: 20px 20px 0; }
.card-title { font-size: 16px; font-weight: 600; color: #1e293b; margin: 0; flex: 1; }
.cat-tag { padding: 3px 10px; background: #eff6ff; color: #2563eb; border-radius: 12px; font-size: 12px; flex-shrink: 0; }
.card-desc { padding: 8px 20px 0; font-size: 14px; color: #64748b; margin: 0; }
.card-preview { margin: 12px 20px; padding: 12px; background: #f8fafc; border-radius: 8px; font-size: 13px; color: #475569; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; white-space: pre-line; }
.card-footer { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-top: 1px solid #f5f5f5; }
.card-stats { display: flex; gap: 16px; }
.stat-item { font-size: 13px; color: #94a3b8; cursor: pointer; }
.stat-item:hover { color: #ef4444; }
.card-actions { display: flex; gap: 4px; }
.action-btn { width: 30px; height: 30px; border: none; border-radius: 6px; background: transparent; font-size: 14px; cursor: pointer; opacity: 0; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }
.prompt-card:hover .action-btn { opacity: 1; }
.copy-btn.copied { opacity: 1 !important; color: #16a34a; }
.edit-btn:hover { background: #eff6ff; }
.delete-btn:hover { background: #fef2f2; }

/* 弹窗 */
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.dialog { background: white; border-radius: 16px; width: 100%; max-width: 560px; max-height: 85vh; display: flex; flex-direction: column; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.dialog-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 24px 0; }
.dialog-header h2 { font-size: 18px; font-weight: 600; color: #1e293b; margin: 0; }
.close-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: #f1f5f9; cursor: pointer; font-size: 20px; color: #64748b; display: flex; align-items: center; justify-content: center; }
.close-btn:hover { background: #e2e8f0; }
.dialog-body { padding: 20px 24px; overflow-y: auto; flex: 1; }
.dialog-desc { font-size: 14px; color: #64748b; margin: 0 0 16px; }
.dialog-label { display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px; }
.dialog-hint { font-size: 13px; color: #94a3b8; margin: 12px 0 0; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 16px 24px; border-top: 1px solid #f0f0f0; }

/* 表单 */
.form-row { display: flex; gap: 16px; }
.flex-1 { flex: 1; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 6px; }
.req { color: #ef4444; }
.form-input, .form-select, .form-textarea { width: 100%; padding: 10px 14px; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 14px; color: #1e293b; background: #f9fafb; box-sizing: border-box; transition: all 0.2s; }
.form-input:focus, .form-select:focus, .form-textarea:focus { outline: none; border-color: #1d4ed8; background: white; box-shadow: 0 0 0 3px rgba(29,78,216,0.1); }
.form-textarea { resize: vertical; min-height: 80px; font-family: inherit; line-height: 1.6; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-weight: 400 !important; }
.checkbox-label input { width: 16px; height: 16px; }
.cancel-btn { padding: 10px 20px; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #475569; font-size: 14px; cursor: pointer; }
.submit-btn { padding: 10px 20px; border: none; border-radius: 8px; background: #1d4ed8; color: white; font-size: 14px; font-weight: 500; cursor: pointer; }
.submit-btn:hover:not(:disabled) { background: #1e40af; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
