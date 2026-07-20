<script setup lang="ts">
/**
 * DiscussView.vue - 思路交流页面
 * 创作者交流社区
 */
import { ref } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'

const posts = ref([
  { id: 1, title: '如何写出有张力的开场？', author: '笔下生花', time: '2小时前', replies: 12, tags: ['技巧', '讨论'] },
  { id: 2, title: '玄幻小说的世界观搭建心得', author: '星辰作者', time: '5小时前', replies: 28, tags: ['玄幻', '经验'] },
  { id: 3, title: '人物对话如何避免"水对话"？', author: '笔墨纵横', time: '1天前', replies: 8, tags: ['技巧', '对话'] },
  { id: 4, title: '求推荐好用的灵感收集方法', author: '灵感收集者', time: '2天前', replies: 15, tags: ['工具', '灵感'] },
])

const tagColors: Record<string, string> = { '技巧': '#3b82f6', '讨论': '#8b5cf6', '玄幻': '#ef4444', '经验': '#10b981', '对话': '#f59e0b', '工具': '#ec4899', '灵感': '#06b6d4' }
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <h1 class="page-title">思路交流</h1>
      </header>
      <div class="tool-container">
        <div class="post-list">
          <div v-for="post in posts" :key="post.id" class="post-card">
            <div class="post-main">
              <h3>{{ post.title }}</h3>
              <div class="post-meta">
                <span class="post-author">{{ post.author }}</span>
                <span class="post-time">{{ post.time }}</span>
                <div class="post-tags">
                  <span v-for="t in post.tags" :key="t" class="tag" :style="{ background: (tagColors[t] || '#64748b') + '18', color: tagColors[t] || '#64748b' }">{{ t }}</span>
                </div>
              </div>
            </div>
            <div class="post-replies">
              <span class="reply-icon">💬</span>
              <span>{{ post.replies }}</span>
            </div>
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
.post-list { display: flex; flex-direction: column; gap: 12px; }
.post-card { display: flex; align-items: center; justify-content: space-between; background: white; border-radius: 12px; padding: 20px 24px; border: 1px solid #f0f0f0; cursor: pointer; transition: all 0.2s; }
.post-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.post-main h3 { font-size: 16px; font-weight: 600; color: #1e293b; margin: 0 0 8px; }
.post-meta { display: flex; align-items: center; gap: 12px; font-size: 13px; color: #94a3b8; }
.post-author { font-weight: 500; color: #64748b; }
.post-tags { display: flex; gap: 6px; }
.tag { padding: 2px 8px; border-radius: 8px; font-size: 12px; font-weight: 500; }
.post-replies { display: flex; align-items: center; gap: 4px; color: #64748b; font-size: 14px; }
.reply-icon { font-size: 16px; }
</style>
