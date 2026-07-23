<script setup lang="ts">
/**
 * SplitBookView.vue - 智能拆书页面
 * 分析小说结构，拆分章节
 */
import { ref } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'

const inputText = ref('')
const result = ref('')
const loading = ref(false)

const analyze = async () => {
  if (!inputText.value.trim()) return
  loading.value = true
  result.value = '正在分析中，请稍候...'
  // 模拟分析
  setTimeout(() => {
    result.value = `分析结果：\n\n这段文本共 ${inputText.value.length} 个字符，包含 ${inputText.value.split(/[。！？]/).filter(s => s.trim()).length} 个句子。\n\n建议可以将文本拆分为 ${Math.ceil(inputText.value.length / 2000)} 个章节。`
    loading.value = false
  }, 1500)
}
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <h1 class="page-title">智能拆书</h1>
      </header>
      <div class="tool-container">
        <div class="input-section">
          <h3>粘贴文本内容</h3>
          <textarea v-model="inputText" class="big-textarea" placeholder="将你的小说文本粘贴到这里，AI 将帮你分析结构并智能拆分章节..." rows="12"></textarea>
          <button class="action-btn" @click="analyze" :disabled="!inputText.trim() || loading">
            {{ loading ? '分析中...' : '开始分析' }}
          </button>
        </div>
        <div v-if="result" class="result-section">
          <h3>分析结果</h3>
          <div class="result-box">{{ result }}</div>
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
.input-section { margin-bottom: 24px; }
.input-section h3, .result-section h3 { font-size: 16px; font-weight: 600; color: #1e293b; margin: 0 0 12px; }
.big-textarea { width: 100%; padding: 16px; border: 1px solid #e5e7eb; border-radius: 12px; font-size: 15px; line-height: 1.7; color: #1e293b; background: white; resize: vertical; box-sizing: border-box; font-family: inherit; }
.big-textarea:focus { outline: none; border-color: #1d4ed8; box-shadow: 0 0 0 3px rgba(29,78,216,0.1); }
.action-btn { margin-top: 12px; padding: 12px 24px; background: #1d4ed8; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; }
.action-btn:hover:not(:disabled) { background: #1e40af; }
.action-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.result-box { background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; font-size: 15px; line-height: 1.8; color: #1e293b; white-space: pre-wrap; }
</style>
