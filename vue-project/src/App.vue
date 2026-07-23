<script setup lang="ts">
/**
 * App.vue - 应用根组件
 * 包含导航栏和路由视图
 */
import { onMounted } from 'vue'
import { useApiConfig } from './stores/apiConfig'
import ApiSettingsModal from './components/ApiSettingsModal.vue'

const { showSettings, loadConfigs } = useApiConfig()

// 应用启动时加载 API 配置
onMounted(() => {
  loadConfigs()
})
</script>

<template>
  <!-- 导航栏 -->
  <nav class="navbar">
    <div class="nav-brand">
      <img alt="Logo" class="logo" src="./assets/logo.svg" width="40" height="40" />
      <span class="brand-text">AI 小说创作平台</span>
    </div>
    
    <div class="nav-right">
      <div class="nav-links">
        <router-link to="/about" class="nav-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg> 关于平台</router-link>
        <router-link to="/novel" class="nav-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg> AI 小说</router-link>
      </div>
      <button class="nav-settings-btn" @click="showSettings = true" title="API 设置">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> <span class="settings-text">API 设置</span>
      </button>
    </div>
  </nav>

  <!-- 路由视图 -->
  <main class="main-content">
    <router-view />
  </main>

  <!-- 页脚 -->
  <footer class="footer">
    <p><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14" style="vertical-align: -2px"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> AI 小说创作平台 | 让创意成为故事</p>
  </footer>

  <!-- 全局 API 设置弹窗 -->
  <ApiSettingsModal />
</template>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* 导航栏样式 */
.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo {
  transition: transform 0.3s;
}

.logo:hover {
  transform: rotate(10deg);
}

.brand-text {
  font-size: 1.2rem;
  font-weight: bold;
  color: #42b883;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-settings-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0.45rem 0.9rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  color: #64748b;
  transition: all 0.15s;
  white-space: nowrap;
}

.nav-settings-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #334155;
}

.settings-text {
  font-weight: 500;
}

.nav-link {
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #666;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f0f9ff;
  color: #42b883;
}

/* 当前激活的导航链接 */
.nav-link.router-link-active {
  background: #42b883;
  color: white;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* 页脚样式 */
.footer {
  background: #333;
  color: #aaa;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.footer p {
  margin: 0;
}
</style>
