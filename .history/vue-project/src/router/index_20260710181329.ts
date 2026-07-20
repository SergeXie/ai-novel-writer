/**
 * Vue Router 路由配置
 * 路由用于管理页面导航，让单页应用（SPA）可以像多页面一样跳转
 */
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// 定义路由规则
// 每个路由对应一个页面组件
const router = createRouter({
  // 使用 HTML5 History 模式，URL 更加美观
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',           // URL 路径
      name: 'home',        // 路由名称（可用于编程式导航）
      component: HomeView  // 对应的组件
    },
    {
      path: '/about',
      name: 'about',
      // 路由懒加载：只在访问该页面时才加载组件，提高首屏加载速度
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/counter',
      name: 'counter',
      component: () => import('../views/CounterView.vue')
    },
    {
      path: '/todo',
      name: 'todo',
      component: () => import('../views/TodoView.vue')
    },
    {
      path: '/novel',
      name: 'novel',
      component: () => import('../views/NovelView.vue')
    }
  ]
})

export default router
