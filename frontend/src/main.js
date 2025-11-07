import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/global.scss'
import './assets/styles/main.scss'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { MotionPlugin } from '@vueuse/motion'

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.use(MotionPlugin)

app.mount('#app')