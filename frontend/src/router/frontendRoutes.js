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
    path: '/culture',
    name: 'culture',
    component: () => import('../views/CultureListView.vue'),
    meta: {
      title: '民俗文化列表',
      requiresAuth: false
    }
  },
  {
    path: '/culture/:id',
    name: 'cultureDetail',
    component: () => import('../views/CultureDetailView.vue'),
    meta: {
      title: '民俗文化详情',
      requiresAuth: false
    }
  },
  {
    path: '/regions',
    name: 'regions',
    component: () => import('../views/RegionsView.vue'),
    meta: {
      title: '地区文化',
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
      title: '页面未找到 - 民俗文化展示系统',
      requiresAuth: false
    }
  }
]