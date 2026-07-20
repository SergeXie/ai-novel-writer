/**
 * Pinia 状态管理 - 待办事项示例
 * 演示如何管理一个待办事项列表
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// 定义待办事项的数据结构
export interface Todo {
  id: number
  text: string
  done: boolean
}

export const useTodoStore = defineStore('todo', () => {
  // === State ===
  const todos = ref<Todo[]>([])
  let nextId = 1  // 用于生成唯一 ID

  // === Getters ===
  // 未完成的待办事项数量
  const remainingCount = computed(() => todos.value.filter(t => !t.done).length)
  // 已完成的待办事项数量
  const completedCount = computed(() => todos.value.filter(t => t.done).length)
  // 总数
  const totalCount = computed(() => todos.value.length)

  // === Actions ===
  // 添加待办事项
  function addTodo(text: string) {
    if (text.trim()) {
      todos.value.push({
        id: nextId++,
        text: text.trim(),
        done: false
      })
    }
  }

  // 删除待办事项
  function removeTodo(id: number) {
    todos.value = todos.value.filter(t => t.id !== id)
  }

  // 切换完成状态
  function toggleTodo(id: number) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      todo.done = !todo.done
    }
  }

  // 清除已完成的事项
  function clearCompleted() {
    todos.value = todos.value.filter(t => !t.done)
  }

  return { todos, remainingCount, completedCount, totalCount, addTodo, removeTodo, toggleTodo, clearCompleted }
})
