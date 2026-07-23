<script setup lang="ts">
/**
 * AppSidebar.vue - 全局侧边栏组件
 * 浅色主题，支持折叠
 */
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 侧边栏折叠状态
const collapsed = ref(false)

// 当前选中菜单
const activeMenu = ref(route.path)

// 菜单列表
const menuItems = [
  { id: '/novel', icon: 'folder', label: '我的作品' },
  { id: '/snippets', icon: 'clipboard', label: '我的词条' },
  { id: '/split', icon: 'book', label: '智能拆书' },
  { id: '/prompts', icon: 'sparkles', label: '提示词广场' },
  { id: '/discuss', icon: 'message', label: 'AI 对话' },
  { id: '/guide', icon: 'book-open', label: '使用指南' },
  { id: '/about', icon: 'info', label: '关于平台' },
]

const navigateTo = (path: string) => {
  activeMenu.value = path
  router.push(path)
}

// 判断菜单是否激活（支持子路由）
const isActive = (itemPath: string) => {
  if (itemPath === '/novel') {
    return route.path === '/novel' || route.path.startsWith('/novel/')
  }
  return activeMenu.value === itemPath
}
</script>

<template>
  <aside class="sidebar" :class="{ collapsed }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <span class="logo-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></span>
      <span v-if="!collapsed" class="logo-text">AI 创作</span>
      <button class="collapse-btn" @click="collapsed = !collapsed" :title="collapsed ? '展开' : '收起'">
        {{ collapsed ? '»' : '«' }}
      </button>
    </div>

    <!-- 菜单 -->
    <nav class="sidebar-menu">
      <div
        v-for="item in menuItems"
        :key="item.id"
        class="menu-item"
        :class="{ active: isActive(item.id) }"
        @click="navigateTo(item.id)"
        :title="item.label"
      >
        <span class="menu-icon">
          <svg v-if="item.icon === 'folder'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          <svg v-else-if="item.icon === 'clipboard'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
          <svg v-else-if="item.icon === 'book'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          <svg v-else-if="item.icon === 'sparkles'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>
          <svg v-else-if="item.icon === 'message'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/></svg>
          <svg v-else-if="item.icon === 'book-open'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        </span>
        <span v-if="!collapsed" class="menu-label">{{ item.label }}</span>
      </div>
    </nav>

    <!-- 底部 -->
    <div class="sidebar-footer">
      <div class="user-avatar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
      <div v-if="!collapsed" class="user-info">
        <div class="user-name">创作者</div>
        <div class="user-sub">AI 创作平台</div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s ease;
  user-select: none;
}

.sidebar.collapsed {
  width: 60px;
}

/* Logo */
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.logo-icon {
  font-size: 22px;
  flex-shrink: 0;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
}

.collapse-btn {
  margin-left: auto;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: #f8fafc;
  color: #64748b;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #1e293b;
}

/* 菜单 */
.sidebar-menu {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 2px;
  color: #475569;
}

.menu-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.menu-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 500;
}

.menu-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.menu-label {
  font-size: 14px;
  white-space: nowrap;
}

/* 底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #eff6ff;
  border: 1px solid #dbeafe;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.user-sub {
  font-size: 12px;
  color: #94a3b8;
}
</style>
