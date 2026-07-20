/**
 * Pinia 状态管理 - 计数器示例
 * Pinia 是 Vue 的新一代状态管理库，用于在组件之间共享数据
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// 定义一个名为 'counter' 的 Store
// 使用 Composition API 风格定义（推荐）
export const useCounterStore = defineStore('counter', () => {
  // === State（状态）===
  // ref() 创建响应式变量，类似于组件中的 data
  const count = ref(0)
  const name = ref('Vue 学习者')

  // === Getters（计算属性）===
  // computed() 创建计算属性，值会随依赖自动更新
  const doubleCount = computed(() => count.value * 2)

  // === Actions（操作）===
  // 普通函数，用于修改状态或执行异步操作
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  // 返回所有需要暴露的状态和方法
  return { count, name, doubleCount, increment, decrement, reset }
})
