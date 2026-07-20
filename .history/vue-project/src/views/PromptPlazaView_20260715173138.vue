<script setup lang="ts">
/**
 * PromptPlazaView.vue - 提示词广场
 * 提供各种写作相关的 AI 提示词模板
 */
import { ref } from 'vue'
import AppSidebar from '../components/AppSidebar.vue'

// 提示词分类
const activeCategory = ref('all')

const categories = [
  { id: 'all', label: '全部', icon: '📋' },
  { id: 'character', label: '角色塑造', icon: '👤' },
  { id: 'plot', label: '情节构思', icon: '📖' },
  { id: 'world', label: '世界观', icon: '🌍' },
  { id: 'dialogue', label: '对话润色', icon: '💬' },
  { id: 'rewrite', label: '改写优化', icon: '✏️' },
  { id: 'outline', label: '大纲生成', icon: '📝' },
]

// 提示词数据
const prompts = ref([
  {
    id: 1,
    title: '角色背景故事生成',
    description: '根据角色名称和基本设定，生成详细的角色背景故事',
    category: 'character',
    prompt: '请为以下角色生成详细的背景故事：\n\n角色名称：[名称]\n性格特点：[特点]\n身份背景：[背景]\n\n要求：\n1. 包含童年经历\n2. 重要人生转折\n3. 形成当前性格的原因',
    usageCount: 1256,
    likes: 89,
  },
  {
    id: 2,
    title: '反派角色塑造',
    description: '创建有深度、有动机的反派角色',
    category: 'character',
    prompt: '请帮我塑造一个有深度的反派角色：\n\n基本信息：[年龄、身份]\n表面动机：[动机]\n\n请分析：\n1. 他的真实目的是什么\n2. 为什么会走上反派道路\n3. 他的弱点和人性的一面',
    usageCount: 843,
    likes: 67,
  },
  {
    id: 3,
    title: '情节转折点设计',
    description: '为故事设计出人意料的转折',
    category: 'plot',
    prompt: '当前故事梗概：[简述]\n\n请设计3个可能的情节转折点：\n1. 小转折（改变角色关系）\n2. 中转折（改变故事方向）\n3. 大转折（颠覆读者认知）\n\n每个转折要合理且有伏笔空间。',
    usageCount: 1089,
    likes: 102,
  },
  {
    id: 4,
    title: '世界观设定模板',
    description: '快速构建完整的世界观体系',
    category: 'world',
    prompt: '请帮我构建一个[类型]世界观：\n\n基础设定：[关键词]\n\n请包含：\n1. 世界的基本规则\n2. 力量体系/科技水平\n3. 社会结构\n4. 主要势力\n5. 历史大事件\n6. 独特的文化元素',
    usageCount: 756,
    likes: 78,
  },
  {
    id: 5,
    title: '对话风格转换',
    description: '让角色对话更符合其性格',
    category: 'dialogue',
    prompt: '请将以下对话改写，使其更符合角色性格：\n\n角色性格：[性格描述]\n当前对话：\n[粘贴对话]\n\n要求：\n1. 保持原意\n2. 加入符合性格的语气词\n3. 调整句式结构',
    usageCount: 623,
    likes: 45,
  },
  {
    id: 6,
    title: '场景氛围渲染',
    description: '通过环境描写增强场景氛围',
    category: 'rewrite',
    prompt: '请为以下场景增加氛围渲染描写：\n\n场景：[场景描述]\n情绪基调：[紧张/温馨/悲伤等]\n\n要求：\n1. 使用五感描写\n2. 与角色情绪呼应\n3. 不超过200字',
    usageCount: 534,
    likes: 52,
  },
  {
    id: 7,
    title: '小说大纲生成',
    description: '根据主题快速生成完整大纲',
    category: 'outline',
    prompt: '请为我生成一部[类型]小说的大纲：\n\n主题：[主题]\n字数目标：[万字]\n核心冲突：[冲突]\n\n请包含：\n1. 三幕结构\n2. 主要情节点\n3. 角色成长线\n4. 高潮设计\n5. 结局走向',
    usageCount: 1567,
    likes: 134,
  },
  {
    id: 8,
    title: '战斗场景描写',
    description: '写出紧张刺激的战斗场面',
    category: 'rewrite',
    prompt: '请帮我描写一场战斗/冲突场景：\n\n参战方：[角色/势力]\n场景环境：[环境]\n力量对比：[强弱关系]\n\n要求：\n1. 动作描写有画面感\n2. 节奏张弛有度\n3. 融入角色情感',
    usageCount: 445,
    likes: 38,
  },
])

// 筛选提示词
const filteredPrompts = ref(prompts.value)

const filterPrompts = (cat: string) => {
  activeCategory.value = cat
  filteredPrompts.value = cat === 'all'
    ? prompts.value
    : prompts.value.filter(p => p.category === cat)
}

// 复制提示词
const copiedId = ref<number | null>(null)
const copyPrompt = (prompt: string, id: number) => {
  navigator.clipboard.writeText(prompt)
  copiedId.value = id
  setTimeout(() => copiedId.value = null, 2000)
}

// 使用提示词（模拟）
const showUseDialog = ref(false)
const selectedPrompt = ref<typeof prompts.value[0] | null>(null)
const userInput = ref('')

