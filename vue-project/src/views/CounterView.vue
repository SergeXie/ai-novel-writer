<script setup lang="ts">
/**
 * 计数器页面 - Pinia 状态管理示例
 * 演示如何使用 Pinia 在组件中管理和共享状态
 */
import { useCounterStore } from '../stores/counter'

// 获取 Store 实例
const counter = useCounterStore()
</script>

<template>
  <div class="counter-page">
    <h1>🔢 Pinia 状态管理示例</h1>
    
    <div class="intro">
      <p>
        Pinia 是 Vue 的官方状态管理库，可以让你在不同组件之间共享数据。
        下面的计数器演示了 Pinia 的基本用法。
      </p>
    </div>

    <!-- 计数器显示 -->
    <div class="counter-display">
      <div class="counter-value">
        <span class="label">当前计数</span>
        <span class="value">{{ counter.count }}</span>
      </div>
      
      <div class="counter-info">
        <p>👤 用户名：{{ counter.name }}</p>
        <p>✖️ 双倍计数：{{ counter.doubleCount }}</p>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="controls">
      <button @click="counter.increment()" class="btn btn-increase">
        ➕ 增加
      </button>
      <button @click="counter.decrement()" class="btn btn-decrease">
        ➖ 减少
      </button>
      <button @click="counter.reset()" class="btn btn-reset">
        🔄 重置
      </button>
    </div>

    <!-- 代码说明 -->
    <div class="code-explanation">
      <h2>📝 代码说明</h2>
      <pre><code>// 在组件中使用 Store
import {{ '{' }} useCounterStore {{ '}' }} from '../stores/counter'

// 获取 Store 实例
const counter = useCounterStore()

// 访问状态
counter.count        // 读取值

// 修改状态
counter.increment()  // 调用方法
counter.count++      // 直接修改</code></pre>
    </div>
  </div>
</template>

<style scoped>
.counter-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #42b883;
  text-align: center;
  margin-bottom: 1.5rem;
}

.intro {
  background: #f0f9ff;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border-left: 4px solid #42b883;
}

.counter-display {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  margin-bottom: 1.5rem;
}

.counter-value {
  margin-bottom: 1rem;
}

.counter-value .label {
  display: block;
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.counter-value .value {
  font-size: 4rem;
  font-weight: bold;
}

.counter-info p {
  margin: 0.5rem 0;
  opacity: 0.9;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-increase {
  background: #42b883;
  color: white;
}

.btn-decrease {
  background: #f56c6c;
  color: white;
}

.btn-reset {
  background: #909399;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.code-explanation {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1.5rem;
  border-radius: 12px;
}

.code-explanation h2 {
  color: #42b883;
  margin-top: 0;
  font-size: 1.2rem;
}

pre {
  margin: 0;
  overflow-x: auto;
}

code {
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
