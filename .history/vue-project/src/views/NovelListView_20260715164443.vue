<script setup lang="ts">
/**
 * NovelListView.vue - 小说项目列表页面
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from '../components/AppSidebar.vue'
import { getProjects, createProject, deleteProject, type NovelProject } from '../api/novel'

const router = useRouter()

// 项目列表
const projects = ref<NovelProject[]>([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

// 新建项目弹窗
const showCreateDialog = ref(false)
const newProject = ref({
  title: '',
  description: '',
  genre: '',
})

// 类型选项
const genreOptions = [
  '玄幻', '奇幻', '武侠', '仙侠', '都市',
  '现实', '军事', '历史', '游戏', '体育',
  '科幻', '悬疑', '灵异', '言情', '其他',
]

// 加载项目列表
const loadProjects = async () => {
  loading.value = true
  try {
    const data = await getProjects(page.value, pageSize.value)
    projects.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('加载项目失败:', error)
  } finally {
    loading.value = false
  }
}

// 创建项目
const handleCreateProject = async () => {
  if (!newProject.value.title.trim()) return
  try {
    await createProject({
      title: newProject.value.title,
      description: newProject.value.description || undefined,
      genre: newProject.value.genre || undefined,
    })
    showCreateDialog.value = false
    newProject.value = { title: '', description: '', genre: '' }
    await loadProjects()
  } catch (error) {
    console.error('创建项目失败:', error)
  }
}

// 删除项目
const handleDeleteProject = async (projectId: string, event: Event) => {
  event.stopPropagation()
  if (!confirm('确定要删除这个项目吗？此操作不可恢复。')) return
  try {
    await deleteProject(projectId)
    await loadProjects()
  } catch (error) {
    console.error('删除项目失败:', error)
  }
}

// 进入项目编辑页面
const openProject = (projectId: string) => {
  router.push(`/novel/${projectId}`)
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

// 获取状态
const getStatusText = (s: string) => ({ draft: '草稿', writing: '创作中', completed: '已完成' }[s] || s)
const getStatusClass = (s: string) => `status-${s}`

// 获取类型渐变色
const getGenreColors = (genre: string | null): [string, string] => {
  const m: Record<string, [string, string]> = {
    '玄幻': ['#f97316', '#ef4444'], '奇幻': ['#a855f7', '#6366f1'],
    '武侠': ['#ef4444', '#b91c1c'], '仙侠': ['#6366f1', '#4f46e5'],
    '都市': ['#3b82f6', '#1d4ed8'], '科幻': ['#8b5cf6', '#6d28d9'],
    '言情': ['#ec4899', '#db2777'], '悬疑': ['#475569', '#1e293b'],
  }
  return m[genre || ''] || ['#667eea', '#764ba2']
}

onMounted(() => loadProjects())
</script>

<template>
  <div class="novel-layout">
    <!-- 左侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-logo">
        <span class="logo-icon">✏️</span>
        <span v-if="!sidebarCollapsed" class="logo-text">AI 创作</span>
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          {{ sidebarCollapsed ? '»' : '«' }}
        </button>
      </div>

      <nav class="sidebar-menu">
        <div
          v-for="item in menuItems"
          :key="item.id"
          class="menu-item"
          :class="{ active: activeMenu === item.id }"
          @click="activeMenu = item.id"
          :title="item.label"
        >
          <span class="menu-icon">{{ item.icon }}</span>
          <span v-if="!sidebarCollapsed" class="menu-label">{{ item.label }}</span>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="user-avatar">👤</div>
        <div v-if="!sidebarCollapsed" class="user-info">
          <div class="user-name">创作者</div>
          <div class="user-sub">AI 创作平台</div>
        </div>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content-area">
      <header class="page-header">
        <div class="header-left">
          <h1 class="page-title">我的作品</h1>
          <span class="project-count">{{ total }}</span>
        </div>
        <button class="create-btn" @click="showCreateDialog = true">
          <span>+</span> 创建作品
        </button>
      </header>

      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
      </div>

      <div v-else-if="projects.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>还没有任何作品</h3>
        <p>点击「创建作品」开始你的创作之旅</p>
      </div>

      <div v-else class="project-grid">
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card"
          @click="openProject(project.id)"
        >
          <div
            class="card-cover"
            :style="{ background: `linear-gradient(135deg, ${getGenreColors(project.genre)[0]}, ${getGenreColors(project.genre)[1]})` }"
          >
            <span class="cover-title">{{ project.title }}</span>
          </div>
          <div class="card-content">
            <div class="card-header">
              <h3 class="card-title">{{ project.title }}</h3>
              <span :class="['card-status', getStatusClass(project.status)]">
                {{ getStatusText(project.status) }}
              </span>
            </div>
            <p class="card-desc">{{ project.description || '暂无简介' }}</p>
            <div class="card-footer">
              <span class="meta-date">{{ formatDate(project.updated_at) }}</span>
              <button class="delete-btn" @click="handleDeleteProject(project.id, $event)">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 创建弹窗 -->
    <Teleport to="body">
      <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
        <div class="dialog">
          <div class="dialog-header">
            <h2>创建新作品</h2>
            <button class="close-btn" @click="showCreateDialog = false">×</button>
          </div>
          <div class="dialog-body">
            <div class="form-group">
              <label>作品名称 <span class="req">*</span></label>
              <input v-model="newProject.title" type="text" placeholder="请输入作品名称" class="form-input" @keyup.enter="handleCreateProject" />
            </div>
            <div class="form-group">
              <label>作品类型</label>
              <select v-model="newProject.genre" class="form-select">
                <option value="">请选择类型</option>
                <option v-for="g in genreOptions" :key="g" :value="g">{{ g }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>作品简介</label>
              <textarea v-model="newProject.description" placeholder="请输入作品简介（选填）" class="form-textarea" rows="4"></textarea>
            </div>
          </div>
          <div class="dialog-footer">
            <button class="cancel-btn" @click="showCreateDialog = false">取消</button>
            <button class="submit-btn" @click="handleCreateProject" :disabled="!newProject.title.trim()">创建</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.novel-layout {
  display: flex;
  width: calc(100% + 4rem);
  margin-left: -2rem;
  margin-top: -2rem;
  height: calc(100vh - 50px);
  background: #f5f7fa;
  overflow: hidden;
}

/* ===== 侧边栏 ===== */
.sidebar {
  width: 200px;
  background: #1a1f36;
  color: #a0aec0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s ease;
}
.sidebar.collapsed { width: 60px; }

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.logo-icon { font-size: 22px; }
.logo-text { font-size: 16px; font-weight: 700; color: white; white-space: nowrap; }
.collapse-btn {
  margin-left: auto;
  width: 24px; height: 24px;
  border-radius: 6px; border: none;
  background: rgba(255,255,255,0.1);
  color: #a0aec0; font-size: 14px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.collapse-btn:hover { background: rgba(255,255,255,0.2); color: white; }

.sidebar-menu {
  flex: 1; padding: 12px 8px; overflow-y: auto;
}
.menu-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px; border-radius: 8px;
  cursor: pointer; transition: all 0.2s; margin-bottom: 2px;
}
.menu-item:hover { background: rgba(255,255,255,0.08); color: white; }
.menu-item.active { background: rgba(59,130,246,0.2); color: #60a5fa; }
.menu-icon { font-size: 18px; width: 24px; text-align: center; flex-shrink: 0; }
.menu-label { font-size: 14px; white-space: nowrap; }

.sidebar-footer {
  padding: 16px; border-top: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; gap: 12px;
}
.user-avatar {
  width: 36px; height: 36px; border-radius: 8px;
  background: #3b82f6; display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.user-name { font-size: 14px; font-weight: 600; color: white; }
.user-sub { font-size: 12px; color: #718096; }

/* ===== 内容区 ===== */
.content-area {
  flex: 1; display: flex; flex-direction: column;
  overflow: hidden; min-width: 0;
}
.page-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24px 32px; background: white;
  border-bottom: 1px solid #e5e7eb; flex-shrink: 0;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.page-title { font-size: 22px; font-weight: 700; color: #1e293b; margin: 0; }
.project-count {
  font-size: 13px; font-weight: 500; color: #94a3b8;
  background: #f1f5f9; padding: 2px 10px; border-radius: 12px;
}
.create-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 10px 20px; background: #1d4ed8; color: white;
  border: none; border-radius: 8px; font-size: 14px; font-weight: 600;
  cursor: pointer; transition: all 0.2s;
}
.create-btn:hover { background: #1e40af; box-shadow: 0 4px 12px rgba(29,78,216,0.3); }

.loading-state { display: flex; align-items: center; justify-content: center; padding: 120px 0; }
.loading-spinner {
  width: 36px; height: 36px; border: 3px solid #e2e8f0;
  border-top-color: #1d4ed8; border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; padding: 120px 0; }
.empty-icon { font-size: 56px; margin-bottom: 20px; }
.empty-state h3 { font-size: 18px; color: #1e293b; margin: 0 0 8px; }
.empty-state p { font-size: 14px; color: #94a3b8; margin: 0; }

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
  gap: 20px; padding: 24px 32px; overflow-y: auto; align-content: start;
}

.project-card {
  display: flex; flex-direction: row; background: white;
  border-radius: 12px; overflow: hidden; cursor: pointer;
  transition: all 0.25s; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  border: 1px solid #f0f0f0;
}
.project-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); transform: translateY(-2px); }

.card-cover {
  width: 140px; min-height: 160px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  padding: 20px 16px;
}
.cover-title {
  font-size: 18px; font-weight: 700; color: white;
  text-align: center; line-height: 1.5; word-break: break-all;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.card-content { flex: 1; display: flex; flex-direction: column; padding: 20px; min-width: 0; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.card-title {
  font-size: 18px; font-weight: 600; color: #1e293b; margin: 0;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; margin-right: 10px;
}
.card-status { padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; flex-shrink: 0; }
.status-draft { background: #f1f5f9; color: #64748b; }
.status-writing { background: #dbeafe; color: #2563eb; }
.status-completed { background: #dcfce7; color: #16a34a; }

.card-desc {
  font-size: 14px; color: #64748b; line-height: 1.7; margin: 0 0 16px; flex: 1;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}

.card-footer { display: flex; align-items: center; justify-content: space-between; }
.meta-date { font-size: 13px; color: #94a3b8; }
.delete-btn {
  width: 32px; height: 32px; border-radius: 8px; border: none;
  background: transparent; color: #94a3b8; font-size: 16px;
  cursor: pointer; opacity: 0; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center;
}
.project-card:hover .delete-btn { opacity: 1; }
.delete-btn:hover { background: #fef2f2; color: #ef4444; }

/* ===== 弹窗 ===== */
.dialog-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.dialog {
  background: white; border-radius: 16px; width: 100%; max-width: 480px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  animation: dialogIn 0.3s ease;
}
@keyframes dialogIn { from { opacity: 0; transform: scale(0.95); } }
.dialog-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 24px 0; }
.dialog-header h2 { font-size: 20px; font-weight: 600; color: #1e293b; margin: 0; }
.close-btn {
  width: 32px; height: 32px; border-radius: 8px; border: none; background: #f1f5f9;
  cursor: pointer; font-size: 20px; color: #64748b;
  display: flex; align-items: center; justify-content: center;
}
.close-btn:hover { background: #e2e8f0; }
.dialog-body { padding: 24px; }
.form-group { margin-bottom: 20px; }
.form-group:last-child { margin-bottom: 0; }
.form-group label { display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px; }
.req { color: #ef4444; }
.form-input, .form-select, .form-textarea {
  width: 100%; padding: 12px 16px; border: 1px solid #e5e7eb;
  border-radius: 10px; font-size: 15px; color: #1e293b; background: #f9fafb;
  box-sizing: border-box; transition: all 0.2s;
}
.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none; border-color: #1d4ed8; background: white;
  box-shadow: 0 0 0 3px rgba(29,78,216,0.1);
}
.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 12px center; background-repeat: no-repeat;
  background-size: 20px; padding-right: 40px;
}
.form-textarea { resize: vertical; min-height: 100px; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 0 24px 24px; }
.cancel-btn {
  padding: 12px 24px; border: 1px solid #e5e7eb; border-radius: 10px;
  background: white; color: #374151; font-size: 15px; cursor: pointer;
}
.cancel-btn:hover { background: #f9fafb; }
.submit-btn {
  padding: 12px 24px; border: none; border-radius: 10px;
  background: #1d4ed8; color: white; font-size: 15px; font-weight: 600; cursor: pointer;
}
.submit-btn:hover:not(:disabled) { background: #1e40af; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
