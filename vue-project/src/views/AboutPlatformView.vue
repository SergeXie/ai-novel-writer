<script setup lang="ts">
/**
 * AboutView.vue - 关于平台页面
 */
import AppSidebar from '../components/AppSidebar.vue'
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header"><h1 class="page-title">关于平台</h1></header>
      <div class="tool-container">
        <div class="about-card">
          <div class="about-logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div>
          <h1>AI 小说创作平台</h1>
          <p class="version">v1.0.0</p>
          <div class="about-desc">
            <p>AI 小说创作平台是一个智能辅助写作工具，帮助创作者高效地构思、撰写和管理小说作品。</p>
            <p>通过 AI 技术，我们提供章节生成、内容润色、结构分析等功能，让创作变得更加轻松。</p>
          </div>
          <div class="features">
            <div class="feature"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></span><span>作品管理</span></div>
            <div class="feature"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg></span><span>AI 辅助创作</span></div>
            <div class="feature"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg></span><span>词条管理</span></div>
            <div class="feature"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span><span>智能拆书</span></div>
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
.tool-container { flex: 1; padding: 32px; display: flex; align-items: flex-start; justify-content: center; }
.about-card { background: white; border-radius: 16px; padding: 48px; text-align: center; max-width: 520px; width: 100%; border: 1px solid #f0f0f0; }
.about-logo { font-size: 56px; margin-bottom: 20px; }
.about-card h1 { font-size: 24px; font-weight: 700; color: #1e293b; margin: 0 0 8px; }
.version { font-size: 14px; color: #94a3b8; margin: 0 0 24px; }
.about-desc p { font-size: 15px; color: #64748b; line-height: 1.7; margin: 0 0 12px; }
.features { display: flex; gap: 20px; justify-content: center; margin-top: 32px; flex-wrap: wrap; }
.feature { display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f8fafc; border-radius: 8px; font-size: 14px; color: #475569; }
</style>
