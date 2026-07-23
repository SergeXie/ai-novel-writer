<script setup lang="ts">
/**
 * 首页 - 欢迎页面
 * 展示 Vue 项目的基本信息和导航链接
 */
import { useRouter } from 'vue-router'

const router = useRouter()

// 示例：编程式导航 - 通过代码跳转页面
function goToAbout() {
  router.push({ name: 'about' })
}
</script>

<template>
  <div class="home">
    <h1>欢迎来到 Vue 学习项目！</h1>
    
    <div class="intro">
      <p>这是一个帮助你学习 Vue 3 的示例项目，包含了以下核心概念：</p>
      
      <div class="feature-grid">
        <div class="feature-card" @click="goToAbout">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" style="vertical-align: -3px"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> Vue 3 基础</h3>
          <p>组件、模板语法、响应式数据</p>
        </div>
        
        <div class="feature-card" @click="router.push({ name: 'novel-list' })">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" style="vertical-align: -3px"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg> AI 小说</h3>
          <p>AI 辅助创作、章节管理、智能拆书</p>
        </div>
      </div>
    </div>

    <div class="quick-start">
      <h2>快速开始</h2>
      <ol>
        <li>点击上方卡片探索不同功能</li>
        <li>查看各页面的代码注释</li>
        <li>尝试修改代码并观察变化</li>
      </ol>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #42b883;
  text-align: center;
  margin-bottom: 2rem;
}

.intro {
  margin-bottom: 2rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.feature-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #42b883;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(66, 184, 131, 0.2);
}

.feature-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.feature-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.quick-start {
  background: #f0f9ff;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #42b883;
}

.quick-start h2 {
  margin-top: 0;
  color: #333;
}

.quick-start ol {
  margin: 0;
  padding-left: 1.2rem;
}

.quick-start li {
  margin: 0.5rem 0;
  color: #555;
}
</style>
