<script setup lang="ts">
/**
 * 关于页面 - AI 小说创作平台介绍
 * 参考「成章 - Verse」多智能体小说写作系统
 */
import { ref } from 'vue'

// FAQ 折叠状态
const openFaq = ref<number | null>(null)

function toggleFaq(index: number) {
  openFaq.value = openFaq.value === index ? null : index
}

// 核心功能列表
const features = [
  {
    icon: 'building',
    title: '世界观构建',
    desc: '只需一句描述，AI 架构大师即刻展开对话，帮你推演世界观法则、生成角色卡，再自动规划分卷分章大纲——整个创作骨架从无到有，不到三分钟。',
    highlights: ['对话式引导世界观构建', '一键生成角色档案', '大纲规划至章节级别']
  },
  {
    icon: 'book',
    title: '知识库管理',
    desc: '上传你的设定手册、已完成章节和参考文档，通过向量检索让 AI 在每次生成时精准"唤醒"相关记忆——角色弱点、伏笔位置、势力关系，全不遗漏。',
    highlights: ['@角色名即时检索', '杜绝前后矛盾', '知识库实时同步']
  },
  {
    icon: 'sparkles',
    title: '提示词广场',
    desc: '数千位作者共同打造的提示词配方库，涵盖润色、续写、细纲、风格迁移等 8 大分类。找到最钟意的配方，一键应用到写作会话。',
    highlights: ['8 大分类全覆盖', '社区点赞排序', '一键收藏应用']
  },
  {
    icon: 'lightbulb',
    title: '灵感助手',
    desc: '常驻写作界面右侧，无需切换页面。遇到任何卡关——情节无法推进、情绪写不到位，直接开口聊，它会给出有依据的具体建议。',
    highlights: ['结合当前章节内容', '多角度给方案', '零切换成本']
  },
  {
    icon: 'pen',
    title: '沉浸式精修',
    desc: '极简无干扰的写作画布，配合 AI 精修建议同屏并列呈现。删除的是红色，新增的是绿色，看完再决定采不采纳——这是你的作品，AI 只是你的顾问。',
    highlights: ['Diff 式双栏对照', '保留原文主导权', '语义级深度润色']
  }
]

// 创作流程
const workflow = [
  { step: '01', title: '捕捉灵光', desc: '随手记录闪现的念头，由 AI 协助梳理为结构化档案。', icon: 'zap' },
  { step: '02', title: '立骨定型', desc: '一键生成缜密的大纲架构，起承转合由您全局掌控。', icon: 'layers' },
  { step: '03', title: '落笔成文', desc: '沉浸式书写体验，AI 实时辅助，告别断文尴尬。', icon: 'edit' },
  { step: '04', title: '研磨质感', desc: '多角色深度校验与润色，赋予作品出版级的文学底色。', icon: 'gem' }
]

// 常见问题
const faqs = [
  {
    q: '我的创作数据安全吗？',
    a: '作品就是作家的生命。我们实行严苛的私密性保护，作品数据全链路加密，绝对不会被用于任何公开模型的训练。您的每一行字，仅属于您自己。'
  },
  {
    q: '作品版权归属如何界定？',
    a: '绝对归属作者。无论是您的原始脑洞，还是 AI 协助扩写的章节，其完整的版权、商业收益及衍生开发权利均由您本人全资享有，受法律严格保护。'
  },
  {
    q: '支持哪些 AI 模型？',
    a: '平台集成多种主流大模型，包括高阶推理模型、高阶润色模型、高阶创作模型和低倍率快写模型，根据不同创作场景智能匹配最合适的模型。'
  },
  {
    q: '如何开启免费创作之旅？',
    a: '新用户注册后即刻获赠启航额度。您可以零成本创建第一本作品，亲身感受 AI 辅助搭建逻辑架构的魅力。'
  }
]
</script>

