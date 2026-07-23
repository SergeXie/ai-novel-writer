<script setup lang="ts">
/**
 * SnippetsView.vue - 我的词条页面
 * 管理创作中常用的词汇、短语、设定等
 */
import { ref, onMounted } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'
import { getSnippets, createSnippet, deleteSnippet, type Snippet } from '../api/novel'

const snippets = ref<Snippet[]>([])
const loading = ref(false)
const showCreateDialog = ref(false)
const newSnippet = ref({ title: '', content: '', category: '自定义' })

const categories = ['人物设定', '世界观', '道具', '术语', '自定义']

const loadSnippets = async () => {
  loading.value = true
  try {
    const data = await getSnippets()
    snippets.value = data.items
  } catch (e) {
    console.error('加载词条失败:', e)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  if (!newSnippet.value.title.trim()) return
  try {
    await createSnippet(newSnippet.value)
    showCreateDialog.value = false
    newSnippet.value = { title: '', content: '', category: '自定义' }
    await loadSnippets()
  } catch (e) {
    console.error('创建失败:', e)
  }
}

const handleDelete = async (id: string) => {
  if (!confirm('确定删除这个词条吗？')) return
  try {
    await deleteSnippet(id)
    await loadSnippets()
  } catch (e) {
    console.error('删除失败:', e)
  }
}

const getCategoryColor = (cat: string) => {
  const m: Record<string, string> = {
    '人物设定': '#3b82f6', '世界观': '#8b5cf6', '道具': '#f59e0b',
    '术语': '#10b981', '自定义': '#64748b',
  }
  return m[cat] || '#64748b'
}

onMounted(() => loadSnippets())
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <div class="header-left">
          <h1 class="page-title">我的词条</h1>
          <span class="count-badge">{{ snippets.length }}</span>
        </div>
        <button class="create-btn" @click="showCreateDialog = true">
          <span>+</span> 新建词条
        </button>
      </header>

      <div v-if="loading" class="loading-state"><div class="spinner"></div></div>

      <div v-else-if="snippets.length === 0" class="empty-state">
        <div class="empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg></div>
        <h3>还没有词条</h3>
        <p>创建词条来管理你小说中的设定和术语</p>
      </div>

      <div v-else class="snippet-grid">
        <div v-for="s in snippets" :key="s.id" class="snippet-card" @click="() => {}">
          <div class="snippet-header">
            <span class="snippet-cat" :style="{ background: getCategoryColor(s.category) + '20', color: getCategoryColor(s.category) }">
              {{ s.category }}
            </span>
            <button class="delete-btn" @click="handleDelete(s.id)">×</button>
          </div>
          <h3 class="snippet-title">{{ s.title }}</h3>
          <p class="snippet-content">{{ s.content || '暂无内容' }}</p>
        </div>
      </div>

      <!-- 弹窗 -->
      <Teleport to="body">
        <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
          <div class="dialog">
            <div class="dialog-header">
              <h2>新建词条</h2>
              <button class="close-btn" @click="showCreateDialog = false">×</button>
            </div>
            <div class="dialog-body">
              <div class="form-group">
                <label>分类</label>
                <select v-model="newSnippet.category" class="form-select">
                  <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>名称 <span class="req">*</span></label>
                <input v-model="newSnippet.title" class="form-input" placeholder="输入词条名称" />
              </div>
              <div class="form-group">
                <label>内容</label>
                <textarea v-model="newSnippet.content" class="form-textarea" rows="5" placeholder="输入词条内容..."></textarea>
              </div>
            </div>
            <div class="dialog-footer">
              <button class="cancel-btn" @click="showCreateDialog = false">取消</button>
              <button class="submit-btn" @click="handleCreate" :disabled="!newSnippet.title.trim()">创建</button>
            </div>
          </div>
        </div>
      </Teleport>
    </main>
  </div>
</template>

<style scoped>
.page-layout { display: flex; width: calc(100% + 4rem); margin-left: -2rem; margin-top: -2rem; height: calc(100vh - 50px); background: #f5f7fa; overflow: hidden; }
.content-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
.page-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 32px; background: white; border-bottom: 1px solid #e5e7eb; flex-shrink: 0; }
.header-left { display: flex; align-items: center; gap: 12px; }
.page-title { font-size: 22px; font-weight: 700; color: #1e293b; margin: 0; }
.count-badge { font-size: 13px; color: #94a3b8; background: #f1f5f9; padding: 2px 10px; border-radius: 12px; }
.create-btn { display: flex; align-items: center; gap: 6px; padding: 10px 20px; background: #1d4ed8; color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
.create-btn:hover { background: #1e40af; }

.loading-state { display: flex; align-items: center; justify-content: center; padding: 120px 0; }
.spinner { width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: #1d4ed8; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; padding: 120px 0; }
.empty-icon { font-size: 56px; margin-bottom: 20px; }
.empty-state h3 { font-size: 18px; color: #1e293b; margin: 0 0 8px; }
.empty-state p { font-size: 14px; color: #94a3b8; margin: 0; }

.snippet-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; padding: 24px 32px; overflow-y: auto; align-content: start; }
.snippet-card { background: white; border-radius: 12px; padding: 20px; border: 1px solid #f0f0f0; cursor: pointer; transition: all 0.2s; }
.snippet-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); transform: translateY(-1px); }
.snippet-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.snippet-cat { padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
.delete-btn { width: 28px; height: 28px; border: none; border-radius: 6px; background: transparent; color: #94a3b8; cursor: pointer; font-size: 18px; opacity: 0; }
.snippet-card:hover .delete-btn { opacity: 1; }
.delete-btn:hover { background: #fef2f2; color: #ef4444; }
.snippet-title { font-size: 16px; font-weight: 600; color: #1e293b; margin: 0 0 8px; }
.snippet-content { font-size: 14px; color: #64748b; line-height: 1.6; margin: 0; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.dialog { background: white; border-radius: 16px; width: 100%; max-width: 480px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.dialog-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 24px 0; }
.dialog-header h2 { font-size: 20px; font-weight: 600; color: #1e293b; margin: 0; }
.close-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: #f1f5f9; cursor: pointer; font-size: 20px; color: #64748b; display: flex; align-items: center; justify-content: center; }
.dialog-body { padding: 24px; }
.form-group { margin-bottom: 16px; }
.form-group:last-child { margin-bottom: 0; }
.form-group label { display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 6px; }
.req { color: #ef4444; }
.form-input, .form-select, .form-textarea { width: 100%; padding: 10px 14px; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 14px; color: #1e293b; background: #f9fafb; box-sizing: border-box; }
.form-input:focus, .form-select:focus, .form-textarea:focus { outline: none; border-color: #1d4ed8; background: white; box-shadow: 0 0 0 3px rgba(29,78,216,0.1); }
.form-textarea { resize: vertical; min-height: 80px; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 0 24px 24px; }
.cancel-btn { padding: 10px 20px; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #374151; font-size: 14px; cursor: pointer; }
.submit-btn { padding: 10px 20px; border: none; border-radius: 8px; background: #1d4ed8; color: white; font-size: 14px; font-weight: 600; cursor: pointer; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
