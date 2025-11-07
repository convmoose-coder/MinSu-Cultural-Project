import { createRouter, createWebHistory } from 'vue-router'
import { frontendRoutes } from './frontendRoutes.js'

// 仅包含用户端前台路由
const routes = [
  ...frontendRoutes
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局路由守卫 - 仅处理前台路由
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = '民俗文化展示系统'
  }
  
  next()
})

export default router