<template>
  <div class="about-page">
    <!-- Hero 区域 -->
    <section class="hero">
      <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22" style="vertical-align: -4px"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg> AI 小说创作平台</h1>
      <p class="hero-subtitle">落笔成章，妙手偶得</p>
      <p class="hero-desc">不止于润饰字句，更陪您梳理灵感、打磨叙事。让每一个构想，都更从容地落成篇章。</p>
    </section>

    <!-- 核心功能 -->
    <section class="section">
      <h2 class="section-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="vertical-align: -3px"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg> 核心功能</h2>
      <div class="features-grid">
        <div v-for="feature in features" :key="feature.title" class="feature-card">
          <div class="feature-icon">
              <svg v-if="feature.icon === 'building'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><line x1="8" y1="6" x2="12" y2="6"/><line x1="14" y1="6" x2="12" y2="6"/><line x1="8" y1="10" x2="12" y2="10"/><line x1="14" y1="10" x2="12" y2="10"/><line x1="8" y1="14" x2="12" y2="14"/><line x1="14" y1="14" x2="12" y2="14"/></svg>
              <svg v-else-if="feature.icon === 'book'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
              <svg v-else-if="feature.icon === 'sparkles'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              <svg v-else-if="feature.icon === 'lightbulb'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </div>
          <h3>{{ feature.title }}</h3>
          <p class="feature-desc">{{ feature.desc }}</p>
          <ul class="feature-highlights">
            <li v-for="h in feature.highlights" :key="h">{{ h }}</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 创作流程 -->
    <section class="section">
      <h2 class="section-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="vertical-align: -3px"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg> 创作流程</h2>
      <p class="section-subtitle">从火花到成卷的全程陪伴</p>
      <div class="workflow">
        <div v-for="item in workflow" :key="item.step" class="workflow-item">
          <div class="workflow-step">{{ item.step }}</div>
          <div class="workflow-icon">
              <svg v-if="item.icon === 'zap'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              <svg v-else-if="item.icon === 'layers'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
              <svg v-else-if="item.icon === 'edit'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </div>
    </section>

    <!-- AI 模型集群 -->
    <section class="section">
      <h2 class="section-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="vertical-align: -3px"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg> 智慧集群</h2>
      <p class="section-subtitle">更深刻，更敏锐，更可靠</p>
      <div class="models-grid">
        <div class="model-card">
          <div class="model-badge">推理</div>
          <h3>高阶推理模型</h3>
          <p class="model-nickname">逻辑推演大师</p>
          <p>擅长理清错综复杂的伏笔脉络，为宏大的反转提供严密支撑。</p>
        </div>
        <div class="model-card">
          <div class="model-badge">润色</div>
          <h3>高阶润色模型</h3>
          <p class="model-nickname">文学造诣特长生</p>
          <p>擅长捕捉细腻的情绪波动，将直白的叙述升华为富有诗意的表达。</p>
        </div>
        <div class="model-card">
          <div class="model-badge">创作</div>
          <h3>高阶创作模型</h3>
          <p class="model-nickname">深海长效记忆</p>
          <p>拥有近乎无限的检索视野，能轻松跨越百万字篇幅，守护全书设定的连贯。</p>
        </div>
        <div class="model-card">
          <div class="model-badge">快写</div>
          <h3>低倍率快写模型</h3>
          <p class="model-nickname">灵感响应专家</p>
          <p>毫秒级的思考速率，即便在思绪如泉涌时，也能快速跟进每一个跳动的瞬间。</p>
        </div>
      </div>
    </section>

    <!-- 常见问题 -->
    <section class="section">
      <h2 class="section-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="vertical-align: -3px"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> 常见问题</h2>
      <div class="faq-list">
        <div
          v-for="(faq, index) in faqs"
          :key="index"
          class="faq-item"
          :class="{ open: openFaq === index }"
        >
          <div class="faq-question" @click="toggleFaq(index)">
            <span>{{ faq.q }}</span>
            <span class="faq-arrow">{{ openFaq === index ? '−' : '+' }}</span>
          </div>
          <div v-if="openFaq === index" class="faq-answer">
            <p>{{ faq.a }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <h2>你的故事，值得被讲述</h2>
      <p>立即开始，开启你的 AI 共创之旅。</p>
      <button class="cta-btn" @click="$router.push('/novel')">开始创作 →</button>
    </section>
  </div>
</template>

<style scoped>
.about-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}

