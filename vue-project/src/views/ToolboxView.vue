<script setup lang="ts">
/**
 * ToolboxView.vue - 工具箱页面
 * 提供各种写作辅助工具
 */
import AppSidebar from '../components/AppSidebar.vue'

const tools = [
  { icon: 'chart', name: '字数统计', desc: '统计文本字数、句数、段落数', color: '#3b82f6' },
  { icon: 'refresh', name: '同义词替换', desc: '智能替换重复用词', color: '#8b5cf6' },
  { icon: 'pen', name: '错别字检测', desc: '检查文本中的错别字', color: '#ef4444' },
  { icon: 'mask', name: '角色名生成', desc: '生成各类角色名字', color: '#f59e0b' },
  { icon: 'globe', name: '世界观模板', desc: '世界观设定参考模板', color: '#10b981' },
  { icon: 'message', name: '对话润色', desc: '优化对话表达', color: '#ec4899' },
]
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <h1 class="page-title">工具箱</h1>
      </header>
      <div class="tool-container">
        <div class="tool-grid">
          <div v-for="tool in tools" :key="tool.name" class="tool-card">
            <div class="tool-icon" :style="{ background: tool.color + '15', color: tool.color }">{{ tool.icon }}</div>
            <div class="tool-info">
              <h3>{{ tool.name }}</h3>
              <p>{{ tool.desc }}</p>
            </div>
            <button class="tool-btn" :style="{ color: tool.color }">使用 →</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-layout { display: flex; width: calc(100% + 4rem); margin-left: -2rem; margin-top: -2rem; height: calc(100vh - 50px); background: #f5f7fa; overflow: hidden; }
.content-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
.page-header { display: flex; align-items: center; padding: 24px 32px; background: white; border-bottom: 1px solid #e5e7eb; flex-shrink: 0; }
.page-title { font-size: 22px; font-weight: 700; color: #1e293b; margin: 0; }
.tool-container { flex: 1; padding: 32px; overflow-y: auto; }
.tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; }
.tool-card { display: flex; align-items: center; gap: 16px; background: white; border-radius: 12px; padding: 20px; border: 1px solid #f0f0f0; cursor: pointer; transition: all 0.2s; }
.tool-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); transform: translateY(-1px); }
.tool-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
.tool-info { flex: 1; min-width: 0; }
.tool-info h3 { font-size: 15px; font-weight: 600; color: #1e293b; margin: 0 0 4px; }
.tool-info p { font-size: 13px; color: #94a3b8; margin: 0; }
.tool-btn { border: none; background: none; font-size: 14px; font-weight: 600; cursor: pointer; white-space: nowrap; }
</style>
