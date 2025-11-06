import { createRouter, createWebHistory } from 'vue-router'
import AdminLogin from '../views/admin/AdminLogin.vue'
import AdminRegister from '../views/admin/Register.vue'
import AdminLogout from '../views/admin/AdminLogout.vue'
import AdminLayout from '../components/admin/AdminLayout.vue'

// 独立的管理后台路由配置
const routes = [
  // 管理员登录相关路由（无需布局）
  {
    path: '/login',
    name: 'adminLogin',
    component: AdminLogin,
    meta: {
      title: '管理员登录',
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: 'adminRegister',
    component: AdminRegister,
    meta: {
      title: '管理员注册',
      requiresAuth: false
    }
  },
  {
    path: '/logout',
    name: 'adminLogout',
    component: AdminLogout,
    meta: {
      title: '管理员注销'
    }
  },
  // 管理员后台主布局和页面
  {
    path: '/',
    component: AdminLayout,
    redirect: '/system-config',
    children: [
      {
        path: 'system-config',
        name: 'adminSystemConfig',
        component: () => import('@/views/admin/SystemConfig.vue'),
        meta: {
          title: '系统配置',
          breadcrumb: ['系统管理', '系统配置'],
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'user-management',
        name: 'adminUserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: {
          title: '用户管理',
          breadcrumb: ['系统管理', '用户管理'],
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'content-config',
        name: 'adminContentConfig',
        component: () => import('@/views/admin/ContentConfig.vue'),
        meta: {
          title: '内容配置',
          breadcrumb: ['内容管理', '内容配置'],
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'data-config',
        name: 'adminDataConfig',
        component: () => import('@/views/admin/DataConfig.vue'),
        meta: {
          title: '数据配置',
          breadcrumb: ['数据管理', '数据配置'],
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes
})

// 增强的路由守卫 - 严格的管理后台认证
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title + ' - 管理后台'
  } else {
    document.title = '管理后台 - 民俗文化展示系统'
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('adminToken')
    const userInfo = localStorage.getItem('adminUserInfo')
    
    if (!token) {
      // 没有token，重定向到登录页
      return next('/login')
    }
    
    // 检查token是否有效
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      if (payload.exp < currentTime) {
        // token已过期
        localStorage.removeItem('adminToken')
        localStorage.removeItem('adminUserInfo')
        return next('/login')
      }
      
      // 检查是否需要管理员权限
      if (to.meta.requiresAdmin) {
        if (userInfo) {
          const user = JSON.parse(userInfo)
          if (user.role !== 'admin') {
            // 权限不足，重定向到登录页
            return next('/login')
          }
        }
      }
      
    } catch (error) {
      // token解析失败
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminUserInfo')
      return next('/login')
    }
  }
  
  // 如果已经登录，访问登录页则重定向到首页
  if (to.path === '/login' || to.path === '/register') {
    const token = localStorage.getItem('adminToken')
    if (token) {
      return next('/')
    }
  }
  
  next()
})

export default router