/* Hero */
.hero {
  text-align: center;
  padding: 3rem 1rem 2rem;
}

.hero h1 {
  font-size: 2.2rem;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
}

.hero-subtitle {
  font-size: 1.4rem;
  color: #6c63ff;
  font-weight: 600;
  margin-bottom: 0.8rem;
}

.hero-desc {
  font-size: 1.05rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

/* Section */
.section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  color: #1a1a2e;
  text-align: center;
  margin-bottom: 0.3rem;
}

.section-subtitle {
  text-align: center;
  color: #888;
  margin-bottom: 1.5rem;
}

/* Features */
.features-grid {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.feature-card {
  background: #f8f9ff;
  border: 1px solid #e8eaff;
  border-radius: 12px;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
}

.feature-card:hover {
  box-shadow: 0 4px 16px rgba(108, 99, 255, 0.08);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.feature-card h3 {
  margin: 0 0 0.5rem;
  color: #1a1a2e;
}

.feature-desc {
  color: #555;
  margin: 0 0 0.8rem;
  line-height: 1.7;
}

.feature-highlights {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.feature-highlights li {
  background: #6c63ff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

/* Workflow */
.workflow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.workflow-item {
  text-align: center;
  padding: 1.5rem 1rem;
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  transition: border-color 0.2s;
}

.workflow-item:hover {
  border-color: #6c63ff;
}

.workflow-step {
  font-size: 0.8rem;
  color: #6c63ff;
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.workflow-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.workflow-item h3 {
  margin: 0 0 0.4rem;
  color: #1a1a2e;
  font-size: 1rem;
}

.workflow-item p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Models */
.models-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.model-card {
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 1.2rem;
}

.model-badge {
  display: inline-block;
  background: #6c63ff;
  color: white;
  padding: 0.15rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.model-card h3 {
  margin: 0 0 0.2rem;
  color: #1a1a2e;
  font-size: 1rem;
}

.model-nickname {
  color: #6c63ff;
  font-style: italic;
  font-size: 0.9rem;
  margin: 0 0 0.4rem;
}

.model-card > p:last-child {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
}

/* FAQ */
.faq-list {
  max-width: 700px;
  margin: 0 auto;
}

.faq-item {
  border: 1px solid #eee;
  border-radius: 10px;
  margin-bottom: 0.6rem;
  overflow: hidden;
  transition: border-color 0.2s;
}

.faq-item.open {
  border-color: #6c63ff;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.2rem;
  cursor: pointer;
  font-weight: 600;
  color: #1a1a2e;
  user-select: none;
}

.faq-question:hover {
  background: #f8f9ff;
}

.faq-arrow {
  font-size: 1.3rem;
  color: #6c63ff;
  flex-shrink: 0;
  margin-left: 1rem;
}

.faq-answer {
  padding: 0 1.2rem 1rem;
  color: #555;
  line-height: 1.7;
}

.faq-answer p {
  margin: 0;
}

/* CTA */
.cta {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #6c63ff 0%, #5a52d5 100%);
  border-radius: 16px;
  color: white;
  margin-top: 2rem;
}

.cta h2 {
  margin: 0 0 0.5rem;
  font-size: 1.6rem;
}

.cta p {
  margin: 0 0 1.2rem;
  opacity: 0.9;
}

.cta-btn {
  background: white;
  color: #6c63ff;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* 响应式 */
@media (max-width: 768px) {
  .workflow {
    grid-template-columns: repeat(2, 1fr);
  }

  .models-grid {
    grid-template-columns: 1fr;
  }

  .hero h1 {
    font-size: 1.6rem;
  }
}
</style>
