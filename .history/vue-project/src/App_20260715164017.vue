<script setup lang="ts">
/**
 * App.vue - 应用根组件
 * 包含导航栏和路由视图
 */
</script>

<template>
  <!-- 导航栏 -->
  <nav class="navbar">
    <div class="nav-brand">
      <img alt="Logo" class="logo" src="./assets/logo.svg" width="40" height="40" />
      <span class="brand-text">AI 小说创作平台</span>
    </div>
    
    <div class="nav-links">
      <router-link to="/" class="nav-link">🏠 首页</router-link>
      <router-link to="/about" class="nav-link">📖 Vue 基础</router-link>
      <router-link to="/counter" class="nav-link">🔢 计数器</router-link>
      <router-link to="/todo" class="nav-link">📝 待办事项</router-link>
      <router-link to="/novel" class="nav-link">✍️ AI 小说</router-link>
    </div>
  </nav>

  <!-- 路由视图 -->
  <main class="main-content">
    <router-view />
  </main>

  <!-- 页脚 -->
  <footer class="footer">
    <p>✨ AI 小说创作平台 | 让创意成为故事</p>
  </footer>
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
