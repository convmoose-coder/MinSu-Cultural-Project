import HomeView from '../views/HomeView.vue'

// 前台路由配置
export const frontendRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: '首页',
      requiresAuth: false
    }
  },
  {
    path: '/minzu',
    name: 'minzu',
    component: () => import('../views/MinzuView.vue'),
    meta: {
      title: '乘灼文化',
      requiresAuth: false
    }
  },
  {
    path: '/regions',
    name: 'regions',
    component: () => import('../views/RegionsView.vue'),
    meta: {
      title: '地区浏览',
      requiresAuth: false
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: {
      title: '关于我们',
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notFound',
    component: HomeView,
    meta: {
      title: '页面未找到',
      requiresAuth: false
    }
  }
]