const openUseDialog = (p: typeof prompts.value[0]) => {
  selectedPrompt.value = p
  showUseDialog.value = true
  userInput.value = p.prompt
}

const copyToClipboard = () => {
  navigator.clipboard.writeText(userInput.value)
}
</script>

<template>
  <div class="page-layout">
    <AppSidebar />
    <main class="content-area">
      <header class="page-header">
        <div class="header-left">
          <h1 class="page-title">✨ 提示词广场</h1>
        </div>
      </header>

      <div class="prompt-container">
        <!-- 分类标签 -->
        <div class="category-bar">
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="cat-btn"
            :class="{ active: activeCategory === cat.id }"
            @click="filterPrompts(cat.id)"
          >
            <span>{{ cat.icon }}</span>
            <span>{{ cat.label }}</span>
          </button>
        </div>

        <!-- 提示词网格 -->
        <div class="prompt-grid">
          <div v-for="prompt in filteredPrompts" :key="prompt.id" class="prompt-card">
            <div class="card-header">
              <h3>{{ prompt.title }}</h3>
              <span class="cat-tag">{{ categories.find(c => c.id === prompt.category)?.label }}</span>
            </div>
            <p class="card-desc">{{ prompt.description }}</p>
            <div class="card-preview">
              {{ prompt.prompt.substring(0, 100) }}...
            </div>
            <div class="card-footer">
              <div class="card-stats">
                <span>👁️ {{ prompt.usageCount }}</span>
                <span>❤️ {{ prompt.likes }}</span>
              </div>
              <div class="card-actions">
                <button
                  class="copy-btn"
                  @click.stop="copyPrompt(prompt.prompt, prompt.id)"
                  :class="{ copied: copiedId === prompt.id }"
                >
                  {{ copiedId === prompt.id ? '✓ 已复制' : '📋 复制' }}
                </button>
                <button class="use-btn" @click="openUseDialog(prompt)">使用</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用弹窗 -->
      <Teleport to="body">
        <div v-if="showUseDialog" class="dialog-overlay" @click.self="showUseDialog = false">
          <div class="dialog dialog-large">
            <div class="dialog-header">
              <h2>{{ selectedPrompt?.title }}</h2>
              <button class="close-btn" @click="showUseDialog = false">×</button>
            </div>
            <div class="dialog-body">
              <p class="dialog-desc">{{ selectedPrompt?.description }}</p>
              <label class="dialog-label">提示词内容（可编辑后复制）</label>
              <textarea v-model="userInput" class="prompt-textarea" rows="12"></textarea>
              <p class="dialog-hint">💡 修改 [方括号] 中的内容为你的具体内容，然后复制使用</p>
            </div>
            <div class="dialog-footer">
              <button class="cancel-btn" @click="showUseDialog = false">关闭</button>
              <button class="copy-btn-lg" @click="copyToClipboard">📋 复制提示词</button>
            </div>
          </div>
        </div>
      </Teleport>
    </main>
  </div>
</template>

<style scoped>
.page-layout {
  display: flex;
  width: calc(100% + 4rem);
  margin-left: -2rem;
  margin-top: -2rem;
  height: calc(100vh - 50px);
  background: #f5f7fa;
  overflow: hidden;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

.page-header {
  display: flex;
  align-items: center;
  padding: 24px 32px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

/* 分类标签栏 */
.category-bar {
  display: flex;
  gap: 8px;
  padding: 20px 32px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  overflow-x: auto;
  flex-shrink: 0;
}

.cat-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: #1d4ed8;
  color: #1d4ed8;
}

.cat-btn.active {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: white;
}

/* 提示词网格 */
.prompt-container {
  flex: 1;
  overflow-y: auto;
}

.prompt-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  padding: 24px 32px;
  align-content: start;
}

/* 提示词卡片 */
.prompt-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  overflow: hidden;
  transition: all 0.25s;
  cursor: pointer;
}

.prompt-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 20px 0;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
}

.cat-tag {
  padding: 3px 10px;
  background: #f1f5f9;
  color: #64748b;
  border-radius: 12px;
  font-size: 12px;
  flex-shrink: 0;
}

.card-desc {
  padding: 8px 20px 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

.card-preview {
  margin: 12px 20px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 13px;
  color: #475569;
  line-height: 1.6;
  white-space: pre-line;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-top: 1px solid #f5f5f5;
}

.card-stats {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #94a3b8;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.copy-btn {
  padding: 6px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #475569;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  border-color: #1d4ed8;
  color: #1d4ed8;
}

.copy-btn.copied {
  background: #dcfce7;
  border-color: #22c55e;
  color: #16a34a;
}

.use-btn {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  background: #1d4ed8;
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.use-btn:hover {
  background: #1e40af;
}

/* 弹窗 */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  font-size: 20px;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #e2e8f0;
}

.dialog-body {
  padding: 20px 24px;
  overflow-y: auto;
  flex: 1;
}

.dialog-desc {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 16px;
}

.dialog-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.prompt-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.7;
  color: #1e293b;
  background: #f9fafb;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
}

.prompt-textarea:focus {
  outline: none;
  border-color: #1d4ed8;
  background: white;
}

.dialog-hint {
  font-size: 13px;
  color: #94a3b8;
  margin: 12px 0 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

.cancel-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}

.copy-btn-lg {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #1d4ed8;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn-lg:hover {
  background: #1e40af;
}
</style>
