<script setup lang="ts">
/**
 * GuideView.vue - 使用指南页面
 */
import AppSidebar from '../components/AppSidebar.vue'

const guides = [
  { icon: '🚀', title: '快速开始', desc: '如何创建你的第一部作品', items: ['点击「创建作品」按钮', '填写作品名称和类型', '点击进入编辑页面'] },
  { icon: '✍️', title: '章节编辑', desc: '高效地编辑你的章节内容', items: ['左侧添加/管理章节', '中间区域编写内容', '支持 Ctrl+S 快速保存'] },
  { icon: '🤖', title: 'AI 助手', desc: '使用 AI 辅助创作', items: ['右侧打开 AI 对话', 'AI 会自动获取当前章节上下文', '可以请求续写、润色等帮助'] },
  { icon: '📋', title: '词条管理', desc: '管理作品中的设定和术语', items: ['创建人物、世界观等词条', '分类管理便于查找', '创作时随时参考'] },
]
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header"><h1 class="page-title">使用指南</h1></header>
      <div class="tool-container">
        <div class="guide-grid">
          <div v-for="g in guides" :key="g.title" class="guide-card">
            <div class="guide-icon">{{ g.icon }}</div>
            <h3>{{ g.title }}</h3>
            <p>{{ g.desc }}</p>
            <ul>
              <li v-for="(item, i) in g.items" :key="i">{{ item }}</li>
            </ul>
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
.guide-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.guide-card { background: white; border-radius: 12px; padding: 24px; border: 1px solid #f0f0f0; }
.guide-icon { font-size: 36px; margin-bottom: 16px; }
.guide-card h3 { font-size: 17px; font-weight: 600; color: #1e293b; margin: 0 0 6px; }
.guide-card p { font-size: 14px; color: #64748b; margin: 0 0 16px; }
.guide-card ul { padding-left: 20px; margin: 0; }
.guide-card li { font-size: 14px; color: #475569; line-height: 1.8; }
</style>
