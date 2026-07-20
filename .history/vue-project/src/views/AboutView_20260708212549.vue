<script setup lang="ts">
/**
 * 关于页面 - Vue 3 基础知识展示
 * 演示模板语法、响应式数据和事件处理
 */
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'

// === 响应式数据 ===
// ref() 用于基本类型（字符串、数字、布尔值等）
const message = ref('你好，Vue 3！')
const count = ref(0)
const isVisible = ref(true)

// reactive() 用于对象/数组
const user = reactive({
  name: '学习者',
  age: 18,
  hobbies: ['编程', '阅读']
})

// === 计算属性 ===
// 根据响应式数据自动计算，有缓存功能
const doubleCount = computed(() => count.value * 2)
const userSummary = computed(() => `${user.name}，${user.age}岁，喜欢${user.hobbies.join('、')}`)

// === 方法 ===
function increment() {
  count.value++
}

function toggleVisibility() {
  isVisible.value = !isVisible.value
}

function addHobby() {
  user.hobbies.push('新爱好')
}

// === 生命周期钩子 ===
onMounted(() => {
  console.log('组件已挂载到页面！')
})

onUnmounted(() => {
  console.log('组件已从页面移除！')
})

// === 侦听器 ===
// 当数据变化时自动执行
watch(count, (newVal, oldVal) => {
  console.log(`计数从 ${oldVal} 变为 ${newVal}`)
})
</script>

<template>
  <div class="about">
    <h1>📖 Vue 3 基础知识</h1>

    <!-- 模板语法：插值 -->
    <section class="section">
      <h2>1. 模板插值</h2>
      <p>消息内容：<strong>{{ message }}</strong></p>
      <p>当前计数：<strong>{{ count }}</strong></p>
      <p>双倍计数（计算属性）：<strong>{{ doubleCount }}</strong></p>
    </section>

    <!-- 事件处理 -->
    <section class="section">
      <h2>2. 事件处理</h2>
      <div class="button-group">
        <button @click="increment" class="btn btn-primary">点击 +1</button>
        <button @click="count--" class="btn btn-secondary">点击 -1</button>
        <button @click="count = 0" class="btn btn-danger">重置</button>
      </div>
    </section>

    <!-- 条件渲染 -->
    <section class="section">
      <h2>3. 条件渲染</h2>
      <button @click="toggleVisibility" class="btn">
        {{ isVisible ? '隐藏' : '显示' }}内容
      </button>
      <p v-if="isVisible" class="visible-content">
        ✅ 这段文字会根据条件显示或隐藏！
      </p>
      <p v-else class="hidden-content">
        👋 这是隐藏时显示的内容！
      </p>
    </section>

    <!-- 列表渲染 -->
    <section class="section">
      <h2>4. 列表渲染</h2>
      <p>用户信息：{{ userSummary }}</p>
      <ul class="hobby-list">
        <li v-for="(hobby, index) in user.hobbies" :key="index">
          {{ index + 1 }}. {{ hobby }}
        </li>
      </ul>
      <button @click="addHobby" class="btn">添加爱好</button>
    </section>

    <!-- 响应式对象 -->
    <section class="section">
      <h2>5. 响应式对象 (reactive)</h2>
      <p>
        <input v-model="user.name" placeholder="修改姓名" class="input" />
      </p>
      <p>
        <input v-model.number="user.age" type="number" placeholder="修改年龄" class="input" />
      </p>
    </section>
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #42b883;
  text-align: center;
  margin-bottom: 2rem;
}

.section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.section h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #42b883;
  padding-bottom: 0.5rem;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-primary {
  background: #42b883;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.visible-content {
  color: #42b883;
  font-weight: bold;
}

.hidden-content {
  color: #6c757d;
  font-style: italic;
}

.hobby-list {
  list-style: none;
  padding: 0;
}

.hobby-list li {
  padding: 0.5rem;
  background: white;
  margin: 0.3rem 0;
  border-radius: 6px;
}

.input {
  padding: 0.5rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  width: 200px;
}

.input:focus {
  outline: none;
  border-color: #42b883;
}
</style>
