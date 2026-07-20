<script setup lang="ts">
/**
 * 待办事项页面 - 综合示例
 * 演示表单处理、列表渲染、条件渲染和 Pinia 状态管理
 */
import { ref } from 'vue'
import { useTodoStore } from '../stores/todo'

// 获取 Store
const todoStore = useTodoStore()

// 本地状态：新待办事项的输入
const newTodo = ref('')

// 添加待办事项
function handleAdd() {
  if (newTodo.value.trim()) {
    todoStore.addTodo(newTodo.value)
    newTodo.value = ''  // 清空输入框
  }
}
</script>

<template>
  <div class="todo-page">
    <h1>📝 待办事项示例</h1>

    <div class="intro">
      <p>
        这个页面演示了 Vue 的核心功能：表单绑定、列表渲染、条件渲染，
        以及使用 Pinia 进行状态管理。
      </p>
    </div>

    <!-- 输入区域 -->
    <div class="input-section">
      <form @submit.prevent="handleAdd" class="input-form">
        <input 
          v-model="newTodo" 
          type="text" 
          placeholder="输入新的待办事项..." 
          class="todo-input"
        />
        <button type="submit" class="btn btn-add" :disabled="!newTodo.trim()">
          ➕ 添加
        </button>
      </form>
    </div>

    <!-- 统计信息 -->
    <div class="stats">
      <span class="stat">
        📊 总计：<strong>{{ todoStore.totalCount }}</strong>
      </span>
      <span class="stat">
        ⏳ 待完成：<strong>{{ todoStore.remainingCount }}</strong>
      </span>
      <span class="stat">
        ✅ 已完成：<strong>{{ todoStore.completedCount }}</strong>
      </span>
    </div>

    <!-- 待办事项列表 -->
    <div class="todo-list">
      <!-- 空状态提示 -->
      <div v-if="todoStore.todos.length === 0" class="empty-state">
        <p>📭 还没有待办事项，添加一个吧！</p>
      </div>

      <!-- 待办事项列表 -->
      <TransitionGroup name="list" tag="div">
        <div 
          v-for="todo in todoStore.todos" 
          :key="todo.id" 
          class="todo-item"
          :class="{ 'done': todo.done }"
        >
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              :checked="todo.done" 
              @change="todoStore.toggleTodo(todo.id)"
            />
            <span class="checkmark"></span>
          </label>
          
          <span class="todo-text">{{ todo.text }}</span>
          
          <button 
            @click="todoStore.removeTodo(todo.id)" 
            class="btn-delete"
            title="删除"
          >
            🗑️
          </button>
        </div>
      </TransitionGroup>
    </div>

    <!-- 清除已完成按钮 -->
    <div v-if="todoStore.completedCount > 0" class="clear-section">
      <button @click="todoStore.clearCompleted()" class="btn btn-clear">
        🧹 清除已完成 ({{ todoStore.completedCount }})
      </button>
    </div>

    <!-- 功能说明 -->
    <div class="tips">
      <h2>💡 功能说明</h2>
      <ul>
        <li><strong>v-model</strong>：双向数据绑定，输入框和数据自动同步</li>
        <li><strong>v-for</strong>：列表渲染，循环显示数组中的每一项</li>
        <li><strong>v-if / v-else</strong>：条件渲染，根据条件显示不同内容</li>
        <li><strong>@click / @change</strong>：事件监听，响应用户操作</li>
        <li><strong>TransitionGroup</strong>：列表动画，添加/删除时有过渡效果</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.todo-page {
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
  margin-bottom: 1.5rem;
  border-left: 4px solid #42b883;
}

.input-section {
  margin-bottom: 1.5rem;
}

.input-form {
  display: flex;
  gap: 0.5rem;
}

.todo-input {
  flex: 1;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 12px;
  transition: border-color 0.2s;
}

.todo-input:focus {
  outline: none;
  border-color: #42b883;
}

.btn {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add {
  background: #42b883;
  color: white;
}

.btn-add:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-clear {
  background: #f56c6c;
  color: white;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.stats {
  display: flex;
  justify-content: space-around;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.stat {
  text-align: center;
}

.stat strong {
  display: block;
  font-size: 1.5rem;
  color: #42b883;
}

.todo-list {
  min-height: 100px;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.todo-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: white;
  border: 2px solid #eee;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  transition: all 0.3s;
}

.todo-item:hover {
  border-color: #42b883;
}

.todo-item.done {
  background: #f8f9fa;
  border-color: #ddd;
}

.todo-item.done .todo-text {
  text-decoration: line-through;
  color: #999;
}

.checkbox-label {
  position: relative;
  cursor: pointer;
  margin-right: 1rem;
}

.checkbox-label input {
  opacity: 0;
  position: absolute;
}

.checkmark {
  width: 24px;
  height: 24px;
  border: 2px solid #ddd;
  border-radius: 6px;
  display: block;
  transition: all 0.2s;
}

.checkbox-label input:checked + .checkmark {
  background: #42b883;
  border-color: #42b883;
}

.checkbox-label input:checked + .checkmark::after {
  content: '✓';
  color: white;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
}

.todo-text {
  flex: 1;
  font-size: 1rem;
}

.btn-delete {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.btn-delete:hover {
  opacity: 1;
}

.clear-section {
  text-align: center;
  margin: 1.5rem 0;
}

.tips {
  background: #fff3cd;
  padding: 1.5rem;
  border-radius: 12px;
  margin-top: 2rem;
}

.tips h2 {
  margin-top: 0;
  color: #856404;
}

.tips ul {
  margin: 0;
  padding-left: 1.2rem;
}

.tips li {
  margin: 0.5rem 0;
  color: #856404;
}

/* 列表动画 */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
