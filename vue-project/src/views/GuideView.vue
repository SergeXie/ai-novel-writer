<script setup lang="ts">
/**
 * GuideView.vue - 使用指南页面
 */
import AppSidebar from '../components/AppSidebar.vue'

const guides = [
  { icon: 'rocket', title: '快速开始', desc: '如何创建你的第一部作品', items: ['点击「创建作品」按钮', '填写作品名称和类型', '点击进入编辑页面'] },
  { icon: 'edit', title: '章节编辑', desc: '高效地编辑你的章节内容', items: ['左侧添加/管理章节', '中间区域编写内容', '支持 Ctrl+S 快速保存'] },
  { icon: 'bot', title: 'AI 助手', desc: '使用 AI 辅助创作', items: ['右侧打开 AI 对话', 'AI 会自动获取当前章节上下文', '可以请求续写、润色等帮助'] },
  { icon: 'clipboard', title: '词条管理', desc: '管理作品中的设定和术语', items: ['创建人物、世界观等词条', '分类管理便于查找', '创作时随时参考'] },
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
            <div class="guide-icon">
              <svg v-if="g.icon === 'rocket'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
              <svg v-else-if="g.icon === 'edit'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              <svg v-else-if="g.icon === 'bot'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
            </div>
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
