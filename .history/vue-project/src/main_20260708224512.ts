import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 使用 Pinia 状态管理
app.use(createPinia())
// 使用 Vue Router 路由
app.use(router)

app.mount('#app')
