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
  { id: '/novel', icon: '📁', label: '我的作品' },
  { id: '/snippets', icon: '📋', label: '我的词条' },
  { id: '/split', icon: '📖', label: '智能拆书' },
  { id: '/toolbox', icon: '🧰', label: '工具箱' },
  { id: '/discuss', icon: '💬', label: '思路交流' },
  { id: '/guide', icon: '📘', label: '使用指南' },
  { id: '/about', icon: 'ℹ️', label: '关于平台' },
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
      <span class="logo-icon">✏️</span>
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
        :class="{ active: activeMenu === item.id }"
        @click="navigateTo(item.id)"
        :title="item.label"
      >
        <span class="menu-icon">{{ item.icon }}</span>
        <span v-if="!collapsed" class="menu-label">{{ item.label }}</span>
      </div>
    </nav>

    <!-- 底部 -->
    <div class="sidebar-footer">
      <div class="user-avatar">👤</div>
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
