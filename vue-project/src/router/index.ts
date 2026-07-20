/**
 * Vue Router 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/about', name: 'about', component: () => import('../views/AboutView.vue') },
    { path: '/counter', name: 'counter', component: () => import('../views/CounterView.vue') },
    { path: '/todo', name: 'todo', component: () => import('../views/TodoView.vue') },
    { path: '/novel', name: 'novel-list', component: () => import('../views/NovelListView.vue') },
    { path: '/novel/:id', name: 'novel-editor', component: () => import('../views/NovelEditorView.vue') },
    { path: '/snippets', name: 'snippets', component: () => import('../views/SnippetsView.vue') },
    { path: '/split', name: 'split', component: () => import('../views/SplitBookView.vue') },
    { path: '/prompts', name: 'prompts', component: () => import('../views/PromptPlazaView.vue') },
    { path: '/discuss', name: 'discuss', component: () => import('../views/DiscussView.vue') },
    { path: '/guide', name: 'guide', component: () => import('../views/GuideView.vue') },
    { path: '/about-platform', name: 'about-platform', component: () => import('../views/AboutPlatformView.vue') },
  ]
})

export default router
