import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/global.scss'
import '@/assets/styles/main.scss'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { MotionPlugin } from '@vueuse/motion'

// 添加全局导航栏样式，确保最高优先级
const style = document.createElement('style')
style.textContent = `
  /* 定义CSS变量 */
  :root {
    --navbar-bg-color: #87CEEB !important;
  }
  
  /* 使用最强大的选择器组合 */
  #custom-navbar {
    background-color: var(--navbar-bg-color) !important;
    background-image: none !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
  }
  
  /* 确保所有状态下都应用背景色 */
  #custom-navbar.navbar,
  #custom-navbar.navbar-scrolled,
  body #custom-navbar,
  html body #custom-navbar,
  nav#custom-navbar,
  nav#custom-navbar.navbar,
  nav#custom-navbar.navbar-scrolled {
    background-color: var(--navbar-bg-color) !important;
    background-image: none !important;
    opacity: 1 !important;
  }
  
  /* 确保容器不会覆盖背景色 */
  #custom-navbar .container,
  #custom-navbar .navbar-inner {
    background-color: transparent !important;
  }
`
document.head.appendChild(style)

// 在应用启动后立即执行的脚本，确保导航栏样式正确应用
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const navElement = document.getElementById('custom-navbar');
    if (navElement) {
      // 使用内联样式确保最高优先级
      navElement.style.setProperty('background-color', '#87CEEB', 'important');
      navElement.style.setProperty('background-image', 'none', 'important');
      navElement.style.setProperty('opacity', '1', 'important');
      
      // 移除可能影响背景色的类
      const classesToRemove = ['bg-white', 'bg-transparent', 'bg-light'];
      classesToRemove.forEach(className => {
        if (navElement.classList.contains(className)) {
          navElement.classList.remove(className);
        }
      });
    }
  }, 10);
});

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.use(MotionPlugin)

app.mount('#app')